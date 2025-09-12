from datetime import datetime

from arim.services import AISServices
from auths.models import UserProfile
from ind_plan.models import IndPlan, PlanWork, PlanWorkType, PreparingCoefficient


class IndPlanService(object):
    @classmethod
    def get_indPlan(cls, plan_id):
        ind_plan = IndPlan.objects.get(pk=plan_id)
        if ind_plan is not None:
            mira_id = ind_plan.user_created.userprofile.mira_id
            data = AISServices.get_uch_nagr_by_person(mira_id)
            discpl_list = list(set(i['discpl'] for i in data))

            if ind_plan.zav is None:
                ind_plan.zav = UserProfile.objects.get(mira_id=data[0]['zav_id']).user
                ind_plan.save()

            categories = {
                'Лек': 'лекции',
                'Прак': 'практика',
                'ЗачОц': 'диф. зачет',
                'Лаб': 'лабораторные',
                'Экз': 'экзамен',
                'Зач': 'зачет',
                'Конс': 'консультации',
                'ПрПр': 'производственная практика',
                'Дип': 'диплом',
                'КурсП': 'курсовой проект',
                'КурсР': 'курсовая работа',
                'Контр': 'контрольная',
                'ГЭК': 'ГЭК',
                'РГР': 'РГР',
                'Аспир': 'Аспир',
                'Маг': 'Маг',
            }

            result_items_uch_nagr = []
            result_items_preparing = PlanWork.objects.all().filter(plan=ind_plan, type=PlanWorkType.preparing)
            result_items_educ_method_work = PlanWork.objects.all().filter(plan=ind_plan, type=PlanWorkType.educ_method)
            result_items_other_works = []
            result_items_work_with_students = PlanWork.objects.all().filter(plan=ind_plan, type=PlanWorkType.work_with_students)

            for discpl in discpl_list:
                uch_nagr_items = []
                for item in data:
                    if item['discpl'] == discpl:
                        uch_nagr_items.append({
                            'grup': item['grup'],
                            'hours_count': item['hours_count'],
                            'formcntr': categories[item['formcntr']],
                            'direct': item['direct'],
                            'sem': item['sem'],
                            'kurs': item['kurs'],
                            'discpl': item['discpl'],
                        })

                result_items_uch_nagr.append({
                    'discpl': discpl,
                    'items': uch_nagr_items,
                })

            preparing_items = {}
            for item in data:
                if item['formcntr'] in ['Лек', 'Лаб', 'Прак'] and item['discpl'] in preparing_items.keys():
                    if  item['formcntr'] in preparing_items[item['discpl']].keys():
                        preparing_items[item['discpl']][item['formcntr']] += float(item['hours_count'])
                    else:
                        preparing_items[item['discpl']][item['formcntr']] = float(item['hours_count'])
                elif item['formcntr'] in ['Лек', 'Лаб', 'Прак'] and item['discpl'] not in preparing_items.keys():
                    preparing_items[item['discpl']] = {
                        item['formcntr']: float(item['hours_count'])
                    }

            for key in preparing_items:
                if 'Лек' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Подготовка к лекциям')

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Подготовка к лекциям',
                            hours_count=preparing_items[key]['Лек'] * PreparingCoefficient.old_lectures.value,
                            max_hours_count = preparing_items[key]['Лек'] * PreparingCoefficient.old_lectures.value,
                            is_new=False
                        )

                        new_item.save()
                    else:
                        if ((not item_preparing[0].is_new
                             and item_preparing[0].max_hours_count != preparing_items[key]['Лек'] * PreparingCoefficient.old_lectures.value)
                                or (item_preparing[0].is_new
                                    and item_preparing[0].max_hours_count != preparing_items[key]['Лек'] * PreparingCoefficient.new_lectures.value)):
                            if not item_preparing[0].is_new:
                                item_preparing[0].max_hours_count = preparing_items[key]['Лек'] * PreparingCoefficient.old_lectures.value
                                item_preparing[0].hours_count = preparing_items[key]['Лек'] * PreparingCoefficient.old_lectures.value
                                item_preparing[0].save()
                            else:
                                item_preparing[0].max_hours_count = preparing_items[key]['Лек'] * PreparingCoefficient.new_lectures.value
                                item_preparing[0].hours_count = preparing_items[key]['Лек'] * PreparingCoefficient.new_lectures.value
                                item_preparing[0].save()

                if 'Лаб' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Проверка отчетов по лабораторным работам')

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Проверка отчетов по лабораторным работам',
                            hours_count=preparing_items[key]['Лаб'] * PreparingCoefficient.check_labs.value,
                            max_hours_count = preparing_items[key]['Лаб'] * PreparingCoefficient.check_labs.value
                        )

                        new_item.save()
                    else:
                        if item_preparing[0].max_hours_count != preparing_items[key]['Лаб'] * PreparingCoefficient.check_labs.value:
                            item_preparing[0].max_hours_count = preparing_items[key]['Лаб'] * PreparingCoefficient.check_labs.value
                            item_preparing[0].hours_count = preparing_items[key]['Лаб'] * PreparingCoefficient.check_labs.value
                            item_preparing[0].save()

                if 'Лаб' in preparing_items[key].keys() or 'Прак' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Подготовка к лабораторным, практическим, семинарским занятиям')

                    sum_hours = ((preparing_items[key]['Лаб'] if 'Лаб' in preparing_items[key].keys() else 0)
                                 + (preparing_items[key]['Прак'] if 'Прак' in preparing_items[key].keys() else 0))

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Подготовка к лабораторным, практическим, семинарским занятиям',
                            hours_count=sum_hours * PreparingCoefficient.old_labs_and_practices.value,
                            max_hours_count = sum_hours * PreparingCoefficient.old_labs_and_practices.value,
                            is_new=False
                        )

                        new_item.save()
                    else:
                        if ((not item_preparing[0].is_new
                             and item_preparing[0].max_hours_count != sum_hours * PreparingCoefficient.old_labs_and_practices.value)
                                or (item_preparing[0].is_new
                                    and item_preparing[0].max_hours_count != sum_hours * PreparingCoefficient.new_labs_and_practices.value)):
                            if not item_preparing[0].is_new:
                                item_preparing[0].max_hours_count = sum_hours * PreparingCoefficient.old_labs_and_practices.value
                                item_preparing[0].hours_count = sum_hours * PreparingCoefficient.old_labs_and_practices.value
                                item_preparing[0].save()
                            else:
                                item_preparing[0].max_hours_count = sum_hours * PreparingCoefficient.new_labs_and_practices.value
                                item_preparing[0].hours_count = sum_hours * PreparingCoefficient.new_labs_and_practices.value
                                item_preparing[0].save()

            result_items_preparing = PlanWork.objects.all().filter(plan=ind_plan, type=PlanWorkType.preparing)
            return {
                'uch_nagr': result_items_uch_nagr,
                'preparing': result_items_preparing,
                'educ_method': result_items_educ_method_work,
                'other_works': result_items_other_works,
                'work_with_students': result_items_work_with_students,
                'plan': ind_plan,
            }
        else:
            return {
                'uch_nagr': [],
                'preparing': [],
                'educ_method': [],
                'other_works': [],
                'work_with_students': [],
                'plan': ind_plan,
            }