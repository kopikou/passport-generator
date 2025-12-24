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
from competence_passport.models import Scheme, CompetenceRelations
from generator.models import DisciplineIndicators, PlanLinesLink
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
            
            prefix, sub_type, num1, num2, num3 = self._extract_competence_parts(competence_index)
            
            # Сортируем по префиксу (УК, ОПК, ПК, ДК)
            prefix_order = {'УК': 1, 'ОПК': 2, 'ПК': 3, 'ДК': 4}
            prefix_priority = prefix_order.get(prefix.upper(), 5)

            return (prefix_priority, num1, num2, num3)
        
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
            #logger.error(f"Error fetching competences for plan {plan_id}: {str(e)}")
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
                'ФТД',
                'Б1.Б.05.02.ДВ.01',
            }
            
            disciplines = LinesData.objects.filter(
                plan=plan
            ).values(
                'id',
                'newdisid',
                'dis',
                'synchronize'
            ).order_by('newdisid')
            
            filtered_disciplines = []
            for disc in disciplines:
                disc_newdisid = disc['newdisid']
                
                if not disc_newdisid:
                    filtered_disciplines.append(disc)
                    continue
                
                should_exclude = False

                if disc_newdisid in groups_to_exclude:
                    should_exclude = True
                
                if not should_exclude:
                    filtered_disciplines.append(disc)
            
            disciplines_list = [
                {
                    'id': disc['id'],
                    'newdisid': disc['newdisid'],
                    'dis': disc['dis'],
                    'synchronize': disc['synchronize']
                }
                for disc in filtered_disciplines
            ]
            
            return Response(self._get_plan_response_data(plan, {
                'disciplines': disciplines_list
            }))
            
        except Exception as e:
            #logger.error(f"Error fetching disciplines for plan {plan_id}: {str(e)}")
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
            #logger.error(f"Error fetching competence matrix for plan {plan_id}: {str(e)}")
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
            #logger.error(f"Error fetching detailed discipline competences: {str(e)}")
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
            #logger.error(f"Error updating discipline competences: {str(e)}")
            return Response(
                {'error': f'Ошибка при обновлении компетенций: {str(e)}'}, 
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
            #logger.error(f"Error updating semester scheme: {str(e)}", exc_info=True)
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
                'Б2.В'
            }

            groups_to_exclude_with_children = {
                'Б3',
                'ФТД', 
                'Б1.Б.05.02.ДВ.01'
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
                    should_exclude = False
                    disc_newdisid = disc.newdisid
                    
                    if disc_newdisid:
                        if disc_newdisid in groups_to_exclude:
                            should_exclude = True

                        for group in groups_to_exclude_with_children:
                            if disc_newdisid.startswith(group + '.'): 
                                should_exclude = True
                                break
                            elif disc_newdisid == group: 
                                should_exclude = True
                                break
                    
                    if should_exclude:
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
            
            return Response(self._get_plan_response_data(plan, {
                'schema_rows': schema_rows
            }))
            
        except Exception as e:
            #logger.error(f"Error fetching competence schema data for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении данных схемы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='plan-details')
    def get_plan_details(self, request):
        """Получение детальной информации о плане для титульного листа"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            error_response = self._validate_plan_id(plan_id)
            if error_response:
                return error_response
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response
            
            # 1. Находим PlanLinesLink для этого плана
            first_discipline = LinesData.objects.filter(plan=plan).first()
            if not first_discipline:
                return Response(
                    {'error': 'В плане нет дисциплин'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            plan_lines_link = PlanLinesLink.objects.filter(
                planlines=first_discipline
            ).first()
            
            # 2. Получаем данные 
            user_mira_id = self.request.user.userprofile.mira_id if hasattr(self.request.user, 'userprofile') else None
            plan_data = GeneratorService.get_rpd_data(plan_lines_link.id, user_mira_id)
            
            # 3. Форматируем ответ для паспорта компетенций
            response_data = {
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'admission': plan_data.get('admission', {}),
                'planlines': plan_data.get('planlines', {}),
                'caf_name': plan_data.get('planlines', {}).get('caf_name', 'Не указано'),
                'plx_file': plan_data.get('plx_file', ''),
            }
            
            return Response(response_data)
            
        except Exception as e:
            #logger.error(f"Error fetching plan details for plan {plan_id}: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Ошибка при получении данных плана: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-relations')
    def get_competence_relations(self, request):
        """Получение связей компетенции с другими компетенциями"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            if not plan_id or not competence_index:
                return Response(
                    {'error': 'ID плана и индекс компетенции обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response

            competence_exists = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).exists()
            
            if not competence_exists:
                return Response(
                    {'error': 'Компетенция не найдена в плане'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            competence_data = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            # Получаем или создаем запись о связях
            relations, created = CompetenceRelations.objects.get_or_create(
                plan=plan,
                competence_index=competence_index,
                defaults={
                    'competence': competence_data.competence if competence_data else competence_index,
                    'relations': ''
                }
            )
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': competence_index,
                'competence': relations.competence or (competence_data.competence if competence_data else ''),
                'relations': relations.relations or '',
                'created': created
            })
            
        except Exception as e:
            #logger.error(f"Error fetching competence relations: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении связей компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='update-competence-relations')
    def update_competence_relations(self, request):
        """Обновление связей компетенции с другими компетенциями"""
        try:
            plan_id = request.data.get('plan_id')
            competence_index = request.data.get('competence_index')
            relations_text = request.data.get('relations_text', '')
            
            if not plan_id or not competence_index:
                return Response(
                    {'error': 'ID плана и индекс компетенции обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response

            competence_data = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            if not competence_data:
                return Response(
                    {'error': 'Компетенция не найдена в плане'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            
            with transaction.atomic():
                relations, created = CompetenceRelations.objects.update_or_create(
                    plan=plan,
                    competence_index=competence_index,
                    defaults={
                        'competence': competence_data.competence,
                        'relations': relations_text
                    }
                )
                
                return Response({
                    'success': True,
                    'message': 'Связи компетенции успешно обновлены',
                    'competence_index': competence_index,
                    'relations': relations_text,
                    'created': created,
                    'updated_at': relations.updated_at
                })
                
        except Exception as e:
            #logger.error(f"Error updating competence relations: {str(e)}")
            return Response(
                {'error': f'Ошибка при обновлении связей компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['GET'], detail=False, url_path='competence-final-indicators')
    def get_competence_final_indicators(self, request):
        """Получение итоговых индикаторов достижения компетенции"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            if not plan_id or not competence_index:
                return Response(
                    {'error': 'ID плана и индекс компетенции обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response

            all_indicators = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).order_by('indicator_index')
            
            # Ищем итоговый индикатор (содержит "Итоговый индикатор" в индексе)
            final_indicators = []
            other_indicators = []
            
            for indicator in all_indicators:
                indicator_data = {
                    'id': indicator.id,
                    'indicator_index': indicator.indicator_index,
                    'indicator': indicator.indicator,
                    'discipline_id': indicator.planlineid.id,
                    'discipline_index': indicator.planlineid.newdisid,
                    'discipline_name': indicator.planlineid.dis,
                    'is_final': 'Итоговый индикатор' in indicator.indicator_index
                }
                
                if indicator_data['is_final']:
                    final_indicators.append(indicator_data)
                else:
                    other_indicators.append(indicator_data)
            
            # Если нет итоговых индикаторов, берем первый доступный как основной
            primary_indicator = None
            if final_indicators:
                primary_indicator = final_indicators[0]
            elif other_indicators:
                primary_indicator = other_indicators[0]
            
            competence_data = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': competence_index,
                'competence': competence_data.competence if competence_data else '',
                'primary_indicator': primary_indicator,
                'all_indicators': final_indicators + other_indicators,
                'final_indicators_count': len(final_indicators),
                'total_indicators_count': len(all_indicators)
            })
            
        except Exception as e:
            #logger.error(f"Error fetching competence final indicators: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении итоговых индикаторов компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='update-competence-final-indicators')
    def update_competence_final_indicators(self, request):
        """Обновление итоговых индикаторов компетенции"""
        try:
            plan_id = request.data.get('plan_id')
            competence_index = request.data.get('competence_index')
            final_indicator_text = request.data.get('final_indicator_text', '')
            indicator_id = request.data.get('indicator_id') 
            
            if not plan_id or not competence_index:
                return Response(
                    {'error': 'ID плана и индекс компетенции обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response

            with transaction.atomic():
                competence_exists = LinesIndicators.objects.filter(
                    planlineid__plan=plan,
                    competence_index=competence_index
                ).exists()
                
                if not competence_exists:
                    return Response(
                        {'error': 'Компетенция не найдена в плане'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                if indicator_id:
                    try:
                        indicator = LinesIndicators.objects.get(
                            id=indicator_id,
                            planlineid__plan=plan,
                            competence_index=competence_index
                        )
                        indicator.indicator = final_indicator_text
                        indicator.save()
                        
                        return Response({
                            'success': True,
                            'message': f'Итоговый индикатор "{indicator.indicator_index}" успешно обновлен',
                            'indicator_id': indicator.id,
                            'indicator_index': indicator.indicator_index,
                            'updated': True
                        })
                        
                    except LinesIndicators.DoesNotExist:
                        return Response(
                            {'error': 'Указанный индикатор не найден'}, 
                            status=status.HTTP_404_NOT_FOUND
                        )
                
                # Если indicator_id не передан, ищем итоговый индикатор
                final_indicators = LinesIndicators.objects.filter(
                    planlineid__plan=plan,
                    competence_index=competence_index,
                    indicator_index__icontains='Итоговый индикатор'
                ).order_by('indicator_index')
                
                if final_indicators.exists():
                    indicator = final_indicators.first()
                    indicator.indicator = final_indicator_text
                    indicator.save()
                    
                    return Response({
                        'success': True,
                        'message': f'Итоговый индикатор "{indicator.indicator_index}" успешно обновлен',
                        'indicator_id': indicator.id,
                        'indicator_index': indicator.indicator_index,
                        'updated': True
                    })

                first_indicator = LinesIndicators.objects.filter(
                    planlineid__plan=plan,
                    competence_index=competence_index
                ).first()
                
                if first_indicator:
                    new_indicator_index = f"{first_indicator.indicator_index} (Итоговый индикатор)"
                    
                    indicator = LinesIndicators.objects.create(
                        planlineid=first_indicator.planlineid,
                        competence_index=competence_index,
                        competence=first_indicator.competence,
                        indicator_index=new_indicator_index,
                        indicator=final_indicator_text
                    )
                    
                    return Response({
                        'success': True,
                        'message': f'Создан новый итоговый индикатор "{new_indicator_index}"',
                        'indicator_id': indicator.id,
                        'indicator_index': indicator.indicator_index,
                        'created': True
                    })

                return Response(
                    {'error': 'Для этой компетенции нет индикаторов в учебном плане'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                    
        except Exception as e:
            #logger.error(f"Error updating competence final indicators: {str(e)}")
            return Response(
                {'error': f'Ошибка при обновлении итоговых индикаторов: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-indicator-disciplines')
    def get_competence_indicator_disciplines(self, request):
        """Получение индикаторов компетенции с привязкой к дисциплинами"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            if not plan_id or not competence_index:
                return Response(
                    {'error': 'ID плана и индекс компетенции обязательны'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan, error_response = self._get_plan_or_error_response(plan_id)
            if error_response:
                return error_response

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
                'Б2.В'
            }
            groups_to_exclude_with_children = {
                'Б3',
                'ФТД', 
                'Б1.Б.05.02.ДВ.01'
            }
            
            # Получаем все индикаторы для этой компетенции с информацией о дисциплинах
            indicators = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).select_related('planlineid').order_by('indicator_index')
            
            # Фильтруем индикаторы: исключаем обобщающие группы и итоговые индикаторы
            filtered_indicators = []
            
            for indicator in indicators:
                is_final_indicator = 'Итоговый индикатор' in indicator.indicator_index

                if is_final_indicator:
                    continue

                discipline_index = indicator.planlineid.newdisid or ''
                should_exclude = False
                    
                if discipline_index:
                    if discipline_index in groups_to_exclude:
                        should_exclude = True

                    for group in groups_to_exclude_with_children:
                        if discipline_index.startswith(group + '.'): 
                            should_exclude = True
                            break
                        elif discipline_index == group: 
                            should_exclude = True
                            break
                    
                if should_exclude:
                    continue
                    
                filtered_indicators.append(indicator)
            
            # Формируем таблицу данных из отфильтрованных индикаторов
            table_data = []
            for indicator in filtered_indicators:
                table_data.append({
                    'id': indicator.id,
                    'indicator_index': indicator.indicator_index,
                    'indicator_content': indicator.indicator,
                    'discipline_index': indicator.planlineid.newdisid or '',
                    'discipline_name': indicator.planlineid.dis,
                    'discipline_id': indicator.planlineid.id,
                })
            
            competence_data = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': competence_index,
                'competence': competence_data.competence if competence_data else '',
                'table_data': table_data,
            })
            
        except Exception as e:
            #logger.error(f"Error fetching competence indicator disciplines: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении индикаторов с дисциплинами: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['POST'], detail=False, url_path='update-indicator-content')
    def update_indicator_content(self, request):
        """Обновление содержания индикатора"""
        try:
            indicator_id = request.data.get('indicator_id')
            new_content = request.data.get('indicator_content', '').strip()
            
            if not indicator_id:
                return Response(
                    {'error': 'ID индикатора обязателен'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                try:
                    indicator = LinesIndicators.objects.get(id=indicator_id)

                    indicator.indicator = new_content
                    indicator.save()
                    
                    plan = indicator.planlineid.plan
                    
                    return Response({
                        'success': True,
                        'message': 'Содержание индикатора успешно обновлено',
                        'indicator': {
                            'id': indicator.id,
                            'indicator_index': indicator.indicator_index,
                            'indicator_content': indicator.indicator,
                            'competence_index': indicator.competence_index,
                            'discipline_id': indicator.planlineid.id,
                            'discipline_name': indicator.planlineid.dis,
                            'discipline_index': indicator.planlineid.newdisid,
                        },
                        'plan_id': plan.id,
                        'plan_mira_id': plan.mira_id,
                        'plan_name': plan.planname
                    })
                    
                except LinesIndicators.DoesNotExist:
                    return Response(
                        {'error': 'Индикатор не найден'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                    
        except Exception as e:
            #logger.error(f"Error updating indicator content: {str(e)}")
            return Response(
                {'error': f'Ошибка при обновлении содержания индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='indicator-details')
    def get_indicator_details(self, request):
        """Получение деталей индикатора (знать/уметь/владеть)"""
        try:
            indicator_id = self.request.query_params.get('indicator_id')
            
            if not indicator_id:
                return Response(
                    {'error': 'ID индикатора обязателен'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                indicator = LinesIndicators.objects.get(id=indicator_id)
            except LinesIndicators.DoesNotExist:
                return Response(
                    {'error': 'Индикатор не найден'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            discipline_indicator = DisciplineIndicators.objects.filter(
                indicator=indicator
            ).first()
            
            if discipline_indicator:
                response_data = {
                    'know': discipline_indicator.know or '',
                    'able': discipline_indicator.able or '',
                    'own': discipline_indicator.own or '',
                    'criteria': discipline_indicator.criteria or '',
                    'methods': discipline_indicator.methods or '',
                }
            else:
                response_data = {
                    'know': '',
                    'able': '',
                    'own': '',
                    'criteria': '',
                    'methods': '',
                }

            response_data.update({
                'indicator_id': indicator.id,
                'indicator_index': indicator.indicator_index,
                'indicator_content': indicator.indicator,
                'competence_index': indicator.competence_index,
                'discipline_id': indicator.planlineid.id,
                'discipline_name': indicator.planlineid.dis,
                'discipline_index': indicator.planlineid.newdisid,
            })
            
            return Response(response_data)
            
        except Exception as e:
            #logger.error(f"Error fetching indicator details: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении деталей индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='save-indicator-details')
    def save_indicator_details(self, request):
        """Сохранение деталей индикатора (знать/уметь/владеть)"""
        try:
            indicator_id = request.data.get('indicator_id')
            know = request.data.get('know', '')
            able = request.data.get('able', '')
            own = request.data.get('own', '')
            criteria = request.data.get('criteria', '')
            methods = request.data.get('methods', '')
            
            if not indicator_id:
                return Response(
                    {'error': 'ID индикатора обязателен'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                try:
                    indicator = LinesIndicators.objects.get(id=indicator_id)
                except LinesIndicators.DoesNotExist:
                    return Response(
                        {'error': 'Индикатор не найден'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

                discipline_indicator, created = DisciplineIndicators.objects.update_or_create(
                    indicator=indicator,
                    defaults={
                        'planlineid': indicator.planlineid,
                        'know': know,
                        'able': able,
                        'own': own,
                        'criteria': criteria,
                        'methods': methods
                    }
                )
                
                return Response({
                    'success': True,
                    'message': 'Данные индикатора успешно сохранены',
                    'created': created,
                    'indicator': {
                        'id': indicator.id,
                        'indicator_index': indicator.indicator_index,
                        'indicator_content': indicator.indicator,
                        'competence_index': indicator.competence_index,
                        'know': discipline_indicator.know,
                        'able': discipline_indicator.able,
                        'own': discipline_indicator.own,
                        'criteria': discipline_indicator.criteria,
                        'methods': discipline_indicator.methods,
                        'updated_at': discipline_indicator.updated_at
                    }
                })
                
        except Exception as e:
            #logger.error(f"Error saving indicator details: {str(e)}")
            return Response(
                {'error': f'Ошибка при сохранении данных индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )