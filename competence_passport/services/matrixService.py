from django.db import transaction
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators
from competence_passport.models import Scheme
from datetime import datetime
from competence_passport.services.ruleService import RuleService
from collections import defaultdict

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
        Проверяет есть ли дисциплины без компетенций, есть ли компетенции без дисциплин;
        Формируются ли проф компетенции преддипломной практикой;
        Формирует ли хотя бы одна практика общепрофессиональную компетенцию
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
        
        # 1. Дисциплины без компетенций
        disciplines_without_competences = RuleService.validate_disciplines_without_competences(
            raw_disciplines, indicators
        )

        # 2. Компетенции без дисциплин
        all_competences = RuleService.get_all_competences(plan_id=plan)

        competences_without_disciplines = RuleService.validate_competences_without_disciplines(
            indicators, all_competences
        )

        practice_discipline_ids = []
        for disc in raw_disciplines:
            if 'практика' in disc['dis'].lower():
                practice_discipline_ids.append(disc['id'])

       
        # 3. Все профессиональные компетенции должны формироваться преддипломной практикой
        professional_competences_without_practice = RuleService.validate_professional_competences_in_prediplom_practice(
            raw_disciplines, all_competences
        )

        # 4. Хотя бы одна практика должна формировать общепрофессиональную компетенцию
        practice_without_opk_error = RuleService.validate_opk_in_practice(
            practice_discipline_ids
        )

        # 5. Компетенция не может формироваться только практикой 
        competences_only_in_practice = RuleService.validate_competences_not_only_in_practice(
            practice_discipline_ids, indicators, all_competences
        )
        
        errors = (
            disciplines_without_competences + 
            competences_without_disciplines +
            professional_competences_without_practice +
            practice_without_opk_error +
            competences_only_in_practice)
        
        is_valid = len(errors) == 0
        
        return {
            'is_valid': is_valid,
            'errors': errors,
            'checked_at': datetime.now().isoformat(),
            'disciplines_without_competences_count': len(disciplines_without_competences),
            'competences_without_disciplines_count': len(competences_without_disciplines),
            'professional_competences_without_practice_count': len(professional_competences_without_practice),
            'practice_without_opk_count': len(practice_without_opk_error),
            'competences_only_in_practice_count': len(competences_only_in_practice)
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
                Scheme.objects.filter(
                    planlineid=discipline,
                    competence_id__competence_index__in=to_delete
                ).delete()

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
