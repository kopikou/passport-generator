import re
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators, SemesterData
from competence_passport.models import Competence, Scheme
from collections import defaultdict

class RuleService:
    """Главный сервис для общих методов"""

    # Группы дисциплин для исключения (отображения/редактирования)
    DISCIPLINE_GROUPS_TO_EXCLUDE = {
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
        'Б1.В.02.ДВ.01': 'Дисциплины по выбору Б1.В.ДВ.1',
        'Б1.В.02.ДВ.02': 'Дисциплины по выбору Б1.В.ДВ.2',
        'Б1.В.03': 'Модуль дополнительного профиля',
        'Б2': 'Практика',
        'Б2.Б': 'Обязательная часть',
        'Б2.В': 'Вариативная часть',
    }
    
    # Группы дисциплин для исключения (отображения/редактирования) с вложенными дисциплинами
    DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN = { 
        'Б1.Б.05.02.ДВ.01': 'Дисциплины по выбору',
        'Б3': 'Государственная итоговая аттестация',
        'ФТД': 'Факультативы'
    }

    # Типы и порядок сортировки компетенций
    COMPETENSE_INFO = {
        'УК': {
            'name': 'Универсальная',
            'order': 1
        },
        'ОПК': {
            'name': 'Общепрофессиональная',
            'order': 2
        },
        'ПК': {
            'name': 'Профессиональная', 
            'order': 3
        },
        'ДК': {
            'name': 'Дополнительная',
            'order': 4
        },
        'Р': {
            'name': '?',
            'order': 5
        }
    }

    @classmethod
    def get_competence_type(cls,competence_index):
        """Тип компетенции по её индексу"""
        normalized = competence_index.strip()

        for prefix, info in cls.COMPETENSE_INFO.items():
            if normalized.startswith(prefix):
                return info['name']
        return ""

    @classmethod
    def sort_competences(cls, competences_data):
        """Сортировка компетенций"""
        def get_sort_key(comp_index):
            """Функция для получения ключа сортировки"""
            normalized = comp_index.strip()
            
            order = 999
            for prefix, info in cls.COMPETENSE_INFO.items():
                if normalized.startswith(prefix):
                    order = info['order']
                    break

            numbers = re.findall(r'\d+', normalized)
            
            return (
                order,
                int(numbers[0]) if numbers else 0,
                int(numbers[1]) if len(numbers) > 1 else 0
            )
        
        if isinstance(competences_data, dict):
            sorted_keys = sorted(
                competences_data.keys(), 
                key=lambda k: get_sort_key(k)
            )
            return [competences_data[key] for key in sorted_keys]
        
        elif isinstance(competences_data, list):
            if competences_data and isinstance(competences_data[0], str):
                return sorted(competences_data, key=get_sort_key)
            else:
                return sorted(competences_data, key=lambda x: get_sort_key(x.get('competence_index', '')))
        
        else:
            return competences_data

    @classmethod
    def get_all_competences(cls, **filters):
        """Получение всех уникальных компетенций для учебного плана"""
        queryset = Competence.objects.all()#LinesIndicators.objects.all()

        if filters:
            queryset = queryset.filter(**filters)
    
        competences = queryset.values(
            'competence_index',
            'competence'
        )#.distinct('competence_index')
        
        return cls.sort_competences(list(competences))
    
    @classmethod
    def get_all_disciplines(cls, plan_id, filter=True, exclude_children=False):
        """Получение всех дисциплин для учебного плана"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)

        disciplines = LinesData.objects.filter(
            plan=plan
        ).values(
            'id',
            'newdisid',
            'dis',
        ).order_by('newdisid')
        
        if not filter:
            return list(disciplines)

        base_exclude = cls.DISCIPLINE_GROUPS_TO_EXCLUDE | cls.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN
        filtered_disciplines = []
        for disc in disciplines:
            disc_newdisid = disc['newdisid']
            should_exclude = False

            if disc_newdisid in base_exclude:
                should_exclude = True

            elif exclude_children:
                for group in cls.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN:
                    if disc_newdisid == group or disc_newdisid.startswith(group + '.'):
                        should_exclude = True
                        break

            if not should_exclude:
                filtered_disciplines.append(disc)
        
        return filtered_disciplines
    
    @staticmethod
    def get_discipline_types(discipline_index):
        """Типы дисциплины"""
        types = []

        # Основные категории
        if 'Б1.Б' in discipline_index:
            types.append('Обязательная часть')
        if 'Б1.В' in discipline_index:
            types.append('Вариативная часть')
        if 'Б2' in discipline_index:
            types.append('Практика')
        if 'Б3' in discipline_index:
            types.append('ГИА')

        # Конкретные модули
        if 'Б1.Б.01' in discipline_index:
            types.append('Общеобразовательный модуль')
        if 'Б1.Б.02' in discipline_index:
            types.append('Фундаментальный модуль')
        if 'Б1.Б.03' in discipline_index:
            types.append('Базовый модуль направления')
        if 'Б1.Б.04' in discipline_index:
            types.append('Модуль проектной деятельности')
        if 'Б1.Б.05' in discipline_index:
            types.append('Модуль по физической культуре')
        if 'Б1.В.01' in discipline_index:
            types.append('Модуль проектной деятельности')
        if 'Б1.В.02' in discipline_index:
            types.append('Модуль профильной подготовки')
        if 'Б1.В.03' in discipline_index:
            types.append('Модуль дополнительного профиля')

        # Если не попали в конкретные
        if not types and ('Б1.Б' in discipline_index or 'Б1.В' in discipline_index):
            types.append('Другой')

        return types if types else ['Другой']
    
    def should_exclude_discipline(discipline_index):
        """Проверяет, должна ли дисциплина быть исключена из проверки"""
        exclude_groups = (RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE | 
                        RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN)
        
        if discipline_index in exclude_groups:
            return True
            
        for group in RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN:
            if discipline_index.startswith(group + '.') or discipline_index == group:
                return True
                
        return False

    @staticmethod
    def get_lines_indicators(**filters):
        """Получение индикаторов компетенций"""
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
        
    @classmethod
    def update_discipline_kompetences(cls, dis_id):
        """Обновление перечня компетенций у дисциплины (поле kompetences в LinesData)"""
        dis = dis_id if isinstance(dis_id, LinesData) else LinesData.objects.get(id=dis_id)

        # Получаем все индикаторы дисциплины
        indicators = cls.get_lines_indicators(planlineid=dis)
        
        if indicators.exists():
            # Формируем строку уникальных индикаторов через запятую
            indicator_list = [str(ind.indicator_index) for ind in indicators]
            kompetences_str = ",".join(indicator_list)
        else:
            kompetences_str = ""
        
        dis.kompetences = kompetences_str
        dis.save(update_fields=['kompetences'])

    @classmethod
    def add_competence_to_discipline(cls, discipline, competence_index, competence_name):
        """Добавляет одну компетенцию к дисциплине с генерацией индикаторов и схемы"""
        competence_obj = Competence.objects.get(
            plan_id=discipline.plan_id,
            competence_index=competence_index
        )
        
        # Получаем все семестры дисциплины с формами аттестации
        semesters_with_forms = []
        for sem in SemesterData.objects.filter(planlineid=discipline):
            forms = {
                'ekz': bool(sem.ekz),
                'zach': bool(sem.zach),
                'zacho': bool(sem.zacho and sem.zacho > 0),
                'kp': bool(sem.kp),
                'kr': bool(sem.kr)
            }
            
            if any(forms.values()):
                semesters_with_forms.append({
                    'semester': sem.num,
                    'forms': forms
                })
        
        # Создаём записи в Scheme
        scheme_records = []
        for item in semesters_with_forms:
            scheme = Scheme.objects.create(
                planlineid=discipline,
                competence_id=competence_obj,
                semester=item['semester'],
                **item['forms']
            )
            scheme_records.append(scheme)
        
        # Создаём индикаторы (по одному на каждую запись в схеме)
        existing_indicators = LinesIndicators.objects.filter(
            planlineid=discipline,
            competence_index=competence_index
        ).exclude(indicator_index__icontains='Итоговый индикатор')
        
        max_num = 0
        for ind in existing_indicators:
            if ind.indicator_index:
                match = re.search(rf'{re.escape(competence_index)}\.(\d+)', ind.indicator_index)
                if match:
                    max_num = max(max_num, int(match.group(1)))
        
        # Создаём индикаторы
        for i in range(len(scheme_records)):
            new_index = f"{competence_index}.{max_num + i + 1}"
            LinesIndicators.objects.create(
                planlineid=discipline,
                competence_index=competence_index,
                competence=competence_name,
                indicator_index=new_index,
                indicator=""  # пустой, редактируется позже
            )

    # Правила валидации для матрицы компетенций
    @staticmethod
    def validate_disciplines_without_competences(raw_disciplines, indicators):
        """Правило: дисциплины без компетенций"""
        disciplines_with_competences = set(ind['planlineid_id'] for ind in indicators)
        disciplines_without_competences = []
        
        for disc in raw_disciplines:
            if disc['id'] not in disciplines_with_competences:
                disciplines_without_competences.append({
                    'message': f'Дисциплина "{disc["dis"]}" ({disc["newdisid"]}) не имеет привязанных компетенций',
                    'discipline_id': disc['id'],
                    'discipline_index': disc['newdisid'],
                    'discipline_name': disc['dis']
                })
        
        return disciplines_without_competences
    
    @staticmethod
    def validate_competences_without_disciplines(indicators, all_competences):
        """Правило: компетенции без дисциплин"""
        used_competence_indexes = {ind['competence_index'] for ind in indicators}
        competences_without_disciplines = []
        
        for comp in all_competences:
            if comp['competence_index'] not in used_competence_indexes:
                competences_without_disciplines.append({
                    'message': f'Компетенция "{comp["competence"]}" ({comp["competence_index"]}) не привязана ни к одной дисциплине',
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                })
        
        return competences_without_disciplines
    
    @classmethod
    def validate_professional_competences_in_prediplom_practice(cls, raw_disciplines, all_competences):
        """Правило: профессиональные компетенции должны формироваться преддипломной практикой"""
        prediplom_practice_ids = []
        for disc in raw_disciplines:
            if 'преддиплом' in disc['dis'].lower():
                prediplom_practice_ids.append(disc['id'])

        professional_competences_without_practice = []
        if prediplom_practice_ids:
            practice_competences = set()
            practice_indicators = LinesIndicators.objects.filter(
                planlineid__in=prediplom_practice_ids
            ).values('competence_index').distinct()
            practice_competences = {ind['competence_index'] for ind in practice_indicators}
            
            # Проверяем профессиональные компетенции
            for comp in all_competences:
                if (comp['competence_index'] not in practice_competences and cls.get_competence_type(comp['competence_index']) == 'Профессиональная'):
                    professional_competences_without_practice.append({
                        'message': f'Профессиональная компетенция {comp["competence_index"]} не формируется преддипломной практикой',
                        'competence_index': comp['competence_index'],
                        'competence': comp['competence']
                    })
        else:
            # Если преддипломная практика не найдена, все профессиональные компетенции считаются проблемными
            for comp in all_competences:
                if cls.get_competence_type(comp['competence_index']) == 'Профессиональная':
                    professional_competences_without_practice.append({
                        'message': f'Профессиональная компетенция {comp["competence_index"]} не формируется преддипломной практикой (практика не найдена)',
                        'competence_index': comp['competence_index'],
                        'competence': comp['competence']
                    })
        return professional_competences_without_practice
    
    @classmethod
    def validate_opk_in_practice(cls, practice_discipline_ids):
        """Правило: хотя бы одна практика должна формировать общепрофессиональную компетенцию"""
        opk_formed_by_practice = False
        practice_indicators = LinesIndicators.objects.filter(
            planlineid__in=practice_discipline_ids
        )
        
        for indicator in practice_indicators:
            comp_type = cls.get_competence_type(indicator.competence_index)
            if comp_type == 'Общепрофессиональная':
                opk_formed_by_practice = True
                break
        
        practice_without_opk_error = []
        if not opk_formed_by_practice:
            practice_without_opk_error.append({
                'message': 'Хотя бы одна практика должна формировать общепрофессиональную компетенцию',
                'competence_index': None,
                'competence': None
            })
        return practice_without_opk_error
    
    @staticmethod
    def validate_competences_not_only_in_practice(practice_discipline_ids, indicators, all_competences):
        """Проверка: компетенция не может формироваться только практиками"""
        competences_only_in_practice = []
        competence_to_disciplines = defaultdict(set)
        for ind in indicators:
            competence_to_disciplines[ind['competence_index']].add(ind['planlineid_id'])

        for comp_index, discipline_ids in competence_to_disciplines.items():
            # Если все дисциплины — это практики
            if discipline_ids and discipline_ids.issubset(practice_discipline_ids):
                comp_obj = next((c for c in all_competences if c['competence_index'] == comp_index), None)
                competences_only_in_practice.append({
                    'message': f'Компетенция {comp_index} формируется только практиками, без других дисциплин',
                    'competence_index': comp_index,
                    'competence': comp_obj['competence']
                })
        return competences_only_in_practice

