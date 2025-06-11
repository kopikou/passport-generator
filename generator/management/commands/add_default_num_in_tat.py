from itertools import groupby
from pprint import pprint

from django.core.management import BaseCommand

from generator.models import AdditionalInfo
from rpd.models import LinesData, SemesterData


class Command(BaseCommand):
    def handle(self, *args, **options):

        data = AdditionalInfo.objects.filter(type='tat').select_related("planlineslink")

        semesters = SemesterData.objects.filter(planlineid__in=[i.planlineslink.planlines_id for i in data]).values()
        semesters_sorted = sorted(semesters, key=lambda x: x['planlineid_id'])
        semesters_by_planlineid = {key: list(items) for key, items in groupby(semesters_sorted, key=lambda x: x['planlineid_id'])}

        res = []
        for i in data:
            for j in i.value:
                if not 'num' in j:
                    semester = semesters_by_planlineid.get(i.planlineslink.planlines_id, {})
                    if j['type'] in ('philosophy', 'foreign', 'base'):
                        filtered_semesters = semester
                    elif j['type'] != 'krkp':
                        filtered_semesters = list(filter(lambda x: x.get(j['type'], False), semester))
                    else:
                        filtered_semesters = list(filter(lambda x: x.get('kp', False) or x.get('kr', False), semester))

                    for q in filtered_semesters:
                        res.append({
                            "value": {
                                **j,
                                "num": q['num'],
                            },
                            "id": i.id,
                        })

                # if not filtered_semesters:
                #     pprint(j)
                #     pprint(i.planlineslink)
        res_sorted = sorted(res, key=lambda x: x['id'])
        res_grouped = {key: list(items) for key, items in groupby(res_sorted, key=lambda x: x['id'])}

        for key, items in res_grouped.items():
            temp = []
            for i in items:
                temp.append(i['value'])

            instance = AdditionalInfo.objects.get(id=key)
            instance.value = temp
            instance.save()

        print(len(res))


