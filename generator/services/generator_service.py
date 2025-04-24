from itertools import groupby

from arim.services import AISServices
from generator.models import PlanLinesLink
from rpd.models import LinesData


class GeneratorService(object):
    @classmethod
    def get_program_list(cls, user_mira_id):
        data = AISServices.get_disciplines_by_person(user_mira_id)

        discpl_list = [i['discpl'] for i in data]
        abbrprofile_list = [i['abbr'] for i in data]
        startyear_list = [i['yr'] for i in data]

        filtered_data = LinesData.objects.filter(dis__in=discpl_list, plan__abbrprofile__in=abbrprofile_list,
                                                 plan__startyear__in=startyear_list,
                                                 plan__file__status=4, synchronize=True).select_related("plan")

        filtered_data_sorted = {f"{i.dis}_{i.plan.abbrprofile}_{i.plan.startyear}": i for i in filtered_data}

        lineslink = PlanLinesLink.objects.filter(mira_id__in=[i['planlin'] for i in data])
        lineslink_sorted = sorted(lineslink, key=lambda x: x.mira_id)
        lineslink_by_id = {i.mira_id: i for i in lineslink_sorted}

        result = []
        for item in data:

            line = filtered_data_sorted.get(f"{item['discpl']}_{item['abbr']}_{item['yr']}")

            if line:

                res = lineslink_by_id.get(item['planlin'], [])

                if not res:
                    res, created = PlanLinesLink.objects.get_or_create(
                        cadmission=item['id_admission'],
                        mira_id=item['planlin'],
                        person=item['mira_id'],
                        defaults={
                            "cadmission": item['id_admission'],
                            "mira_id": item['planlin'],
                            "person": item['mira_id'],
                            "status": PlanLinesLink.StatusChoices.appointed,
                            "planlines_id": line.id,
                        }
                    )

                result.append({
                    **item,
                    "id": res.id,
                    "status": res.status,
                    "status_verbose": res.status_verbose,
                    "kafcode": res.planlines.caf,
                    "discode": res.planlines.newdisid,
                })

        sorted_result = sorted(result, key=lambda x: (x['planlin'], x['mira_id']))
        grouped_result = {key: list(items) for key, items in
                          groupby(sorted_result, key=lambda x: (x['planlin'], x['mira_id']))}

        res = []
        for key, items in grouped_result.items():
            temp = {
                **items[0],
                "type": [i['type'] for i in items],
            }
            res.append(temp)

        return res