import re
from django.db import transaction
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators
from competence_passport.models import Competence
from generator.models import DisciplineIndicators
from collections import defaultdict
from competence_passport.services.ruleService import RuleService

class PassportService:
    @staticmethod
    def get_competence_passport(plan_id):
        """Получение паспорта компетенций"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)

        # Получаем дисциплины
        filtered_disciplines = RuleService.get_all_disciplines(
            plan, 
            filter=True, 
            exclude_children=True
        )
        filtered_discipline_ids = {d['id'] for d in filtered_disciplines}

        competences = Competence.objects.filter(plan_id=plan)
        competences = RuleService.sort_competences(competences)

        # Отфильтрованные индикаторы
        indicators = LinesIndicators.objects.filter(
            planlineid__plan=plan,
            planlineid__in=filtered_discipline_ids,
            competence_index__in=[c.competence_index for c in competences]
        ).select_related('planlineid')

        indicators_for_list = defaultdict(list)
        for ind in indicators:
            indicators_for_list[ind.competence_index].append(ind)

        # ЗУВ и критерии
        indicator_ids_for_list = [ind.id for ind in indicators]
        disc_ind_map = {}
        for di in DisciplineIndicators.objects.filter(
            indicator_id__in=indicator_ids_for_list,
            planlineid_id__in=filtered_discipline_ids
        ):
            key = (di.indicator_id, di.planlineid_id)
            disc_ind_map[key] = di

        passport_data = []
        for comp in competences:
            comp_idx = comp.competence_index
            comp_text = comp.competence
            comp_type = RuleService.get_competence_type(comp_idx)
            comp_relations = comp.relations#relations_map.get(comp_idx, "")

            # Поиск итогового индикатора
            final_indicator = comp.final_indicator

            indicator_list = []
            for ind in indicators_for_list.get(comp_idx, []):
                key = (ind.id, ind.planlineid.id)
                disc_ind = disc_ind_map.get(key)
                indicator_list.append({
                    "indicator_id": ind.id,
                    "indicator_index": ind.indicator_index or "",
                    "indicator": ind.indicator or "",
                    "discipline_id": ind.planlineid.id,
                    "discipline_index": ind.planlineid.newdisid or "",
                    "discipline_name": ind.planlineid.dis or "",
                    "know": disc_ind.know if disc_ind else "",
                    "able": disc_ind.able if disc_ind else "",
                    "own": disc_ind.own if disc_ind else "",
                    "criteria": disc_ind.criteria if disc_ind else "",
                    "methods": disc_ind.methods if disc_ind else ""
                })

            # Сортировка
            def sort_key(x):
                nums = re.findall(r'\d+', x["indicator_index"])
                return (int(nums[0]) if nums else 0, int(nums[1]) if len(nums) > 1 else 0)
            indicator_list.sort(key=sort_key)

            passport_data.append({
                "competence_index": comp_idx,
                "type": comp_type,
                "competence": comp_text,
                "competence_relations": comp_relations,
                "competence_final_indicator": final_indicator,
                "indicator_list": indicator_list
            })

        passport_data = RuleService.sort_competences(passport_data)

        return passport_data
    
    @staticmethod
    def update_competence_final_indicator(plan_id, competence_index, final_indicator_text):
        """
        Обновление или создание итогового индикатора компетенции
        """
        plan = PlanData.objects.get(id=plan_id)

        with transaction.atomic():
            # Поиск существующего итогового индикатора
            final_indicators = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index,
                indicator_index__icontains='Итоговый индикатор'
            ).order_by('indicator_index')
            
            competence = Competence.objects.filter(
                plan_id=plan,
                competence_index=competence_index,
            ).first()

            if final_indicators.exists() or competence.exists():
                indicator = final_indicators.first()
                indicator.indicator = final_indicator_text
                indicator.save()

                competence.final_indicator = final_indicator_text
                competence.save()
                return {
                    #'indicator': indicator,
                    'indicator': competence.final_indicator
                }

            # Создание нового итогового индикатора
            first_indicator = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()

            if not first_indicator:
                raise ValueError("Для этой компетенции нет индикаторов в учебном плане")

            new_index = f"{first_indicator.indicator_index} Итоговый индикатор"
            indicator = LinesIndicators.objects.create(
                planlineid=first_indicator.planlineid,
                competence_index=competence_index,
                competence=first_indicator.competence,
                indicator_index=new_index,
                indicator=final_indicator_text
            )

            competence.final_indicator = final_indicator_text
            competence.save()
            return {
                #'indicator': indicator,
                'indicator': competence.final_indicator
            }
        
    @staticmethod
    def update_indicator_details(indicator_id, know, able, own, criteria, methods):
        """Обновление деталей индикатора"""
        with transaction.atomic():
            indicator = LinesIndicators.objects.get(id=indicator_id)
            discipline_indicator, _ = DisciplineIndicators.objects.update_or_create(
                indicator=indicator,
                defaults={
                    'planlineid': indicator.planlineid,
                    'know': know or "",
                    'able': able or "",
                    'own': own or "",
                    'criteria': criteria or "",
                    'methods': methods or ""
                }
            )
            return discipline_indicator
        
    @staticmethod
    def update_indicator(indicator_id, discipline_id=None, indicator_index=None, indicator_content=None):
        """
        Обновление индикатора: дисциплины, индекса, текста.
        """
        with transaction.atomic():
            indicator = LinesIndicators.objects.select_related('planlineid').get(id=indicator_id)
            old_discipline = indicator.planlineid

            # Обновление дисциплины
            if discipline_id and discipline_id != old_discipline.id:
                new_discipline = LinesData.objects.get(id=discipline_id)
                indicator.planlineid = new_discipline

            # Обновление индекса
            if indicator_index:
                existing = LinesIndicators.objects.filter(
                    planlineid=indicator.planlineid,
                    competence_index=indicator.competence_index,
                    indicator_index=indicator_index
                ).exclude(id=indicator_id).exists()

                if existing:
                    raise ValueError(f"Индикатор с индексом {indicator_index} уже существует в этой дисциплине")

                indicator.indicator_index = indicator_index

            # Обновление текста
            if indicator_content is not None:
                indicator.indicator = indicator_content

            indicator.save()

            # Обновление строки компетенций у дисциплины
            RuleService.update_discipline_kompetences(old_discipline)
            if discipline_id and discipline_id != old_discipline.id:
                RuleService.update_discipline_kompetences(indicator.planlineid)

            return indicator