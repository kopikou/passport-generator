from arim.services import AISServices


class NagrService(object):
    @classmethod
    def get_nagr(cls, user_mira_id):
        data = AISServices.get_uch_nagr_b_person(user_mira_id)
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
            items = []
            podg_items = {
                'Лаб': 0,
                'Лек': 0,
            }
            for item in data:
                if item['discpl'] == discpl:
                    items.append({
                        'grup': item['grup'],
                        'hours_count': item['hours_count'],
                        'formcntr': categories[item['formcntr']],
                        'direct': item['direct'],
                        'sem': item['sem'],
                        'kurs': item['kurs'],
                        'discpl': item['discpl'],
                    })
                    # podg_items[item['formcntr']] += item['hours_count']

            result_items_uch_nagr.append({
                'discpl': discpl,
                'items': items,
            })

        return result_items_uch_nagr