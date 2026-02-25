from django.db import transaction
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators
from datetime import datetime
from competence_passport.services.ruleService import RuleService

class MatrixService:
    @staticmethod
    def get_competence_matrix(plan_id):
        """Получение матрицы компетенций"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)

        disciplines = RuleService.get_all_disciplines(plan, filter=False)
        
        groups = {}

        for discipline in disciplines:
            # Получаем компетенции для этой дисциплины с полным описанием
            competences_with_indicators = LinesIndicators.objects.filter(
                planlineid=discipline['id'],
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence',
                'indicator_index',
                'indicator'
            ).order_by('competence_index', 'indicator_index').distinct('competence_index', 'indicator_index')

            competence_dicts = {}
            for ind in competences_with_indicators:
                cidx = ind['competence_index']
                if cidx not in competence_dicts:
                    competence_dicts[cidx] = {
                        'competence_index': cidx,
                        'competence': ind['competence'],
                        'type': RuleService.get_competence_type(cidx),
                        'indicator_list': []
                    }
                competence_dicts[cidx]['indicator_list'].append({
                    'indicator_index': ind['indicator_index'],
                    'indicator': ind['indicator']
                })


            disc_key = discipline['newdisid']
            exclude_groups = (RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE | 
                            RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN)
            
            if disc_key not in groups:
                # Проверяем, является ли этот индекс группой
                if disc_key in exclude_groups:
                    group_name = RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE.get(
                        disc_key,
                        RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN.get(disc_key, disc_key)
                    )
                    groups[disc_key] = {
                        'type': 'group',
                        'id': discipline['id'],
                        'index': disc_key,
                        'name': group_name,
                        'competences': {}, 
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }
                else:
                    groups[disc_key] = {
                        'type': 'discipline',
                        'id': discipline['id'],
                        'index': disc_key,
                        'name': discipline['dis'],
                        'competences': {}, 
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }

            groups[disc_key]['competences'].update(competence_dicts)
            
            # Обрабатываем родительские группы
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
                    group_name = RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE.get(
                        base_group_key,
                        RuleService.DISCIPLINE_GROUPS_TO_EXCLUDE_WITH_CHILDREN.get(base_group_key, base_group_key)
                    )

                    groups[base_group_key] = {
                        'type': 'group',
                        'id': discipline['id'],
                        'index': base_group_key,
                        'name': group_name,
                        'competences': {}, 
                        'level': base_group_key.count('.') + 1 if '.' in base_group_key else 1
                    }

                groups[base_group_key]['competences'].update(competence_dicts)

        matrix_data = []
        for item in groups.values():
            sorted_competences = RuleService.sort_competences(item['competences'])

            matrix_data.append({
                'type': item['type'], 
                'level': item['level'],  
                'discipline_id': item['id'],
                'discipline_index': item['index'],
                'discipline_name': item['name'],
                'competence_list': sorted_competences 
            })

        matrix_data.sort(key=lambda x: (x['discipline_index']))

        return matrix_data
    
    @staticmethod
    def validate_competence_matrix(plan_id):
        """
        Валидация матрицы компетенций
        Проверяет есть ли дисциплины без компетенций, есть ли компетенции без дисциплин
        """      
        plan = PlanData.objects.get(mira_id=plan_id)
        
        # Получаем все дисциплины
        raw_disciplines = RuleService.get_all_disciplines(
            plan_id=plan,
            filter=True,
            exclude_children=True
        )
        discipline_ids = [d['id'] for d in raw_disciplines]
        
        # Получаем все индикаторы для этих дисциплин
        indicators = LinesIndicators.objects.filter(
            planlineid__in=discipline_ids
        ).values('competence_index', 'planlineid_id').distinct()
        
        # Находим дисциплины без компетенций
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
        
        # Находим все уникальные компетенции в плане
        all_competences = RuleService.get_all_competences(
            #planlineid__plan=plan
            plan_id=plan
        )
        
        # Находим компетенции, которые есть в плане, но не используются в дисциплинах
        used_competence_indices = {ind['competence_index'] for ind in indicators}
        competences_without_disciplines = []
        
        for comp in all_competences:
            if comp['competence_index'] not in used_competence_indices:
                competences_without_disciplines.append({
                    'message': f'Компетенция "{comp["competence"]}" ({comp["competence_index"]}) не привязана ни к одной дисциплине',
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                })
        
        # Определяем валидность
        is_valid = len(disciplines_without_competences) == 0 and len(competences_without_disciplines) == 0
        
        errors = disciplines_without_competences + competences_without_disciplines
        
        return {
            'is_valid': is_valid,
            'errors': errors,
            'checked_at': datetime.now().isoformat(),
            'disciplines_without_competences_count': len(disciplines_without_competences),
            'competences_without_disciplines_count': len(competences_without_disciplines)
        }
    
    @staticmethod
    def update_discipline_competences(plan_id, discipline_id, selected_competences):
        """
        Обновление компетенции у дисциплины
        Удаление ненужных, добавление новых, сохранение существующих
        """
        # Получаем дисциплины
        plan = PlanData.objects.get(mira_id=plan_id)
        discipline = LinesData.objects.get(id=discipline_id, plan=plan)

        # Текущие компетенции дисциплины
        current_competences = set(
            LinesIndicators.objects.filter(planlineid=discipline)
            .values_list('competence_index', flat=True)
            .distinct()
        )

        # Выбранные компетенции
        selected_competences_map = {
            comp['competence_index']: comp['competence']
            for comp in selected_competences
            if comp.get('competence_index')
        }
        selected_competences_set = set(selected_competences_map.keys())

        # Определяем действия
        to_delete = current_competences - selected_competences_set
        to_add = selected_competences_set - current_competences

        with transaction.atomic():
            # Удаляем ненужные
            if to_delete:
                LinesIndicators.objects.filter(
                    planlineid=discipline,
                    competence_index__in=to_delete
                ).delete()

            # Добавляем новые
            for comp_index in to_add:
                competence_name = selected_competences_map[comp_index]
                RuleService.add_competence_to_discipline(discipline, comp_index, competence_name)

            # Обновляем запись у дисциплины
            RuleService.update_discipline_kompetences(discipline)

        return {
            'discipline': discipline,
            'deleted': sorted(to_delete),
            'added': sorted(to_add),
            'kept': sorted(current_competences & selected_competences_set)
        }
