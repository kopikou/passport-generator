import re
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators

class ReferenceService:
    """Сервис для работы со справочниками данных"""
    
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
    def sort_competences(cls, competences_list):
        """Сортировка компетенций"""
        def sort_key(item):
            competence_index = item.get('competence_index', '')
            
            normalized = competence_index.strip()

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
        
        return sorted(competences_list, key=sort_key)

    @classmethod
    def get_all_competences_for_plan(cls, plan_id):
        """Получение всех уникальных компетенций для плана"""
        plan = PlanData.objects.get(mira_id=plan_id)
        plan_lines = LinesData.objects.filter(plan=plan)
        
        competences = LinesIndicators.objects.filter(
            planlineid__in=plan_lines, 
            competence__isnull=False,
            competence_index__isnull=False
        ).values(
            'competence_index',
            'competence'
        ).distinct('competence_index')
        
        return cls.sort_competences(list(competences))
    
    @classmethod
    def get_all_disciplines_for_plan(cls, plan_id):
        """Получение всех дисциплин для учебного плана"""
        plan = PlanData.objects.get(mira_id=plan_id)
        
        disciplines = LinesData.objects.filter(
            plan=plan
        ).values(
            'id',
            'newdisid',
            'dis',
        ).order_by('newdisid')
        
        filtered_disciplines = []
        for disc in disciplines:
            disc_newdisid = disc['newdisid']           
            should_exclude = False

            if disc_newdisid in cls.DISCIPLINE_GROUPS_TO_EXCLUDE or disc_newdisid in cls.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN:
                should_exclude = True
            
            if not should_exclude:
                filtered_disciplines.append(disc)
        
        return list(filtered_disciplines)
    


    
