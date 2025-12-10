from django.conf import settings
from app.disable_mira_dumps import DATA_GROUP_LIST, DATA_GROUPS_PROGRAM
from django.db import transaction
from django.db.models import Prefetch, Max
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework import status
from generator.services.generator_service import GeneratorService
from app.utils import UserProfileHasPermission
from auths.models import Permissions
from generator.permissions import CanViewRPDProgram
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators, SemesterData
from competence_passport.models import Scheme
import logging
import re

logger = logging.getLogger(__name__)


class CompetencePassportViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]

    def get_queryset(self):
        return PlanData.objects.none()

    def _get_plan_or_error_response(self, plan_id):
        """Получение плана"""
        try:
            return PlanData.objects.get(mira_id=plan_id), None
        except PlanData.DoesNotExist:
            return None, Response(
                {'error': 'Учебный план не найден в базе данных'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def _get_discipline_or_error_response(self, plan, discipline_id):
        """Получение дисциплины"""
        try:
            return LinesData.objects.get(id=discipline_id, plan=plan), None
        except LinesData.DoesNotExist:
            return None, Response(
                {'error': 'Дисциплина не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def _get_all_competences_for_plan(self, plan):
        """Получение всех уникальных компетенций для плана"""
        plan_lines = LinesData.objects.filter(plan=plan)
        
        competences = LinesIndicators.objects.filter(
            planlineid__in=plan_lines, 
            competence__isnull=False,
            competence_index__isnull=False
        ).values(
            'competence_index',
            'competence'
        ).distinct()
        
        return list(competences)

    def _get_competence_type(self, competence_index):
        """Определяет тип компетенции по индексу"""
        if not competence_index:
            return 'Неизвестно'
        
        if 'УК' in competence_index or competence_index.startswith('УК'):
            return 'Универсальная'
        elif 'ОПК' in competence_index or competence_index.startswith('ОПК'):
            return 'Общепрофессиональная'
        elif 'ПК' in competence_index or competence_index.startswith('ПК'):
            return 'Профессиональная'
        elif 'ДК' in competence_index or competence_index.startswith('ДК'):
            return 'Дополнительная'
        else:
            return 'Другая'

    def _extract_competence_parts(self, competence_index):
        """Извлекает тип и номер компетенции для сортировки"""
        if not competence_index:
            return ('', '', 0, 0, 0)
        
        normalized = competence_index.strip()
        
        # Паттерны для разных форматов:
        # 1. "УК ОС-1", "УК ОС-1.1", "УК ОС-1.1.1"
        # 2. "УК-1", "УК-1.1", "УК-1.1.1"
        
        # Паттерн для формата "УК ОС-1" или "УК ОС-1.1"
        match = re.match(r'^(УК|ОПК|ПК|ДК)\s*([А-ЯЁA-Z]+)?-?(\d+)(?:\.(\d+))?(?:\.(\d+))?$', normalized, re.IGNORECASE)
        if match:
            groups = match.groups()
            prefix = groups[0] or ''
            sub_type = groups[1] or ''
            num1 = int(groups[2]) if groups[2] else 0
            num2 = int(groups[3]) if groups[3] else 0
            num3 = int(groups[4]) if groups[4] else 0
            return (prefix, sub_type, num1, num2, num3)
        
        # Паттерн для формата "УК-1" 
        match = re.match(r'^(УК|ОПК|ПК|ДК)[-\s]*(\d+)(?:\.(\d+))?(?:\.(\d+))?$', normalized, re.IGNORECASE)
        if match:
            groups = match.groups()
            prefix = groups[0] or ''
            num1 = int(groups[1]) if groups[1] else 0
            num2 = int(groups[2]) if groups[2] else 0
            num3 = int(groups[3]) if groups[3] else 0
            return (prefix, '', num1, num2, num3)
        
        return ('', '', 0, 0, 0)

    def _sort_competences(self, competences_list):
        """Сортировка списка компетенций по типу и индексу с числовой сортировкой"""
        def sort_key(item):
            competence_index = item.get('competence_index', '')
            
            # Сортируем по типу компетенции
            type_order = {
                'Универсальная': 1,
                'Общепрофессиональная': 2,
                'Профессиональная': 3,
                'Дополнительная': 4,
                'Другая': 5
            }
            comp_type = self._get_competence_type(competence_index)
            type_priority = type_order.get(comp_type, 99)
            
            prefix, sub_type, num1, num2, num3 = self._extract_competence_parts(competence_index)
            
            # Сортируем по префиксу (УК, ОПК, ПК, ДК)
            prefix_order = {'УК': 1, 'ОПК': 2, 'ПК': 3, 'ДК': 4}
            prefix_priority = prefix_order.get(prefix.upper(), 5)
            
            return (type_priority, prefix_priority, num1, num2, num3, competence_index)
        
        return sorted(competences_list, key=sort_key)

    def _update_kompetences_cache(self, discipline):
        """Обновляет поле kompetences в LinesData"""
        # Получаем все индикаторы дисциплины
        indicators = LinesIndicators.objects.filter(
            planlineid=discipline,
            competence_index__isnull=False
        ).order_by('indicator_index')
        
        if indicators.exists():
            # Формируем строку индикаторов через запятую
            indicator_list = [ind.indicator_index for ind in indicators]
            kompetences_str = ",".join(indicator_list)
        else:
            kompetences_str = ""
        
        discipline.kompetences = kompetences_str
        discipline.save(update_fields=['kompetences'])

    def _get_plan_response_data(self, plan, additional_data=None):
        """Базовые данные ответа для методов, работающих с планом"""
        base_data = {
            'plan_id': plan.id,
            'plan_mira_id': plan.mira_id,
            'plan_name': plan.planname,
            'abbrprofile': plan.abbrprofile
        }
        
        if additional_data:
            base_data.update(additional_data)
            
        return base_data

    def _validate_plan_id(self, plan_id):
        """Валидация ID плана"""
        if not plan_id:
            return Response(
                {'error': 'ID плана не указан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return None

    def _natural_sort_key(self, s):
        """Ключ для естественной сортировки (natural sort)"""
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        
        return [convert(c) for c in re.split(r'(\d+)', s)]

    def _sort_competence_list(self, competence_list):
        """Сортировка списка индексов компетенций"""
        if isinstance(competence_list, set):
            competence_list = list(competence_list)
        
        temp_items = [{'competence_index': comp} for comp in competence_list]
        sorted_items = self._sort_competences(temp_items)
        
        return [item['competence_index'] for item in sorted_items]

    @action(methods=['GET'], detail=False, url_path='group-list')
    def get_group_list(self, request, *args, **kwargs):
        txt_filter = self.request.query_params.get('text')
        group_txt_filter = self.request.query_params.get('groupText')
        status_filter = self.request.query_params.get('status')
        my_filter = self.request.query_params.get('my')
        year_filter = self.request.query_params.get('year')
        
        if settings.DISABLE_MIRA:
           res = DATA_GROUP_LIST
        else:
            res = GeneratorService.get_group_list(
                self.request.user.userprofile.mira_id, 
                year_filter, 
                txt_filter,
                group_txt_filter, 
                status_filter, 
                my_filter
            )

        return Response(data=res)
        
    @action(methods=['GET'], detail=False, url_path='all-competences')
    def get_all_competences(self, request):
        """Получение всех компетенций для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            error_response = self._validate_plan_id(plan_id)
            if error_response:
                return error_response
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            competences = self._get_all_competences_for_plan(plan)
            sorted_competences = self._sort_competences(competences)
            
            competences_list = [
                {
                    'id': f"{comp['competence_index']}_{hash(comp['competence'])}",
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                }
                for comp in sorted_competences
            ]
            
            return Response(self._get_plan_response_data(plan, {
                'competences': competences_list
            }))
            
        except Exception as e:
            logger.error(f"Error fetching competences for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['GET'], detail=False, url_path='all-disciplines')
    def get_all_disciplines(self, request):
        """Получение всех дисциплин для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            error_response = self._validate_plan_id(plan_id)
            if error_response:
                return error_response
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            disciplines = LinesData.objects.filter(
                plan=plan
            ).values(
                'id',
                'newdisid',
                'dis',
                'synchronize'
            ).order_by('newdisid')
            
            disciplines_list = [
                {
                    'id': disc['id'],
                    'newdisid': disc['newdisid'],
                    'dis': disc['dis'],
                    'synchronize': disc['synchronize']
                }
                for disc in disciplines
            ]
            
            return Response(self._get_plan_response_data(plan, {
                'disciplines': disciplines_list
            }))
            
        except Exception as e:
            logger.error(f"Error fetching disciplines for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении дисциплин: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-matrix')
    def get_competence_matrix(self, request):
        """Получение матрицы компетенций для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            error_response = self._validate_plan_id(plan_id)
            if error_response:
                return error_response
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            # Получаем все дисциплины плана
            disciplines = LinesData.objects.filter(
                plan=plan
            ).prefetch_related(
                Prefetch(
                    'indicators',
                    queryset=LinesIndicators.objects.filter(
                        competence__isnull=False,
                        competence_index__isnull=False
                    ).only('competence_index', 'competence')
                )
            ).order_by('newdisid')
            
            # Получаем все уникальные компетенции
            all_competences = self._get_all_competences_for_plan(plan)
            all_competences_sorted = self._sort_competences(all_competences)
            all_competence_indices = [comp['competence_index'] for comp in all_competences_sorted]
            
            # Создаем словарь для группировки дисциплины по префиксам
            groups = {}
            
            # Определяем названия для основных групп
            group_names = {
                'Б1': 'Дисциплины (модули)',
                'Б1.Б': 'Обязательная часть',
                'Б1.Б.01': 'Общеобразовательный модуль',
                'Б1.Б.02': 'Фундаментальный модуль',
                'Б1.Б.03': 'Базовый модуль направления',
                'Б1.Б.04': 'Модуль проектной деятельности',
                'Б1.Б.05': 'Модуль по физической культуре и спорту',
                'Б1.В': 'Вариативная часть',
                'Б1.В.01': 'Модуль проектной деятельности',
                'Б1.В.02': 'Модуль профильной подготовки',
                'Б1.В.03': 'Модуль дополнительного профиля',
                'Б2': 'Практика',
                'Б2.Б': 'Обязательная часть',
                'Б2.В': 'Вариативная часть',
                'Б3': 'Государственная итоговая аттестация',
                'ФТД': 'Факультативы'
            }
            
            for discipline in disciplines:
                if not discipline.newdisid:
                    continue
                
                # Получаем компетенции для этой дисциплины
                discipline_competences = set()
                for indicator in discipline.indicators.all():
                    if indicator.competence_index:
                        discipline_competences.add(indicator.competence_index)
                
                disc_key = discipline.newdisid
                if disc_key not in groups:
                    groups[disc_key] = {
                        'type': 'discipline',
                        'index': disc_key,
                        'name': discipline.dis,
                        'competences': discipline_competences,
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }
                
                parts = disc_key.split('.')
                for i in range(len(parts)):
                    group_key = '.'.join(parts[:i+1])
                    
                    base_group_key = group_key
                    if base_group_key.startswith('Б1.Б.05.02'):
                        base_group_key = 'Б1.Б.05'
                    elif base_group_key.startswith('Б1.В.02.ДВ'):
                        base_group_key = 'Б1.В.02'
                    elif base_group_key.startswith('Б1.В.ДВ'):
                        base_group_key = 'Б1.В'
                    
                    if base_group_key not in groups:
                        groups[base_group_key] = {
                            'type': 'group',
                            'index': base_group_key,
                            'name': group_names.get(base_group_key, base_group_key),
                            'competences': set(),
                            'level': base_group_key.count('.') + 1 if '.' in base_group_key else 1
                        }
                    groups[base_group_key]['competences'].update(discipline_competences)
            
            matrix_data = []
            for item in groups.values():
                sorted_competences = self._sort_competence_list(item['competences'])
                indices_str = ", ".join(sorted_competences)
                
                matrix_data.append({
                    'type': item['type'], 
                    'level': item['level'],  
                    'index': item['index'],
                    'name': item['name'],
                    'competence_indices': indices_str,
                    'competence_indices_list': sorted_competences
                })
            
            def sort_key(x):
                type_order = 0 if x['type'] == 'group' else 1
                return (type_order, x['index'])
            
            matrix_data.sort(key=sort_key)
            
            return Response(self._get_plan_response_data(plan, {
                'matrix': matrix_data
            }))
            
        except Exception as e:
            logger.error(f"Error fetching competence matrix for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении матрицы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='discipline-competences-detailed')
    def get_discipline_competences_detailed(self, request):
        """Детальная информация о компетенциях дисциплины с индикаторами"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            discipline_id = self.request.query_params.get('discipline_id')
            
            if not plan_id or not discipline_id:
                return Response(
                    {'error': 'ID плана и дисциплины обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            discipline, error_response = self._get_discipline_or_error_response(plan, discipline_id)
            if error_response:
                return error_response
            
            all_competences = self._get_all_competences_for_plan(plan)
            sorted_competences = self._sort_competences(all_competences)
            
            discipline_indicators = LinesIndicators.objects.filter(
                planlineid=discipline
            ).order_by('indicator_index')
            
            # Группируем индикаторы по компетенциям
            current_competences = {}
            for indicator in discipline_indicators:
                comp_index = indicator.competence_index
                if comp_index:
                    if comp_index not in current_competences:
                        current_competences[comp_index] = {
                            'competence': indicator.competence,
                            'indicators': [],
                            'indicators_count': 0
                        }
                    current_competences[comp_index]['indicators'].append({
                        'index': indicator.indicator_index,
                        'name': indicator.indicator
                    })
                    current_competences[comp_index]['indicators_count'] += 1
            
            # Формируем список компетенций с детальной информацией
            competences_list = []
            for comp in sorted_competences:
                comp_index = comp['competence_index']
                is_selected = comp_index in current_competences
                
                competences_list.append({
                    'competence_index': comp_index,
                    'competence': comp['competence'],
                    'selected': is_selected,
                    'type': self._get_competence_type(comp_index),
                    'indicators_count': current_competences.get(comp_index, {}).get('indicators_count', 0),
                    'indicators': current_competences.get(comp_index, {}).get('indicators', [])
                })
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'discipline_id': discipline.id,
                'discipline_index': discipline.newdisid,
                'discipline_name': discipline.dis,
                'competences': competences_list,
                'current_kompetences': discipline.kompetences or ""
            })
            
        except Exception as e:
            logger.error(f"Error fetching detailed discipline competences: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении детальной информации: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['POST'], detail=False, url_path='update-discipline-competences')
    def update_discipline_competences(self, request):
        """Обновление компетенций для дисциплины с выбранными компетенциями"""
        try:
            plan_id = request.data.get('plan_id')
            discipline_id = request.data.get('discipline_id')
            selected_competences = request.data.get('selected_competences', [])
            
            if not plan_id or not discipline_id:
                return Response(
                    {'error': 'ID плана и дисциплины обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            discipline, error_response = self._get_discipline_or_error_response(plan, discipline_id)
            if error_response:
                return error_response
            
            with transaction.atomic():
                # Получаем текущие компетенции дисциплины
                current_indicators = LinesIndicators.objects.filter(
                    planlineid=discipline
                )
                
                current_competences = {}
                for indicator in current_indicators:
                    comp_index = indicator.competence_index
                    if comp_index not in current_competences:
                        current_competences[comp_index] = []
                    current_competences[comp_index].append(indicator)
                
                # Получаем индексы выбранных компетенций из запроса
                selected_comp_indices = [comp['competence_index'] for comp in selected_competences]
                
                # Компетенции для удаления 
                comp_to_delete = set(current_competences.keys()) - set(selected_comp_indices)
                
                # Компетенции для добавления
                comp_to_add = set(selected_comp_indices) - set(current_competences.keys())
                
                # Компетенции которые остаются 
                comp_to_keep = set(current_competences.keys()) & set(selected_comp_indices)
                
                deleted_count = 0
                added_count = 0
                kept_count = 0
                
                # 1. Удляем компетенции, которые не выбраны
                for comp_index in comp_to_delete:
                    deleted = LinesIndicators.objects.filter(
                        planlineid=discipline,
                        competence_index=comp_index
                    ).delete()
                    deleted_count += deleted[0]
                
                # 2. Добавляем новые компетенции
                for comp_index in comp_to_add:
                    comp_data = next((c for c in selected_competences 
                                    if c['competence_index'] == comp_index), None)
                    if not comp_data:
                        continue
                    
                    competence_name = comp_data.get('competence')
                    indicators_data = comp_data.get('indicators', [])
                    
                    # Получаем исходное количество индикаторов для этой компетенции в других дисциплинах или используем количество из запроса, если есть
                    if indicators_data:
                        for idx, indicator_data in enumerate(indicators_data, 1):
                            indicator = LinesIndicators(
                                planlineid=discipline,
                                competence_index=comp_index,
                                competence=competence_name,
                                indicator_index=indicator_data.get('index', f"{comp_index}.{idx}"),
                                indicator=indicator_data.get('name', '')
                            )
                            indicator.save()
                            added_count += 1
                    else:
                        # Создаем один индикатор по умолчанию
                        max_indicator = LinesIndicators.objects.filter(
                            planlineid__plan=plan,
                            competence_index=comp_index
                        ).aggregate(Max('indicator_index'))['indicator_index__max']
                        
                        if max_indicator:
                            try:
                                last_num = int(max_indicator.split('.')[-1])
                                indicator_num = last_num + 1
                            except (ValueError, IndexError):
                                indicator_num = 1
                        else:
                            indicator_num = 1
                        
                        indicator = LinesIndicators(
                            planlineid=discipline,
                            competence_index=comp_index,
                            competence=competence_name,
                            indicator_index=f"{comp_index}.{indicator_num}",
                            indicator=""
                        )
                        indicator.save()
                        added_count += 1
                
                # 3. Считаем компетенции, которые остались без изменений
                for comp_index in comp_to_keep:
                    kept_count += len(current_competences[comp_index])
                
                self._update_kompetences_cache(discipline)
                
                comp_to_delete_sorted = self._sort_competence_list(comp_to_delete)
                comp_to_add_sorted = self._sort_competence_list(comp_to_add)
                comp_to_keep_sorted = self._sort_competence_list(comp_to_keep)
                
                return Response({
                    'success': True,
                    'message': f'Удалено {deleted_count} индикаторов, добавлено {added_count} индикаторов, сохранено {kept_count} индикаторов',
                    'deleted': deleted_count,
                    'added': added_count,
                    'kept': kept_count,
                    'total': deleted_count + added_count + kept_count,
                    'competences_deleted': comp_to_delete_sorted,
                    'competences_added': comp_to_add_sorted,
                    'competences_kept': comp_to_keep_sorted,
                    'discipline': {
                        'id': discipline.id,
                        'index': discipline.newdisid,
                        'name': discipline.dis
                    }
                })
                
        except Exception as e:
            logger.error(f"Error updating discipline competences: {str(e)}")
            return Response(
                {'error': f'Ошибка при обновлении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['GET'], detail=False, url_path='discipline-semester-schemes')
    def get_discipline_semester_schemes(self, request):
        """Получение схем форм аттестации для дисциплины по компетенциям"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            discipline_id = self.request.query_params.get('discipline_id')
            
            if not plan_id or not discipline_id:
                return Response(
                    {'error': 'ID плана и дисциплины обязательны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            discipline, error_response = self._get_discipline_or_error_response(plan, discipline_id)
            if error_response:
                return error_response
            
            # Получаем все компетенции дисциплины
            competence_indicators = LinesIndicators.objects.filter(
                planlineid=discipline,
                competence_index__isnull=False
            ).values('competence_index', 'competence').distinct()
            
            # Получаем существующие схемы для этой дисциплины
            existing_schemes = Scheme.objects.filter(
                planlineid=discipline
            ).order_by('competence_index', 'semester')
            
            # Группируем схемы по компетенциям
            schemes_by_competence = {}
            for scheme in existing_schemes:
                comp_key = scheme.competence_index
                if comp_key not in schemes_by_competence:
                    schemes_by_competence[comp_key] = []
                schemes_by_competence[comp_key].append({
                    'semester': scheme.semester,
                    'ekz': scheme.ekz or False,
                    'zach': scheme.zach or False,
                    'zacho': scheme.zacho or False,
                    'kp': scheme.kp or False,
                    'kr': scheme.kr or False,
                    'id': scheme.id
                })
            
            semesters = SemesterData.objects.filter(planlineid=discipline).order_by('num')
            semester_numbers = [sem.num for sem in semesters]
            
            # Формируем данные по компетенциям
            competence_schemes = []
            for comp in competence_indicators:
                comp_schemes = schemes_by_competence.get(comp['competence_index'], [])
                
                # Создаем структуру для всех семестров дисциплины
                semesters_data = {}
                for sem_num in range(1, 9):  # Все возможные семестры
                    forms = []
                    scheme_id = None
                    
                    # Ищем схему для этого семестра
                    for scheme in comp_schemes:
                        if scheme['semester'] == sem_num:
                            if scheme['ekz']: forms.append('Э')
                            if scheme['zach']: forms.append('З')
                            if scheme['zacho']: forms.append('Зо')
                            if scheme['kp']: forms.append('КП')
                            if scheme['kr']: forms.append('КР')
                            scheme_id = scheme['id']
                            break
                    
                    semesters_data[f'semester_{sem_num}'] = {
                        'forms': forms,
                        'forms_display': ', '.join(forms) if forms else '',
                        'scheme_id': scheme_id,
                        'has_scheme': len(forms) > 0
                    }
                
                competence_schemes.append({
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence'],
                    'semesters': semesters_data
                })
            
            return Response({
                'plan_id': plan.id,
                'discipline_id': discipline.id,
                'discipline_index': discipline.newdisid,
                'discipline_name': discipline.dis,
                'semester_numbers': semester_numbers,
                'competence_schemes': competence_schemes
            })
            
        except Exception as e:
            logger.error(f"Error fetching discipline semester schemes: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении схем форм аттестации: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['POST'], detail=False, url_path='update-semester-scheme')
    def update_semester_scheme(self, request):
        """Обновление схемы формы аттестации для компетенции в семестре"""
        try:
            plan_id = request.data.get('plan_id')
            discipline_id = request.data.get('discipline_id')
            competence_index = request.data.get('competence_index')
            semester = request.data.get('semester')
            forms = request.data.get('forms', {})
            
            if not all([plan_id, discipline_id, competence_index, semester]):
                return Response(
                    {'error': 'Все обязательные поля должны быть заполнены'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            discipline, error_response = self._get_discipline_or_error_response(plan, discipline_id)
            if error_response:
                return error_response
            
            forms_converted = {}
            for key in ['ekz', 'zach', 'zacho', 'kp', 'kr']:
                value = forms.get(key, False)
                forms_converted[key] = bool(value)
            
            has_any_form = any(forms_converted.values())
            
            with transaction.atomic():
                # Проверяем, существует ли компетенция для этой дисциплины
                competence_exists = LinesIndicators.objects.filter(
                    planlineid=discipline,
                    competence_index=competence_index
                ).exists()
                
                if not competence_exists:
                    return Response(
                        {'error': 'Компетенция не привязана к данной дисциплине'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                semester_exists = SemesterData.objects.filter(
                    planlineid=discipline,
                    num=semester
                ).exists()
                
                if not semester_exists:
                    return Response(
                        {'error': 'Указанный семестр не существует для данной дисциплины'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                competence_name = None
                competence_obj = LinesIndicators.objects.filter(
                    planlineid=discipline,
                    competence_index=competence_index
                ).first()
                if competence_obj:
                    competence_name = competence_obj.competence
                
                if has_any_form:
                    # Создаем или обновляем запись
                    scheme, created = Scheme.objects.update_or_create(
                        planlineid=discipline,
                        competence_index=competence_index,
                        semester=semester,
                        defaults={
                            'competence': competence_name or competence_index,
                            'ekz': forms_converted['ekz'],
                            'zach': forms_converted['zach'],
                            'zacho': forms_converted['zacho'],
                            'kp': forms_converted['kp'],
                            'kr': forms_converted['kr']
                        }
                    )
                    scheme_id = scheme.id
                else:
                    # Удаляем запись, если она существует
                    deleted_count, _ = Scheme.objects.filter(
                        planlineid=discipline,
                        competence_index=competence_index,
                        semester=semester
                    ).delete()
                    
                    scheme_id = None
                    created = False
                
                # Формируем строку для отображения
                forms_display = []
                if forms_converted['ekz']: forms_display.append('Э')
                if forms_converted['zach']: forms_display.append('З')
                if forms_converted['zacho']: forms_display.append('Зо')
                if forms_converted['kp']: forms_display.append('КП')
                if forms_converted['kr']: forms_display.append('КР')
                
                return Response({
                    'success': True,
                    'scheme_id': scheme_id,
                    'created': created,
                    'forms_display': ', '.join(forms_display) if forms_display else '',
                    'has_forms': has_any_form,
                    'message': 'Схема успешно обновлена'
                })
                
        except Exception as e:
            logger.error(f"Error updating semester scheme: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Ошибка при обновлении схемы: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['GET'], detail=False, url_path='competence-schema-data')
    def get_competence_schema_data(self, request):
        """Получение данных для схемы компетенций с формами аттестации"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            error_response = self._validate_plan_id(plan_id)
            if error_response:
                return error_response
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            all_competences = self._get_all_competences_for_plan(plan)
            competences = self._sort_competences(all_competences)
            
            # Получаем дисциплины с семестрами и индикаторами
            disciplines = LinesData.objects.filter(
                plan=plan
            ).prefetch_related(
                Prefetch(
                    'semesters',
                    queryset=SemesterData.objects.all().order_by('num')
                ),
                Prefetch(
                    'indicators',
                    queryset=LinesIndicators.objects.filter(
                        competence__isnull=False,
                        competence_index__isnull=False
                    )
                ),
                Prefetch(
                    'competence_schemes',
                    queryset=Scheme.objects.all()
                )
            ).order_by('newdisid')
            
            # Определяем группы, которые нужно исключить
            groups_to_exclude = {
                'Б1',
                'Б1.Б',
                'Б1.Б.01',
                'Б1.Б.02',
                'Б1.Б.03',
                'Б1.Б.04',
                'Б1.Б.05',
                'Б1.В',
                'Б1.В.01',
                'Б1.В.02',
                'Б1.В.02.ДВ.01',
                'Б1.В.02.ДВ.02',
                'Б1.В.03',
                'Б2',
                'Б2.Б',
                'Б2.В',
                'Б3',
                'ФТД'
            }
            
            schema_rows = []
            
            for comp in competences:
                comp_index = comp['competence_index']
                comp_name = comp['competence']
                comp_type = self._get_competence_type(comp_index)
                
                schema_rows.append({
                    'type': 'competence',
                    'competence_index': comp_index,
                    'competence_name': comp_name,
                    'competence_type': comp_type,
                    'id': f"comp_{comp_index.replace('.', '_').replace('-', '_')}"
                })
                
                # Находим дисциплины, формирующие эту компетенцию
                discipline_rows = []
                for disc in disciplines:
                    if disc.newdisid and disc.newdisid in groups_to_exclude:
                        continue
                    
                    has_competence = any(
                        indicator.competence_index == comp_index 
                        for indicator in disc.indicators.all()
                    )
                    
                    if has_competence:
                        # Получаем схемы для этой компетенции и дисциплины
                        competence_schemes = {}
                        for scheme in disc.competence_schemes.all():
                            if scheme.competence_index == comp_index:
                                forms = []
                                if scheme.ekz: forms.append('Э')
                                if scheme.zach: forms.append('З')
                                if scheme.zacho: forms.append('Зо')
                                if scheme.kp: forms.append('КП')
                                if scheme.kr: forms.append('КР')
                                
                                competence_schemes[scheme.semester] = {
                                    'forms': forms,
                                    'forms_display': ', '.join(forms) if forms else '',
                                    'has_custom_scheme': len(forms) > 0
                                }
                        
                        # Заполняем все 8 семестров
                        full_semester_data = {}
                        for i in range(1, 9):
                            key = f'semester_{i}'
                            if i in competence_schemes:
                                full_semester_data[key] = competence_schemes[i]
                            else:
                                full_semester_data[key] = {
                                    'forms': [],
                                    'forms_display': '',
                                    'has_custom_scheme': False
                                }
                        
                        discipline_rows.append({
                            'type': 'discipline',
                            'discipline_index': disc.newdisid or '',
                            'discipline_name': disc.dis,
                            'discipline_id': disc.id,
                            'parent_competence': comp_index,
                            **full_semester_data
                        })
                
                if discipline_rows:
                    schema_rows.extend(discipline_rows)
                else:
                    schema_rows.pop()
            
            all_disciplines_with_competences = LinesData.objects.filter(
                plan=plan,
                indicators__competence_index__isnull=False
            ).distinct()
            
            all_competence_indices = set()
            for disc in all_disciplines_with_competences:
                if disc.newdisid and disc.newdisid in groups_to_exclude:
                    continue
                    
                for indicator in disc.indicators.all():
                    if indicator.competence_index:
                        all_competence_indices.add(indicator.competence_index)
            
            competences_without_disciplines = []
            for comp in competences:
                if comp['competence_index'] not in all_competence_indices:
                    competences_without_disciplines.append(comp)
            
            if competences_without_disciplines:
                schema_rows.append({
                    'type': 'divider',
                    'label': f'Компетенции без дисциплин ({len(competences_without_disciplines)})'
                })
                
                for comp in competences_without_disciplines:
                    schema_rows.append({
                        'type': 'competence',
                        'competence_index': comp['competence_index'],
                        'competence_name': comp['competence'],
                        'competence_type': self._get_competence_type(comp['competence_index']),
                        'warning': True
                    })
            
            return Response(self._get_plan_response_data(plan, {
                'schema_rows': schema_rows
            }))
            
        except Exception as e:
            logger.error(f"Error fetching competence schema data for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении данных схемы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )