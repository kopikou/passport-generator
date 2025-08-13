from arim.services import AISServices


class IndPlanService(object):
    @classmethod
    def get_indPlan(cls, user_mira_id):
        data = AISServices.get_indPlan_by_person(user_mira_id)
        discpl_list = list(set(i['discpl'] for i in data))
        groups_list = list(set(i['grup'] for i in data))

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
        result_items_podg = []
        result_items_uch_met_rab = []
        result_items_others = []
        result_items_ob_rab = []

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
            podg_items = {
                'labs': 0,  # Проверка отчетов по лабам
                'labs_and_practices': 0,  # Подготовка к лабам и практикам
                'lectures': 0,  # Подготовка к лекциям
            }

            if item['formcntr'] in ['Лаб', 'Прак']:
                podg_items['labs_and_practices'] += item['hours_count']
                if item['formcntr'] == 'Лаб':
                    podg_items['labs'] += item['hours_count']
            elif item['formcntr'] == 'Лек':
                podg_items['lectures'] += item['hours_count']

            result_items_podg.append({
                'discpl': item['discpl'],
                'grup': item['grup'],
                'kurs': item['kurs'],
                'sem': item['sem'],
                'items': podg_items,
            })

        return {
            'uch_nagr': result_items_uch_nagr,
            'podg': result_items_podg,
        }