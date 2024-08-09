from pprint import pprint

from django.core.management import BaseCommand

from arim.models import UchPlanPlan
from arim.services import AISServices
from rpd.models import RPDFile, LinesData, PlanData


class Command(BaseCommand):
    help = "Перенос данных о планах (план, дисциплины, семестры) из системы в АИС"

    def handle(self, *args, **options):

        data = list(RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted))
        # RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted).update(status=RPDFile.StatusChoice.on_synchronize)

        for i in data:
            plan_data = PlanData.objects.filter(file_id=i.id)
            line_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id)
            semester_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id)

            transfer_plan_data = {}
            for i in plan_data:
                transfer_plan_data = {
                    "species": i.species,
                    "studyprog": i.studyprog,
                    "fullplanname": i.planname,
                    "name": i.planname,
                    "kafcode": i.kafcode,
                    "lastshifr": i.lastshifr,
                    "abbrprofile": i.abbrprofile,
                    "startyear": i.startyear,
                    "gosdate": i.gosdate,
                    "gosdocument": i.gosdocument,
                    "gostype": i.gostype,
                    "fordel": 'f',
                }

            check = ""

            plan_mira_id = 0  # берем мира ид если он Есть

            pprint(plan_data)
            pprint(line_data)
            pprint(semester_data)

            # RPDFile.objects.get(id=i.id).update(status=RPDFile.StatusChoice.finished)
