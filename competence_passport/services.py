import re
import logging
from django.conf import settings
from django.db import transaction
from django.db.models import Prefetch, Max
from django.db.models.functions import Lower
from app.disable_mira_dumps import DATA_GROUP_LIST, DATA_GROUPS_PROGRAM
from generator.services.generator_service import GeneratorService
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators, SemesterData
from competence_passport.models import Scheme, CompetenceRelations
from generator.models import DisciplineIndicators, PlanLinesLink
from datetime import datetime
logger = logging.getLogger(__name__)


class CompetencePassportService:
    """Сервис для работы с схемой, матрицей и паспортом компетенций"""
    
    # Группы для исключения
    GROUPS_TO_EXCLUDE = {
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
    
    GROUPS_TO_EXCLUDE_WITH_CHILDREN = {
        'Б3',
        'ФТД', 
        'Б1.Б.05.02.ДВ.01'
    }
    
    GROUP_NAMES = {
        'Б1': 'Дисциплины (модули)',
        'Б1.Б': 'Обязательная часть',
        'Б1.Б.01': 'Общеобразовательный модуль',
        'Б1.Б.02': 'Фундаментальный модуль',
        'Б1.Б.03': 'Базовый модуль направления',
        'Б1.Б.04': 'Модуль проектной деятельности',
        'Б1.Б.05': 'Модуль по физической культуре и спорту',
        'Б1.Б.05.02.ДВ.01': 'Дисциплины по выбору',
        'Б1.В': 'Вариативная часть',
        'Б1.В.01': 'Модуль проектной деятельности',
        'Б1.В.02': 'Модуль профильной подготовки',
        'Б1.В.02.ДВ.01': 'Дисциплины по выбору Б1.В.ДВ.1',
        'Б1.В.02.ДВ.02': 'Дисциплины по выбору Б1.В.ДВ.2',
        'Б1.В.03': 'Модуль дополнительного профиля',
        'Б2': 'Практика',
        'Б2.Б': 'Обязательная часть',
        'Б2.В': 'Вариативная часть',
        'Б3': 'Государственная итоговая аттестация',
        'ФТД': 'Факультативы'
    }
    
    @staticmethod
    def get_plan_or_error_response(plan_id):
        """Получение плана"""
        try:
            return PlanData.objects.get(mira_id=plan_id), None
        except PlanData.DoesNotExist:
            return None, {
                'error': 'Учебный план не найден в базе данных',
                'status': 404
            }

    @staticmethod
    def get_discipline_or_error_response(plan, discipline_id):
        """Получение дисциплины"""
        try:
            return LinesData.objects.get(id=discipline_id, plan=plan), None
        except LinesData.DoesNotExist:
            return None, {
                'error': 'Дисциплина не найдена',
                'status': 404
            }

    @staticmethod
    def get_all_competences_for_plan(plan):
        """Получение всех уникальных компетенций для плана"""
        plan_lines = LinesData.objects.filter(plan=plan)
        
        competences = LinesIndicators.objects.filter(
            planlineid__in=plan_lines, 
            competence__isnull=False,
            competence_index__isnull=False
        ).values(
            'competence_index',
            'competence'
        ).distinct('competence_index')
        
        return list(competences)

    @staticmethod
    def get_distinct_lines_indicators(queryset=None, **filters):
        """Получение уникальных индикаторов"""
        if queryset is None:
            queryset = LinesIndicators.objects.all()
        
        if filters:
            queryset = queryset.filter(**filters)

        return queryset.order_by(
            'planlineid',
            'competence_index',
            'indicator_index',
            'indicator'
        ).distinct(
            'planlineid',
            'competence_index',
            'indicator_index'
        )

    @staticmethod
    def get_competence_type(competence_index):
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
        
    @classmethod
    def get_competence_by_index(cls, plan, competence_index):
        """Получение названия компетенции по индексу"""
        try:
            indicator = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            return indicator.competence if indicator else competence_index
        except:
            return competence_index

    @staticmethod
    def extract_competence_parts(competence_index):
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

    @classmethod
    def sort_competences(cls, competences_list):
        """Сортировка списка компетенций по типу и индексу с числовой сортировкой"""
        def sort_key(item):
            competence_index = item.get('competence_index', '')
            
            prefix, sub_type, num1, num2, num3 = cls.extract_competence_parts(competence_index)
            
            # Сортируем по префиксу (УК, ОПК, ПК, ДК)
            prefix_order = {'УК': 1, 'ОПК': 2, 'ПК': 3, 'ДК': 4}
            prefix_priority = prefix_order.get(prefix.upper(), 5)

            return (prefix_priority, num1, num2, num3)
        
        return sorted(competences_list, key=sort_key)

    @classmethod
    def update_kompetences_cache(cls, discipline):
        """Обновляет поле kompetences в LinesData"""
        # Получаем все индикаторы дисциплины
        indicators = cls.get_distinct_lines_indicators(
            planlineid=discipline,
            competence_index__isnull=False
        ).order_by('indicator_index')
        
        if indicators.exists():
            # Формируем строку уникальных индикаторов через запятую
            seen_indices = set()
            indicator_list = []
            for ind in indicators:
                if ind.indicator_index not in seen_indices:
                    seen_indices.add(ind.indicator_index)
                    indicator_list.append(ind.indicator_index)
            kompetences_str = ",".join(indicator_list)
        else:
            kompetences_str = ""
        
        discipline.kompetences = kompetences_str
        discipline.save(update_fields=['kompetences'])

    @staticmethod
    def get_plan_response_data(plan, additional_data=None):
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

    @staticmethod
    def validate_plan_id(plan_id):
        """Валидация ID плана"""
        if not plan_id:
            return {
                'error': 'ID плана не указан',
                'status': 400
            }
        return None

    @classmethod
    def sort_competence_list(cls, competence_list):
        """Сортировка списка индексов компетенций"""
        if isinstance(competence_list, set):
            competence_list = list(competence_list)
        
        temp_items = [{'competence_index': comp} for comp in competence_list]
        sorted_items = cls.sort_competences(temp_items)
        
        return [item['competence_index'] for item in sorted_items]

    @staticmethod
    def get_group_list(user_mira_id, year_filter, txt_filter, group_txt_filter, status_filter, my_filter):
        """Получение списка групп"""
        if settings.DISABLE_MIRA:
            return DATA_GROUP_LIST
        else:
            return GeneratorService.get_group_list(
                user_mira_id, 
                year_filter, 
                txt_filter,
                group_txt_filter, 
                status_filter, 
                my_filter
            )

    @classmethod
    def get_all_disciplines_for_plan(cls, plan_id):
        """Получение всех дисциплин для конкретного учебного плана"""
        error_response = cls.validate_plan_id(plan_id)
        if error_response:
            return None, error_response
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response 
        
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

            if disc_newdisid in cls.GROUPS_TO_EXCLUDE:
                should_exclude = True
            if disc_newdisid in cls.GROUPS_TO_EXCLUDE_WITH_CHILDREN:
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
        
        return plan, disciplines_list, None

    @classmethod
    def get_competence_matrix(cls, plan_id):
        """Получение матрицы компетенций для конкретного учебного плана"""
        error_response = cls.validate_plan_id(plan_id)
        if error_response:
            return None, error_response
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        # Получаем все дисциплины плана
        disciplines = LinesData.objects.filter(
            plan=plan
        ).prefetch_related(
            Prefetch(
                'indicators',
                queryset=LinesIndicators.objects.filter(
                    competence__isnull=False,
                    competence_index__isnull=False
                ).only('competence_index', 'competence').distinct('competence_index', 'planlineid')
            )
        ).order_by('newdisid')

        groups = {}
        
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
                # Проверяем, является ли этот индекс группой
                if disc_key in cls.GROUP_NAMES:
                    groups[disc_key] = {
                        'type': 'group',
                        'index': disc_key,
                        'name': cls.GROUP_NAMES[disc_key],
                        'competences': discipline_competences,
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }
                else:
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
                        'name': cls.GROUP_NAMES.get(base_group_key, base_group_key),
                        'competences': set(),
                        'level': base_group_key.count('.') + 1 if '.' in base_group_key else 1
                    }
                groups[base_group_key]['competences'].update(discipline_competences)
        
        matrix_data = []
        for item in groups.values():
            sorted_competences = cls.sort_competence_list(item['competences'])
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
        
        return plan, matrix_data, None

    @classmethod
    def get_discipline_competences_detailed(cls, plan_id, discipline_id):
        """Детальная информация о компетенциях дисциплины с индикаторами"""
        if not plan_id or not discipline_id:
            return None, {
                'error': 'ID плана и дисциплины обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        discipline, error_response = cls.get_discipline_or_error_response(plan, discipline_id)
        if error_response:
            return None, error_response
        
        all_competences = cls.get_all_competences_for_plan(plan)
        sorted_competences = cls.sort_competences(all_competences)
        
        discipline_indicators = cls.get_distinct_lines_indicators(
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
                'type': cls.get_competence_type(comp_index),
                'indicators_count': current_competences.get(comp_index, {}).get('indicators_count', 0),
                'indicators': current_competences.get(comp_index, {}).get('indicators', [])
            })
        
        return {
            'plan': plan,
            'discipline': discipline,
            'competences_list': competences_list
        }, None

    @classmethod
    def update_discipline_competences(cls, plan_id, discipline_id, selected_competences):
        """Обновление компетенций для дисциплины с выбранными компетенциями"""
        if not plan_id or not discipline_id:
            return None, {
                'error': 'ID плана и дисциплины обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        discipline, error_response = cls.get_discipline_or_error_response(plan, discipline_id)
        if error_response:
            return None, error_response
        
        with transaction.atomic():
            # Получаем текущие компетенции дисциплины
            current_indicators = cls.get_distinct_lines_indicators(
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
            
            # 1. Удаляем компетенции, которые не выбраны
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
                
                # Получаем существующие индикаторы
                existing_indicators = cls.get_distinct_lines_indicators(
                    planlineid=discipline,
                    competence_index=comp_index
                ).exclude(
                    indicator_index__icontains='Итоговый индикатор'
                ).order_by('indicator_index')
                
                # Определяем следующий доступный номер индикатора
                last_indicator_index = 0
                if existing_indicators.exists():
                    last_indicator = existing_indicators.last()
                    if last_indicator and last_indicator.indicator_index:
                        match = re.search(r'\d+', last_indicator.indicator_index)
                        if match:
                            last_indicator_index = int(match.group())
                
                new_index_number = last_indicator_index + 1
                base_comp_index = comp_index.replace(' ', '-')
                indicator_index = f"{base_comp_index}.{new_index_number}"
                с
                while LinesIndicators.objects.filter(
                    planlineid=discipline,
                    competence_index=comp_index,
                    indicator_index=indicator_index
                ).exists():
                    new_index_number += 1
                    indicator_index = f"{base_comp_index}.{new_index_number}"
                
                # Создаем один индикатор
                indicator = LinesIndicators(
                    planlineid=discipline,
                    competence_index=comp_index,
                    competence=competence_name,
                    indicator_index=indicator_index, 
                    indicator=''  
                )
                indicator.save()
                added_count += 1
            
            # 3. Считаем компетенции, которые остались без изменений
            for comp_index in comp_to_keep:
                kept_count += len(current_competences[comp_index])
            
            # Обновляем кэш компетенций дисциплины
            cls.update_kompetences_cache(discipline)
            
            comp_to_delete_sorted = cls.sort_competence_list(comp_to_delete)
            comp_to_add_sorted = cls.sort_competence_list(comp_to_add)
            comp_to_keep_sorted = cls.sort_competence_list(comp_to_keep)
            
            return {
                'discipline': discipline,
                'comp_to_delete_sorted': comp_to_delete_sorted,
                'comp_to_add_sorted': comp_to_add_sorted,
                'comp_to_keep_sorted': comp_to_keep_sorted
            }, None

    @classmethod
    def update_semester_scheme(cls, plan_id, discipline_id, competence_index, semester, forms):
        """Обновление схемы формы аттестации для компетенции в семестре"""
        if not all([plan_id, discipline_id, competence_index, semester]):
            return None, {
                'error': 'Все обязательные поля должны быть заполнены',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        discipline, error_response = cls.get_discipline_or_error_response(plan, discipline_id)
        if error_response:
            return None, error_response
        
        forms_converted = {}
        for key in ['ekz', 'zach', 'zacho', 'kp', 'kr']:
            value = forms.get(key, False)
            forms_converted[key] = bool(value)
        
        has_any_form = any(forms_converted.values())
        
        with transaction.atomic():
            competence_exists = cls.get_distinct_lines_indicators(
                planlineid=discipline,
                competence_index=competence_index
            ).exists()
            
            if not competence_exists:
                return None, {
                    'error': 'Компетенция не привязана к данной дисциплине',
                    'status': 400
                }
            
            semester_exists = SemesterData.objects.filter(
                planlineid=discipline,
                num=semester
            ).exists()
            
            if not semester_exists:
                return None, {
                    'error': 'Указанный семестр не существует для данной дисциплины',
                    'status': 400
                }
            
            semester_data = SemesterData.objects.filter(
                planlineid=discipline,
                num=semester
            ).first()
            
            # Проверяем, чтобы пользователь не мог выбрать формы, которые недоступны по учебному плану
            unavailable_forms = []
            
            if semester_data:
                if forms_converted['ekz'] and not semester_data.ekz:
                    unavailable_forms.append('ekz')
                if forms_converted['zach'] and not semester_data.zach:
                    unavailable_forms.append('zach')
                if forms_converted['zacho'] and not semester_data.zacho:
                    unavailable_forms.append('zacho')
                if forms_converted['kp'] and not semester_data.kp:
                    unavailable_forms.append('kp')
                if forms_converted['kr'] and not semester_data.kr:
                    unavailable_forms.append('kr')

            if unavailable_forms:
                return None, {
                    'error': 'Указанная форма аттестации не доступна для данной дисциплины в данном семестре',
                    'status': 400
                }
            
            competence_name = None
            competence_obj = cls.get_distinct_lines_indicators(
                planlineid=discipline,
                competence_index=competence_index
            ).first()
            competence_name = competence_obj.competence if competence_obj else competence_index
            
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
            
            return {
                'scheme_id': scheme_id,
                'created': created,
                'forms_display': ', '.join(forms_display) if forms_display else '',
                'has_forms': has_any_form
            }, None

    @classmethod
    def get_competence_schema_data(cls, plan_id):
        """Получение данных для схемы компетенций с формами аттестации"""
        error_response = cls.validate_plan_id(plan_id)
        if error_response:
            return None, error_response
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        all_competences = cls.get_all_competences_for_plan(plan)
        competences = cls.sort_competences(all_competences)
        
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
                queryset=cls.get_distinct_lines_indicators(
                    competence__isnull=False,
                    competence_index__isnull=False
                )
            ),
            Prefetch(
                'competence_schemes',
                queryset=Scheme.objects.all()
            )
        ).order_by('newdisid')
        
        schema_rows = []
        
        for comp in competences:
            comp_index = comp['competence_index']
            comp_name = comp['competence']
            comp_type = cls.get_competence_type(comp_index)
            
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
                    if disc_newdisid in cls.GROUPS_TO_EXCLUDE:
                        should_exclude = True

                    for group in cls.GROUPS_TO_EXCLUDE_WITH_CHILDREN:
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
        
        return plan, {'schema_rows': schema_rows}, None

    @staticmethod
    def get_plan_details(plan_id, user_mira_id):
        """Получение детальной информации о плане для титульного листа"""
        error_response = CompetencePassportService.validate_plan_id(plan_id)
        if error_response:
            return None, error_response
        
        plan, error_response = CompetencePassportService.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        # 1. Находим PlanLinesLink для этого плана
        first_discipline = LinesData.objects.filter(plan=plan).first()
        if not first_discipline:
            return None, {
                'error': 'В плане нет дисциплин',
                'status': 404
            }

        plan_lines_link = PlanLinesLink.objects.filter(
            planlines=first_discipline
        ).first()
        
        # 2. Получаем данные 
        plan_data = GeneratorService.get_rpd_data(plan_lines_link.id, user_mira_id)
        
        # 3. Форматируем ответ для паспорта компетенций
        response_data = {
            'plan': plan,
            'plan_data': {
                'admission': plan_data.get('admission', {}),
                'planlines': plan_data.get('planlines', {}),
                'caf_name': plan_data.get('planlines', {}).get('caf_name', 'Не указано'),
                'plx_file': plan_data.get('plx_file', ''),
            }
        }
        
        return response_data, None

    @classmethod
    def get_competence_relations(cls, plan_id, competence_index):
        """Получение связей компетенции с другими компетенциями"""
        if not plan_id or not competence_index:
            return None, {
                'error': 'ID плана и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = CompetencePassportService.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response

        competence_exists = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index=competence_index
        ).exists()
        
        if not competence_exists:
            return None, {
                'error': 'Компетенция не найдена в плане',
                'status': 404
            }

        competence_data = cls.get_distinct_lines_indicators(
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
        
        return {
            'plan': plan,
            'competence_index': competence_index,
            'competence': relations.competence or (competence_data.competence if competence_data else ''),
            'relations': relations.relations or '',
            'created': created
        }, None

    @classmethod
    def update_competence_relations(cls, plan_id, competence_index, relations_text):
        """Обновление связей компетенции с другими компетенциями"""
        if not plan_id or not competence_index:
            return None, {
                'error': 'ID плана и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response

        competence_data = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index=competence_index
        ).first()
        
        if not competence_data:
            return None, {
                'error': 'Компетенция не найдена в плане',
                'status': 404
            }
        
        
        with transaction.atomic():
            relations, created = CompetenceRelations.objects.update_or_create(
                plan=plan,
                competence_index=competence_index,
                defaults={
                    'competence': competence_data.competence,
                    'relations': relations_text
                }
            )
            
            return {
                'competence_index': competence_index,
                'relations': relations_text,
                'created': created,
                'updated_at': relations.updated_at
            }, None

    @classmethod
    def get_competence_final_indicators(cls, plan_id, competence_index):
        """Получение итоговых индикаторов достижения компетенции"""
        if not plan_id or not competence_index:
            return None, {
                'error': 'ID плана и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response

        all_indicators = cls.get_distinct_lines_indicators(
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
        
        competence_data = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index=competence_index
        ).first()
        
        return {
            'plan': plan,
            'competence_index': competence_index,
            'competence': competence_data.competence if competence_data else '',
            'primary_indicator': primary_indicator,
            'all_indicators': final_indicators + other_indicators,
            'final_indicators_count': len(final_indicators),
            'total_indicators_count': len(all_indicators)
        }, None

    @classmethod
    def update_competence_final_indicators(cls, plan_id, competence_index, final_indicator_text, indicator_id=None):
        """Обновление итоговых индикаторов компетенции"""
        if not plan_id or not competence_index:
            return None, {
                'error': 'ID плана и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response

        with transaction.atomic():
            competence_exists = cls.get_distinct_lines_indicators(
                planlineid__plan=plan,
                competence_index=competence_index
            ).exists()
            
            if not competence_exists:
                return None, {
                    'error': 'Компетенция не найдена в плане',
                    'status': 404
                }
            
            if indicator_id:
                try:
                    indicator = LinesIndicators.objects.get(
                        id=indicator_id,
                        planlineid__plan=plan,
                        competence_index=competence_index
                    )
                    indicator.indicator = final_indicator_text
                    indicator.save()
                    
                    return {
                        'indicator': indicator,
                        'updated': True,
                        'created': False
                    }, None
                    
                except LinesIndicators.DoesNotExist:
                    return None, {
                        'error': 'Указанный индикатор не найден',
                        'status': 404
                    }
            
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
                
                return {
                    'indicator': indicator,
                    'updated': True,
                    'created': False
                }, None

            first_indicator = cls.get_distinct_lines_indicators(
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
                
                return {
                    'indicator': indicator,
                    'updated': False,
                    'created': True
                }, None

            return None, {
                'error': 'Для этой компетенции нет индикаторов в учебном плане',
                'status': 404
            }

    @classmethod
    def get_competence_indicator_disciplines(cls, plan_id, competence_index):
        """Получение индикаторов компетенции с привязкой к дисциплинами"""
        if not plan_id or not competence_index:
            return None, {
                'error': 'ID плана и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        # Получаем все индикаторы для этой компетенции с информацией о дисциплинах
        indicators = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index=competence_index
        ).select_related('planlineid').order_by('indicator_index')
        
        # Фильтруем индикаторы
        filtered_indicators = []
        
        for indicator in indicators:
            is_final_indicator = 'Итоговый индикатор' in indicator.indicator_index

            if is_final_indicator:
                continue

            discipline_index = indicator.planlineid.newdisid or ''
            should_exclude = False
                
            if discipline_index:
                if discipline_index in cls.GROUPS_TO_EXCLUDE:
                    should_exclude = True

                for group in cls.GROUPS_TO_EXCLUDE_WITH_CHILDREN:
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
        
        competence_data = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index=competence_index
        ).first()
        
        return {
            'plan': plan,
            'competence_index': competence_index,
            'competence': competence_data.competence if competence_data else '',
            'table_data': table_data,
        }, None

    @staticmethod
    def update_indicator_content(indicator_id, new_content):
        """Обновление содержания индикатора"""
        if not indicator_id:
            return None, {
                'error': 'ID индикатора обязателен',
                'status': 400
            }
        
        with transaction.atomic():
            try:
                indicator = LinesIndicators.objects.get(id=indicator_id)

                indicator.indicator = new_content
                indicator.save()
                
                plan = indicator.planlineid.plan
                
                return {
                    'indicator': indicator,
                    'plan': plan
                }, None
                
            except LinesIndicators.DoesNotExist:
                return None, {
                    'error': 'Индикатор не найден',
                    'status': 404
                }

    @staticmethod
    def get_indicator_details(indicator_id):
        """Получение деталей индикатора (знать/уметь/владеть)"""
        if not indicator_id:
            return None, {
                'error': 'ID индикатора обязателен',
                'status': 400
            }
        
        try:
            indicator = LinesIndicators.objects.get(id=indicator_id)
        except LinesIndicators.DoesNotExist:
            return None, {
                'error': 'Индикатор не найден',
                'status': 404
            }
        
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
            'indicator': indicator
        })
        
        return response_data, None

    @staticmethod
    def save_indicator_details(indicator_id, know, able, own, criteria, methods):
        """Сохранение деталей индикатора (знать/уметь/владеть)"""
        if not indicator_id:
            return None, {
                'error': 'ID индикатора обязателен',
                'status': 400
            }
        
        with transaction.atomic():
            try:
                indicator = LinesIndicators.objects.get(id=indicator_id)
            except LinesIndicators.DoesNotExist:
                return None, {
                    'error': 'Индикатор не найден',
                    'status': 404
                }

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
            
            return {
                'discipline_indicator': discipline_indicator,
                'indicator': indicator,
                'created': created
            }, None
        
    @classmethod
    def validate_scheme_indicators(cls, plan_id):
        """Проверка соответствия числа промежуточных аттестаций и индикаторов"""
        error_response = cls.validate_plan_id(plan_id)
        if error_response:
            return None, error_response
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        schemes = Scheme.objects.filter(
            planlineid__plan=plan
        ).select_related('planlineid').order_by(
            'competence_index', 'planlineid__newdisid', 'semester'
        )
        
        indicators = cls.get_distinct_lines_indicators(
            planlineid__plan=plan,
            competence_index__isnull=False
        ).select_related('planlineid').exclude(
            indicator_index__icontains='Итоговый индикатор'
        )
        
        # Группируем по компетенции и дисциплине
        indicators_by_competence_discipline = {}
        for indicator in indicators:
            key = (indicator.competence_index, indicator.planlineid.id)
            if key not in indicators_by_competence_discipline:
                indicators_by_competence_discipline[key] = []
            indicators_by_competence_discipline[key].append(indicator)

        schemes_by_competence_discipline = {}
        for scheme in schemes:
            key = (scheme.competence_index, scheme.planlineid.id)
            if key not in schemes_by_competence_discipline:
                schemes_by_competence_discipline[key] = []
            schemes_by_competence_discipline[key].append(scheme)
        
        # Проверяем схемы на соответствие
        validation_errors = []
        
        for scheme in schemes:
            competence_index = scheme.competence_index
            discipline = scheme.planlineid

            should_exclude = False
            if discipline.newdisid:
                if discipline.newdisid in cls.GROUPS_TO_EXCLUDE:
                    should_exclude = True
                
                for group in cls.GROUPS_TO_EXCLUDE_WITH_CHILDREN:
                    if discipline.newdisid.startswith(group + '.'):
                        should_exclude = True
                        break
                    elif discipline.newdisid == group:
                        should_exclude = True
                        break
            
            if should_exclude:
                continue
            
            # Получаем схемы и индикаторы для этой компетенции и дисциплины
            key = (competence_index, discipline.id)
            discipline_indicators = indicators_by_competence_discipline.get(key, [])
            discipline_scheme = schemes_by_competence_discipline.get(key, [])

            forms_count = len(discipline_scheme)
            indicators_count = len(discipline_indicators)
            
            if forms_count != indicators_count:
                error_id = f"{competence_index}_{discipline.id}_{scheme.semester}"
                competence_name = scheme.competence or cls.get_competence_by_index(plan, competence_index)
                
                if forms_count > 0 and indicators_count == 0:
                    error_type = 'missing_indicators'
                    message = f'Указаны формы аттестации, но отсутствуют индикаторы'
                    advice = 'Добавьте индикаторы формирования компетенции в паспорте компетенций для этой дисциплины'
                elif forms_count == 0 and indicators_count > 0:
                    error_type = 'missing_forms'
                    message = f'ДУказаны индикаторы, но отсутствуют формы аттестации'
                    advice = 'Добавьте формы аттестации в схеме компетенций для этого семестра'
                else:
                    error_type = 'forms_mismatch'
                    message = f'Не совпадает число форм аттестации ({forms_count}) и индикаторов ({indicators_count})'
                    advice = 'Скорректируйте либо число форм аттестации в схеме, либо число индикаторов в паспорте компетенций'
                
                validation_errors.append({
                    'id': error_id,
                    'competence_index': competence_index,
                    'competence_name': competence_name,
                    'discipline_index': discipline.newdisid or '',
                    'discipline_name': discipline.dis,
                    'discipline_id': discipline.id,
                    'scheme_forms_count': forms_count,
                    'indicators_count': indicators_count,
                    'semester': scheme.semester,
                    'error_type': error_type,
                    'message': message,
                    'advice': advice
                })
        
        temp_errors = {}
        for error in validation_errors:
            comp_index = error['competence_index']
            if comp_index not in temp_errors:
                temp_errors[comp_index] = []
            temp_errors[comp_index].append(error)
        
        # Сортируем компетенции
        sorted_competence_indices = cls.sort_competence_list(list(temp_errors.keys()))
        sorted_errors = []
        for comp_index in sorted_competence_indices:
            errors_for_competence = sorted(temp_errors[comp_index], 
                                        key=lambda x: (x['discipline_index'], x['semester']))
            sorted_errors.extend(errors_for_competence)
        
        return {
            'plan': plan,
            'validation_errors': sorted_errors,
            'has_errors': len(sorted_errors) > 0,
            'errors_count': len(sorted_errors),
            'checked_at': datetime.now().isoformat()
        }, None

    @classmethod
    def fix_scheme_indicators(cls, plan_id, discipline_id, competence_index, 
                            scheme_forms_count, indicators_count, semester):
        """Автоматическое исправление индикаторов - создание или удаление"""
        if not all([plan_id, discipline_id, competence_index]):
            return None, {
                'error': 'ID плана, дисциплины и индекс компетенции обязательны',
                'status': 400
            }
        
        plan, error_response = cls.get_plan_or_error_response(plan_id)
        if error_response:
            return None, error_response
        
        discipline, error_response = cls.get_discipline_or_error_response(plan, discipline_id)
        if error_response:
            return None, error_response
        
        with transaction.atomic():
            # Получаем существующие индикаторы 
            existing_indicators = cls.get_distinct_lines_indicators(
                planlineid=discipline,
                competence_index=competence_index
            ).exclude(
                indicator_index__icontains='Итоговый индикатор'
            ).order_by('indicator_index')

            competence_data = cls.get_distinct_lines_indicators(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            if not competence_data:
                return None, {
                    'error': 'Компетенция не найдена в плане',
                    'status': 404
                }
            
            current_indicators_count = existing_indicators.count()
            needed_count = scheme_forms_count
            
            indicators_created = 0
            indicators_removed = 0
            
            # Если нужно создать индикаторы (форм аттестации больше, чем индикаторов)
            if needed_count > current_indicators_count:
                indicators_to_create = needed_count - current_indicators_count
                
                # Определяем следующий доступный номер индикатора
                last_indicator_index = 0
                if current_indicators_count > 0:
                    last_indicator = existing_indicators.last()
                    if last_indicator and last_indicator.indicator_index:
                        match = re.search(r'\d+', last_indicator.indicator_index)
                        if match:
                            last_indicator_index = int(match.group())
                
                # Создаем недостающие индикаторы 
                for i in range(indicators_to_create):
                    new_index_number = last_indicator_index + i + 1
                    base_comp_index = competence_index.replace(' ', '-')
                    indicator_index = f"{base_comp_index}.{new_index_number}"
                    
                    while LinesIndicators.objects.filter(
                        planlineid=discipline,
                        competence_index=competence_index,
                        indicator_index=indicator_index
                    ).exists():
                        new_index_number += 1
                        indicator_index = f"{base_comp_index}.{new_index_number}"
                    
                    indicator = LinesIndicators.objects.create(
                        planlineid=discipline,
                        competence_index=competence_index,
                        competence=competence_data.competence,
                        indicator_index=indicator_index,
                        indicator=''
                    )
                    indicators_created += 1
            
            # Если нужно удалить индикаторы (форм аттестации меньше, чем индикаторов)
            elif needed_count < current_indicators_count:
                indicators_to_remove = current_indicators_count - needed_count

                indicators_to_delete = existing_indicators.order_by(
                    '-indicator_index' 
                )[:indicators_to_remove]
                
                for indicator in indicators_to_delete:
                    indicator.delete()
                    indicators_removed += 1
            
            cls.update_kompetences_cache(discipline)

            final_indicators = cls.get_distinct_lines_indicators(
                planlineid=discipline,
                competence_index=competence_index
            ).exclude(
                indicator_index__icontains='Итоговый индикатор'
            ).count()
            
            message_parts = []
            if indicators_created > 0:
                message_parts.append(f'создано {indicators_created} индикаторов')
            if indicators_removed > 0:
                message_parts.append(f'удалено {indicators_removed} индикаторов')
            if not message_parts:
                message_parts.append('количество индикаторов уже соответствует формам аттестации')
            
            return {
                'indicators_created': indicators_created,
                'indicators_removed': indicators_removed,
                'final_indicators_count': final_indicators,
                'message': 'Исправление выполнено: ' + ', '.join(message_parts)
            }, None