import re
from django.db import transaction
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators, SemesterData
from competence_passport.models import Scheme, Competence
from datetime import datetime
from collections import defaultdict
from competence_passport.services.ruleService import RuleService

class SchemaService:
    @staticmethod
    def get_competence_schema(plan_id):
        """Получение схемы компетенций с формами контроля по дисциплинам и семестрам"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)

        disciplines = RuleService.get_all_disciplines(plan, filter=True, exclude_children=True)
        discipline_ids = [d['id'] for d in disciplines]

        schema = Scheme.objects.filter(
            planlineid__in=discipline_ids
        ).select_related('planlineid')

        competence_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for line in schema:
            comp_idx = line.competence_id.competence_index
            disc_id = line.planlineid_id
            semester = line.semester
            competence_map[comp_idx][disc_id][semester].append(line)

        schema_data = []

        for comp_idx, disc_map in competence_map.items():
            # Получаем содержание компетенции 
            shema = next(iter(next(iter(disc_map.values())).values()))[0]
            competence = shema.competence_id.competence or ""

            discipline_list = []

            for disc_id, sem_map in disc_map.items():
                # Находим дисциплину 
                disc_info = next((d for d in disciplines if d['id'] == disc_id), None)
                if not disc_info:
                    continue

                semester_data = []
                for semester, forms in sem_map.items():
                    form_control = set()
                    for form in forms:
                        if form.ekz: form_control.add("ekz")
                        if form.zach: form_control.add("zach")
                        if form.zacho: form_control.add("zacho")
                        if form.kp: form_control.add("kp")
                        if form.kr: form_control.add("kr")
                    semester_data.append({
                        "semester": semester,
                        "form_control": sorted(form_control)  
                    })

                discipline_list.append({
                    "discipline_id": disc_id,
                    "discipline_index": disc_info['newdisid'],
                    "discipline_name": disc_info['dis'],
                    "semester_data": semester_data
                })

            discipline_list.sort(key=lambda d: d['discipline_index'])

            schema_data.append({
                "competence_index": comp_idx,
                "competence": competence,
                "discipline_list": discipline_list
            })

        schema_data = RuleService.sort_competences(schema_data)

        return schema_data

    @staticmethod
    def update_semester_scheme(plan_id, discipline_id, competence_index, competence, semester, forms):
        """
        Обновление схемы аттестации для компетенции в дисциплине и семестре
        Если формы не выбраны — удаление записи
        """
        # Получаем дисциплины
        plan = PlanData.objects.get(mira_id=plan_id)
        discipline = LinesData.objects.get(id=discipline_id, plan=plan)

        # Проверяем существование семестра
        semester_obj = SemesterData.objects.filter(
            planlineid=discipline,
            num=semester
        ).first()
        if not semester_obj:
            raise ValueError("Указанный семестр не существует для данной дисциплины")

        # Проверяем доступности форм по учебному плану
        form_fields = ['ekz', 'zach', 'zacho', 'kp', 'kr']
        for field in form_fields:
            if forms.get(field, False) and not getattr(semester_obj, field, False):
                raise ValueError(f"Форма аттестации недоступна в этом семестре")

        has_any_form = any(forms.get(f, False) for f in form_fields)

        competence_id = Competence.objects.get(
            competence_index=competence_index,
            plan_id=plan.id
        )
        with transaction.atomic():
            if has_any_form:
                # Создаём или обновляем
                scheme, created = Scheme.objects.update_or_create(
                    planlineid=discipline,
                    competence_id=competence_id,
                    semester=semester,
                    defaults={
                        **{f: forms.get(f, False) for f in form_fields}
                    }
                )
                scheme_id = scheme.id
            else:
                # Удаляем, если нет форм
                Scheme.objects.filter(
                    planlineid=discipline,
                    competence_id=competence_id,
                    semester=semester
                ).delete()
                scheme_id = None
                created = False

        return {
            'scheme_id': scheme_id,
            'created': created,
            'has_forms': has_any_form
        }
    
    @staticmethod
    def validate_scheme_indicators(plan_id):
        """
        Проверка соответствия числа промежуточных аттестаций и индикаторов
        """
        plan = PlanData.objects.get(mira_id=plan_id)
        
        # Получаем схемы и индикаторы
        schemes = Scheme.objects.filter(
            planlineid__plan=plan
        ).select_related('planlineid', 'competence_id').order_by(
            'competence_id__competence_index', 'planlineid__newdisid', 'semester'
        )
        
        indicators = RuleService.get_lines_indicators(
            planlineid__plan=plan,
            competence_index__isnull=False
        ).select_related('planlineid').exclude(
            indicator_index__icontains='Итоговый индикатор'
        )

        # Получаем все семестры для случая "нет форм"
        semester_data_map = defaultdict(list)
        semester_objs = SemesterData.objects.filter(planlineid__plan=plan)
        for sem in semester_objs:
            semester_data_map[sem.planlineid.id].append(sem)

        indicators_dict = defaultdict(list)
        for ind in indicators:
            indicators_dict[(ind.competence_index, ind.planlineid.id)].append(ind)

        schemes_dict = defaultdict(list)
        for scheme in schemes:
            schemes_dict[(scheme.competence_id.competence_index, scheme.planlineid.id)].append(scheme)
        
        validation_errors = []
        
        all_keys = set(schemes_dict.keys()) | set(indicators_dict.keys())
        
        for key in all_keys:
            competence_index, discipline_id = key
            
            discipline_obj = None
            discipline_index = None

            if indicators_dict[key]:
                discipline_obj = indicators_dict[key][0].planlineid
                discipline_index = discipline_obj.newdisid
            elif schemes_dict[key]:
                discipline_obj = schemes_dict[key][0].planlineid
                discipline_index = discipline_obj.newdisid
            
            # Пропускаем дисциплины для исключения
            if discipline_index and RuleService.should_exclude_discipline(discipline_index):
                continue
                
            forms_count = len(schemes_dict[key])
            indicators_count = len(indicators_dict[key])
            
            if forms_count != indicators_count:
                if forms_count > 0 and indicators_count == 0:
                    message = 'Указаны формы аттестации, но отсутствуют индикаторы'
                elif forms_count == 0 and indicators_count > 0:
                    message = 'Указаны индикаторы, но отсутствуют формы аттестации'
                else:
                    message = f'Не совпадает число форм аттестации ({forms_count}) и индикаторов ({indicators_count})'
                
                competence_name = None
                discipline_name = None
                
                if schemes_dict[key]:
                    example_scheme = schemes_dict[key][0]
                    competence_name = example_scheme.competence_id.competence
                    discipline_name = example_scheme.planlineid.dis
                elif indicators_dict[key]:
                    example_indicator = indicators_dict[key][0]
                    competence_name = example_indicator.competence
                    discipline_name = example_indicator.planlineid.dis

                semesters_to_check = []
                # Несоответсвие 
                if forms_count > 0:
                    # Если есть формы аттестаций, то используем их семестры
                    semesters_to_check = [s.semester for s in schemes_dict[key]]
                else:
                    # Если нет форм аттестаций, используем все семестры дисциплины
                    semesters_to_check = [sem.num for sem in semester_data_map.get(discipline_id, [])] or [1] 

                for semester in semesters_to_check:
                    error_id = f"{competence_index}_{discipline_id}_{semester}"
                    validation_errors.append({
                        'id': error_id,
                        'competence_index': competence_index,
                        'competence_name': competence_name,
                        'discipline_index': discipline_index or '',
                        'discipline_name': discipline_name or '',
                        'discipline_id': discipline_id,
                        'scheme_forms_count': forms_count,
                        'indicators_count': indicators_count,
                        'semester': semester,
                        'message': message,
                    })
        
        # Сортировка
        errors_by_competence = defaultdict(list)
        for error in validation_errors:
            errors_by_competence[error['competence_index']].append(error)
        
        sorted_competences = RuleService.sort_competences(list(errors_by_competence.keys()))
        sorted_errors = []
        for comp_idx in sorted_competences:
            sorted_errors.extend(sorted(errors_by_competence[comp_idx], 
                                    key=lambda x: (x['discipline_index'], x['semester'])))
        
        return {
            'is_valid': len(sorted_errors) == 0,
            'errors': sorted_errors,
            'checked_at': datetime.now().isoformat(),
            'errors_count': len(sorted_errors)
        }

    @staticmethod
    def fix_scheme_indicators(plan_id, discipline_id,competence_index,scheme_forms_count):
        """
        Автоматическое исправление индикаторов - создание или удаление.
        """
        plan = PlanData.objects.get(mira_id=plan_id)
        discipline = LinesData.objects.get(id=discipline_id, plan=plan)
        
        with transaction.atomic():
            # Получаем существующие индикаторы
            existing_indicators = LinesIndicators.objects.filter(
                planlineid=discipline,
                competence_index=competence_index
            ).exclude(
                indicator_index__icontains='Итоговый индикатор'
            ).order_by('indicator_index')
            
            # Получаем компетенцию для создания новых индикаторов
            competence_obj = LinesIndicators.objects.filter(
                planlineid__plan=plan,
                competence_index=competence_index
            ).first()
            
            if not competence_obj:
                raise ValueError('Компетенция не найдена в плане')
            
            current_count = existing_indicators.count()
            needed_count = scheme_forms_count
            indicators_created = 0
            indicators_removed = 0
            
            # Создание недостающих индикаторов
            if needed_count > current_count:
                to_create = needed_count - current_count
                # Получаем максимальный номер существующего индикатора
                max_num = 0
                for ind in existing_indicators:
                    if ind.indicator_index:
                        match = re.search(rf'{re.escape(competence_index)}\.(\d+)', ind.indicator_index)
                        if match:
                            max_num = max(max_num, int(match.group(1)))
                
                for i in range(1, to_create + 1):
                    new_num = max_num + i
                    indicator_index = f"{competence_index}.{new_num}"
                    
                    LinesIndicators.objects.create(
                        planlineid=discipline,
                        competence_index=competence_index,
                        competence=competence_obj.competence,
                        indicator_index=indicator_index,
                        indicator=''
                    )
                    indicators_created += 1
            
            # Удаление лишних индикаторов
            elif needed_count < current_count:
                to_remove = current_count - needed_count
                indicators_to_delete = existing_indicators.order_by('-indicator_index')[:to_remove]
                for ind in indicators_to_delete:
                    ind.delete()
                    indicators_removed += 1
            
            # Обновляем запись дисциплины
            RuleService.update_discipline_kompetences(discipline)
            
            final_count = LinesIndicators.objects.filter(
                planlineid=discipline,
                competence_index=competence_index
            ).exclude(
                indicator_index__icontains='Итоговый индикатор'
            ).count()
            
            message_parts = []
            if indicators_created:
                message_parts.append(f'создано {indicators_created} индикаторов')
            if indicators_removed:
                message_parts.append(f'удалено {indicators_removed} индикаторов')
            if not message_parts:
                message_parts.append('количество индикаторов уже соответствует формам аттестации')
            
            return {
                'success': True,
                'indicators_created': indicators_created,
                'indicators_removed': indicators_removed,
                'final_indicators_count': final_count,
                'message': 'Исправление выполнено: ' + ', '.join(message_parts),
                'discipline_id': discipline_id,
                'competence_index': competence_index
            }