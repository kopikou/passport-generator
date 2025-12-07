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
import logging
logger = logging.getLogger(__name__)


class CompetencePassportViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]

    def get_queryset(self):
        return PlanData.objects.none()

    
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
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплины
            plan_lines = LinesData.objects.filter(plan=plan)
            
            # Получаем уникальные компетенции 
            competences = LinesIndicators.objects.filter(
                planlineid__in=plan_lines, 
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence'
            ).distinct().order_by('competence_index')
            
            competences_list = [
                {
                    'id': f"{comp['competence_index']}_{hash(comp['competence'])}",
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                }
                for comp in competences
            ]
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'competences': competences_list
            })
            
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
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплины БЕЗ фильтрации по synchronize
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
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'disciplines': disciplines_list
            })
            
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
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
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
                
                # Добавляем дисциплину в матрицу
                disc_key = discipline.newdisid
                if disc_key not in groups:
                    groups[disc_key] = {
                        'type': 'discipline',
                        'index': disc_key,
                        'name': discipline.dis,
                        'competences': discipline_competences,
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }
                
                # Добавляем компетенции ко всем родительским группам
                parts = disc_key.split('.')
                for i in range(len(parts)):
                    group_key = '.'.join(parts[:i+1])
                    
                    # Определяем базовую группу для ключа
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
                    
                    # Добавляем компетенции к группе
                    groups[base_group_key]['competences'].update(discipline_competences)
            
            matrix_data = []
            for item in groups.values():
                sorted_competences = sorted(list(item['competences']))
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
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'matrix': matrix_data
            })
            
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
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплину
            try:
                discipline = LinesData.objects.get(id=discipline_id, plan=plan)
            except LinesData.DoesNotExist:
                return Response(
                    {'error': 'Дисциплина не найдена'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем все доступные компетенции плана
            all_competences = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence'
            ).distinct().order_by('competence_index')
            
            # Получаем текущие компетенции дисциплины с группировкой
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
            for comp in all_competences:
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
            
            # Получаем план и дисциплину
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                discipline = LinesData.objects.get(id=discipline_id, plan=plan)
            except LinesData.DoesNotExist:
                return Response(
                    {'error': 'Дисциплина не найдена'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with transaction.atomic():
                # Получаем текущие компетенции дисциплины
                current_indicators = LinesIndicators.objects.filter(
                    planlineid=discipline
                )
                
                # Группируем текущие индикаторы по компетенциям
                current_competences = {}
                for indicator in current_indicators:
                    comp_index = indicator.competence_index
                    if comp_index not in current_competences:
                        current_competences[comp_index] = []
                    current_competences[comp_index].append(indicator)
                
                # Получаем индексы выбранных компетенций из запроса
                selected_comp_indices = [comp['competence_index'] for comp in selected_competences]
                
                # Компетенции для удаления (не выбраны в новом списке)
                comp_to_delete = set(current_competences.keys()) - set(selected_comp_indices)
                
                # Компетенции для добавления (новые в списке)
                comp_to_add = set(selected_comp_indices) - set(current_competences.keys())
                
                # Компетенции которые остаются (есть и в текущих, и в выбранных)
                comp_to_keep = set(current_competences.keys()) & set(selected_comp_indices)
                
                deleted_count = 0
                added_count = 0
                kept_count = 0
                
                # 1. УДАЛЯЕМ компетенции, которые не выбраны
                for comp_index in comp_to_delete:
                    deleted = LinesIndicators.objects.filter(
                        planlineid=discipline,
                        competence_index=comp_index
                    ).delete()
                    deleted_count += deleted[0]
                
                # 2. ДОБАВЛЯЕМ новые компетенции
                for comp_index in comp_to_add:
                    # Находим данные о новой компетенции в запросе
                    comp_data = next((c for c in selected_competences 
                                    if c['competence_index'] == comp_index), None)
                    if not comp_data:
                        continue
                    
                    competence_name = comp_data.get('competence')
                    indicators_data = comp_data.get('indicators', [])
                    
                    # Получаем исходное количество индикаторов для этой компетенции в других дисциплинах или используем количество из запроса, если есть
                    if indicators_data:
                        # Используем индикаторы из запроса
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
                        # Определяем номер для индикатора (максимальный + 1)
                        max_indicator = LinesIndicators.objects.filter(
                            planlineid__plan=plan,
                            competence_index=comp_index
                        ).aggregate(Max('indicator_index'))['indicator_index__max']
                        
                        if max_indicator:
                            # Извлекаем номер из индекса (например, "ПКС-4.3" -> 3)
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
                
                # 3. СЧИТАЕМ компетенции, которые остались без изменений
                for comp_index in comp_to_keep:
                    kept_count += len(current_competences[comp_index])
                
                self._update_kompetences_cache(discipline)
                
                return Response({
                    'success': True,
                    'message': f'Удалено {deleted_count} индикаторов, добавлено {added_count} индикаторов, сохранено {kept_count} индикаторов',
                    'deleted': deleted_count,
                    'added': added_count,
                    'kept': kept_count,
                    'total': deleted_count + added_count + kept_count,
                    'competences_deleted': list(comp_to_delete),
                    'competences_added': list(comp_to_add),
                    'competences_kept': list(comp_to_keep),
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
        
        # Обновляем дисциплину
        discipline.kompetences = kompetences_str
        discipline.save(update_fields=['kompetences'])
    
    def _get_default_competence_name(self, competence_index):
        """Возвращает название компетенции по умолчанию"""
        if 'УК' in competence_index:
            return f"Универсальная компетенция {competence_index}"
        elif 'ОПК' in competence_index:
            return f"Общепрофессиональная компетенция {competence_index}"
        elif 'ПК' in competence_index:
            return f"Профессиональная компетенция {competence_index}"
        elif 'ДК' in competence_index:
            return f"Дополнительная компетенция {competence_index}"
        else:
            return f"Компетенция {competence_index}"
    
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
        
    @action(methods=['GET'], detail=False, url_path='competence-schema-data')
    def get_competence_schema_data(self, request):
        """Получение данных для схемы компетенций с формами аттестации"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            all_competences = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence'
            ).distinct()
            
            competences_list = list(all_competences)
            
            def sort_competences(comp_list):
                def get_competence_type(competence_index):
                    if not competence_index:
                        return 'Другая'
                    
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
                
                type_order = {
                    'Универсальная': 1,
                    'Общепрофессиональная': 2,
                    'Профессиональная': 3,
                    'Дополнительная': 4,
                    'Другая': 5
                }
                
                return sorted(comp_list, key=lambda x: (
                    type_order.get(get_competence_type(x['competence_index']), 99),
                    x['competence_index']
                ))
            
            competences = sort_competences(competences_list)
            
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
                )
            ).order_by('newdisid')
            
            schema_rows = []
            
            for comp in competences:
                comp_index = comp['competence_index']
                comp_name = comp['competence']
                comp_type = self._get_competence_type(comp_index)
                
                schema_rows.append({
                    'type': 'competence',
                    'competence_index': comp_index,
                    'competence_name': comp_name,
                    'competence_type': comp_type
                })
                
                # Находим дисциплины, формирующие эту компетенцию
                discipline_rows = []
                for disc in disciplines:
                    has_competence = any(
                        indicator.competence_index == comp_index 
                        for indicator in disc.indicators.all()
                    )
                    
                    if has_competence:
                        semester_data = {}
                        
                        for sem in disc.semesters.all():
                            forms = []
                            if sem.ekz:  # Экзамен
                                forms.append('Э')
                            if sem.zach:  # Зачет
                                forms.append('З')
                            if sem.zacho and sem.zacho > 0:  # Зачет с оценкой
                                forms.append('Зо')
                            if sem.kp:  # Курсовой проект
                                forms.append('КП')
                            if sem.kr:  # Курсовая работа
                                forms.append('КР')
                            
                            if forms:
                                semester_data[f'semester_{sem.num}'] = ', '.join(forms)
                            else:
                                semester_data[f'semester_{sem.num}'] = ''
                        
                        # Заполняем все 8 семестров
                        full_semester_data = {}
                        for i in range(1, 9):
                            key = f'semester_{i}'
                            full_semester_data[key] = semester_data.get(key, '')
                        
                        discipline_rows.append({
                            'type': 'discipline',
                            'discipline_index': disc.newdisid or '',
                            'discipline_name': disc.dis,
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
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'schema_rows': schema_rows
            })
            
        except Exception as e:
            logger.error(f"Error fetching competence schema data for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении данных схемы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )