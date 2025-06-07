from cgi import logfp
from itertools import groupby
from pprint import pprint

from django.core.management import BaseCommand

from generator.models import AdditionalInfo
from rpd.models import LinesData, SemesterData


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = AdditionalInfo.objects.filter(type='fos').select_related("planlineslink", "planlineslink__planlines__plan")

        semesters = SemesterData.objects.filter(planlineid__in=[i.planlineslink.planlines_id for i in data]).values()
        semesters_sorted = sorted(semesters, key=lambda x: x['planlineid_id'])
        semesters_by_planlineid = {key: list(items) for key, items in
                                   groupby(semesters_sorted, key=lambda x: x['planlineid_id'])}

        res = []

        for i in data:
            yearlabel = 'учебный год' if i.planlineslink.planlines.plan.studyform == 'Заочная' else 'семестр'

            for j in i.value:
                if not 'num' in j:
                    semesters = semesters_by_planlineid.get(i.planlineslink.planlines_id, {})

                    for sem in semesters:
                        res.append({
                            "value": {
                                **j,
                                "title": f"{yearlabel} {sem['num']} | {j['title']}",
                                "num": sem['num'],
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

        # print(res)
        print(f" rows count: {len(res)}")
