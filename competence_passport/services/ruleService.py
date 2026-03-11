import re
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators, SemesterData
from competence_passport.models import Competence, Scheme

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
        """Добавляет одну компетенцию к дисциплине с генерацией индикатора и схемы"""
        # Находим последний номер индикатора
        existing = LinesIndicators.objects.filter(
            planlineid=discipline,
            competence_index=competence_index
        ).exclude(indicator_index__icontains='Итоговый индикатор')

        last_number = 0
        for ind in existing:
            if ind.indicator_index:
                match = re.search(rf'{re.escape(competence_index)}\.(\d+)', ind.indicator_index)
                if match:
                    num = int(match.group(1))
                    last_number = max(last_number, num)

        new_index = f"{competence_index}.{last_number + 1}"

        # Создаём индикатор
        LinesIndicators.objects.create(
            planlineid=discipline,
            competence_index=competence_index,
            competence=competence_name,
            indicator_index=new_index,
            indicator=""  # пустой, редактируется позже
        )

        competence_obj = Competence.objects.get(
            plan_id=discipline.plan_id,
            competence_index=competence_index
        )
        semesters = SemesterData.objects.filter(planlineid=discipline)
        
        # Создаём записи в Scheme для каждого семестра с формами аттестации
        for sem in semesters:
            has_forms = any([
                sem.ekz, sem.zach, 
                (sem.zacho and sem.zacho > 0), 
                sem.kp, sem.kr
            ])
            
            if has_forms:
                Scheme.objects.create(
                    planlineid=discipline,
                    competence_id=competence_obj,
                    semester=sem.num,
                    ekz=bool(sem.ekz),
                    zach=bool(sem.zach),
                    zacho=bool(sem.zacho and sem.zacho > 0),
                    kp=bool(sem.kp),
                    kr=bool(sem.kr)
                )


