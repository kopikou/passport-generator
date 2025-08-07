from arim.services import AISServices


class NagrService(object):
    @classmethod
    def get_nagr(cls, user_mira_id):
        data = AISServices.get_uch_nagr_b_person(user_mira_id)
        discpl_list = list(set(i['discpl'] for i in data))
        groups_list = list(set(i['grup'] for i in data))

        result_items = []
        for group in groups_list:
            group_items = []
            for item in data:
                if item['grup'] == group:
                    group_items.append({
                        'discpl': item['discpl'],
                        'hours': item['hours_count'],
                        'formcntr': item['formcntr'],
                    })


        return data