from datetime import datetime

from arim.services import AISServices
from ind_plan.models import IndPlan, PlanWork, PlanWorkType
from ind_plan.serializers import PlanWorkSerializer


class IndPlanService(object):
    @classmethod
    def get_indPlan(cls, plan_id):
        ind_plan = IndPlan.objects.get(pk=plan_id)
        if (ind_plan is not None):
            mira_id = ind_plan.user_created.userprofile.mira_id
            data = AISServices.get_uch_nagr_by_person(mira_id)
            discpl_list = list(set(i['discpl'] for i in data))

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

            coefficients_for_new = {
                'labs_and_practices': 2.0,
                'lectures': 3.0,
            }

            coefficients_for_old = {
                'labs_and_practices': 0.5,
                'lectures': 1.0,
            }

            general_coefficients = {
                'check_labs': 0.2,
            }

            for key in preparing_items:
                if 'Лек' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Подготовка к лекциям')

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Подготовка к лекциям',
                            hours_count=preparing_items[key]['Лек'] * coefficients_for_old['lectures'],
                            max_hours_count = preparing_items[key]['Лек'] * coefficients_for_old['lectures'],
                            is_new=False
                        )

                        new_item.save()
                    else:
                        if ((not item_preparing[0].is_new
                             and item_preparing[0].max_hours_count != preparing_items[key]['Лек'] * coefficients_for_old['lectures'])
                                or (item_preparing[0].is_new
                                    and item_preparing[0].max_hours_count != preparing_items[key]['Лек'] * coefficients_for_new['lectures'])):
                            if not item_preparing[0].is_new:
                                item_preparing[0].max_hours_count = preparing_items[key]['Лек'] * coefficients_for_old['lectures']
                                item_preparing[0].hours_count = preparing_items[key]['Лек'] * coefficients_for_old['lectures']
                                item_preparing[0].save()
                            else:
                                item_preparing[0].max_hours_count = preparing_items[key]['Лек'] * coefficients_for_new['lectures']
                                item_preparing[0].hours_count = preparing_items[key]['Лек'] * coefficients_for_new['lectures']
                                item_preparing[0].save()

                if 'Лаб' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Проверка отчетов по лабораторным работам')

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Проверка отчетов по лабораторным работам',
                            hours_count=preparing_items[key]['Лаб'] * general_coefficients['check_labs'],
                            max_hours_count = preparing_items[key]['Лаб'] * general_coefficients['check_labs'],
                            is_new=False
                        )

                        new_item.save()
                    else:
                        if item_preparing[0].max_hours_count != preparing_items[key]['Лаб'] * general_coefficients['check_labs']:
                            item_preparing[0].max_hours_count = preparing_items[key]['Лаб'] * general_coefficients['check_labs']
                            item_preparing[0].hours_count = preparing_items[key]['Лаб'] * general_coefficients['check_labs']
                            item_preparing[0].save()

                if 'Лаб' in preparing_items[key].keys() or 'Прак' in preparing_items[key].keys():
                    item_preparing = result_items_preparing.filter(name = key + ': Подготовка к лабораторным, практическим, семинарским занятиям')

                    sum_hours = (preparing_items[key]['Лаб'] if 'Лаб' in preparing_items[key].keys() else 0)  + (preparing_items[key]['Прак'] if 'Прак' in preparing_items[key].keys() else 0)

                    if len(item_preparing) == 0:
                        new_item = PlanWork.objects.create(
                            plan=ind_plan,
                            type=PlanWorkType.preparing,
                            name=key + ': Подготовка к лабораторным, практическим, семинарским занятиям',
                            hours_count=sum_hours * coefficients_for_old['labs_and_practices'],
                            max_hours_count = sum_hours * coefficients_for_old['labs_and_practices'],
                            is_new=False
                        )

                        new_item.save()
                    else:
                        if ((not item_preparing[0].is_new
                             and item_preparing[0].max_hours_count != sum_hours * coefficients_for_old['labs_and_practices'])
                                or (item_preparing[0].is_new
                                    and item_preparing[0].max_hours_count != sum_hours * coefficients_for_new['labs_and_practices'])):
                            if not item_preparing[0].is_new:
                                item_preparing[0].max_hours_count = sum_hours * coefficients_for_old['labs_and_practices']
                                item_preparing[0].hours_count = sum_hours * coefficients_for_old['labs_and_practices']
                                item_preparing[0].save()
                            else:
                                item_preparing[0].max_hours_count = sum_hours * coefficients_for_new['labs_and_practices']
                                item_preparing[0].hours_count = sum_hours * coefficients_for_new['labs_and_practices']
                                item_preparing[0].save()

            result_items_preparing = PlanWork.objects.all().filter(plan=ind_plan, type=PlanWorkType.preparing)
            # for item in data:
            #     preparing_items = {
            #         'labs': 0,  # Проверка отчетов по лабам
            #         'labs_and_practices': 0,  # Подготовка к лабам и практикам
            #         'lectures': 0,  # Подготовка к лекциям
            #     }
            #
            #     if item['formcntr'] in ['Лаб', 'Прак']:
            #         preparing_items['labs_and_practices'] += item['hours_count']
            #         if item['formcntr'] == 'Лаб':
            #             preparing_items['labs'] += item['hours_count']
            #     elif item['formcntr'] == 'Лек':
            #         preparing_items['lectures'] += item['hours_count']
            #
            #     result_items_preparing.append({
            #         'discpl': item['discpl'],
            #         'grup': item['grup'],
            #         'kurs': item['kurs'],
            #         'sem': item['sem'],
            #         'items': preparing_items,
            #     })

            serializer = PlanWorkSerializer(result_items_preparing, many=True)

            return {
                'uch_nagr': result_items_uch_nagr,
                'preparing': serializer.data,
                'educ_method': result_items_educ_method_work,
                'other_works': result_items_other_works,
                'work_with_students': result_items_work_with_students,
            }
        else:
            return {
                'uch_nagr': [],
                'preparing': [],
                'educ_method': [],
                'other_works': [],
                'work_with_students': [],
            }