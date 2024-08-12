from pprint import pprint

from django.core.management import BaseCommand
from django.db.models import Q

from arim.models import UchPlanPlan, UchPlanLines, UchPlanDiscpl, UchPlanKaf
from arim.services import AISServices
from rpd.models import RPDFile, LinesData, PlanData


class Command(BaseCommand):
    help = "Перенос данных о планах (план, дисциплины, семестры) из системы в АИС"

    def handle(self, *args, **options):

        data = list(RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted))
        # RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted).update(status=RPDFile.StatusChoice.on_synchronize)

        for i in data:
            plan_data = PlanData.objects.filter(file_id=i.id).values()
            line_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id).values()
            semester_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id).values()

            transfer_plan_data = {}
            for plan in plan_data:
                transfer_plan_data = {
                    "species": plan['species'],
                    "studyprog": plan['studyprog'],
                    "fullplanname": plan['planname'],
                    "name": plan['planname'],
                    "kafcode": plan['kafcode'],
                    "lastshifr": plan['lastshifr'],
                    "abbrprofile": plan['abbrprofile'],
                    "startyear": plan['startyear'],
                    "gosdate": plan['gosdate'],
                    "gosdocument": plan['gosdocument'],
                    "gostype": plan['gostype'],
                    "fordel": 'f',
                }


                uchplan, created = UchPlanPlan.objects.get_or_create(
                    species=plan['species'],
                    startyear=plan['startyear'],
                    abbrprofile=plan['abbrprofile'],
                    defaults=transfer_plan_data,
                )

            query = Q()
            for line in line_data:
                query |= Q(name=line['dis'])

            discpl_names = UchPlanDiscpl.objects.filter(query)
            discpl_names = {f"{i['name']}": i for i in discpl_names.values()}

            kaf_codes = UchPlanKaf.objects.all()
            kaf_codes = {i['ckaf2rpgen']: i for i in kaf_codes.values()}

            for line in line_data:

                if not discpl_names.get(line['dis']):
                    disid, created = UchPlanDiscpl.objects.get_or_create(
                        name=line['dis']
                    )
                    disid = disid.id
                else:
                    disid = discpl_names.get(line['dis'])['id']

                transfer_line_data = {
                    "planid_id": uchplan.id,
                    "disid_id": disid,
                    "newdisid": line['newdisid'],
                    "iddis": line['newdisid'],
                    "kompetences": line['kompetences'],
                    "mustbesdudied": line['mustbesdudied'],
                    "hoursinzet": line['hoursinzet'],
                    "kafcode_id": line['caf'],
                    "ckaf": kaf_codes.get(line['caf'], {}).get("ckaf2istu"),
                    "nocalccontrol": line['nocalccontrol'],
                    "fordel": "f",
                    "type": line['type'],
                    "viewpract": line['viewpract'],
                    "viewobject": line['viewobject'],
                }

                lines, created = UchPlanLines.objects.get_or_create(
                    planid_id=uchplan.id,
                    disid_id=transfer_line_data['disid_id'],
                    defaults=transfer_line_data,
                )

                print(transfer_line_data)

            # pprint(plan_data)
            # pprint(line_data)
            # pprint(semester_data)

            # RPDFile.objects.get(id=i.id).update(status=RPDFile.StatusChoice.finished)
