from datetime import datetime

from arim.services import AISServices
from ind_plan.models import IndPlan


class IndPlanService(object):
    @classmethod
    def get_indPlan(cls, user):
        data = AISServices.get_uch_nagr_by_person(user.userprofile.mira_id)
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
        result_items_preparing = []
        result_items_educ_method_work = []
        result_items_other_works = []
        result_items_work_with_students = []

        ind_plan, created = IndPlan.objects.get_or_create(year=int(data[0]['ddat'].year), user_created=user)

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

        for item in data:
            preparing_items = {
                'labs': 0,  # Проверка отчетов по лабам
                'labs_and_practices': 0,  # Подготовка к лабам и практикам
                'lectures': 0,  # Подготовка к лекциям
            }

            if item['formcntr'] in ['Лаб', 'Прак']:
                preparing_items['labs_and_practices'] += item['hours_count']
                if item['formcntr'] == 'Лаб':
                    preparing_items['labs'] += item['hours_count']
            elif item['formcntr'] == 'Лек':
                preparing_items['lectures'] += item['hours_count']

            result_items_preparing.append({
                'discpl': item['discpl'],
                'grup': item['grup'],
                'kurs': item['kurs'],
                'sem': item['sem'],
                'items': preparing_items,
            })

        return {
            'uch_nagr': result_items_uch_nagr,
            'preparing': result_items_preparing,
        }