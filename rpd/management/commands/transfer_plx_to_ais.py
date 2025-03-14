from pprint import pprint

from django.core.management import BaseCommand
from django.db.models import Q

from arim.models import UchPlanPlan, UchPlanLines, UchPlanDiscpl, UchPlanKaf, UchPlanSemestr, BoolChoice, Catadmission, \
    UchPlanFiles
from arim.services import AISServices
from rpd.models import RPDFile, LinesData, PlanData, SemesterData, PlanDocuments


class Command(BaseCommand):
    help = "Перенос данных о планах (план, дисциплины, семестры) из системы в АИС"

    def handle(self, *args, **options):

        data = list(RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted))
        RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted).update(status=RPDFile.StatusChoice.on_synchronize)

        kaf_codes = UchPlanKaf.objects.all()
        kaf_codes = {i['ckaf2rpgen']: i for i in kaf_codes.values()}

        for i in data:
            plan_data = PlanData.objects.filter(file_id=i.id).values()
            line_data = LinesData.objects.filter(plan__file_id=i.id).values()
            semester_data = SemesterData.objects.filter(planlineid__synchronize=True, planlineid__plan__file_id=i.id).values()
            files_data = PlanDocuments.objects.filter(plan__file_id=i.id).values()

            transfer_plan_data = {}
            for plan in plan_data:
                cadmission = Catadmission.objects.get(abbr=plan['abbrprofile'], yr=plan['startyear'])

                transfer_plan_data = {
                    "species": plan['species'],
                    "studyprog": plan['studyprog'],
                    "studyform": plan['studyform'],
                    "fullplanname": plan['planname'],
                    "name": plan['planname'],
                    "kafcode_id": plan['kafcode'],
                    "ckaf": kaf_codes.get('kafcode', None),
                    "lastshifr": plan['lastshifr'],
                    "abbrprofile": plan['abbrprofile'],
                    "cadmission_id": cadmission.id,
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

                PlanData.objects.filter(id=plan['id']).update(mira_id=uchplan.id)

                Catadmission.objects.filter(id=cadmission.id).update(cuchplan_id=uchplan.id)


            for file in files_data:
                transfer_file_data = {
                    "cplan_id": uchplan.id,
                    "name": file['name'],
                    "ctype": file['type'],
                }

                files, created = UchPlanFiles.objects.get_or_create(
                    cplan_id=uchplan.id,
                    name=transfer_file_data['name'],
                    ctype=transfer_file_data['ctype'],
                    defaults=transfer_file_data,
                )

            query = Q()
            for line in line_data:
                query |= Q(name=line['dis'])

            discpl_names = UchPlanDiscpl.objects.filter(query)
            discpl_names = {f"{i['name']}": i for i in discpl_names.values()}

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
                    "fordel": "t" if line['synchronize'] else 'f',
                    "type": line['type'],
                    "viewpract": line['viewpract'],
                    "viewobject": line['viewobject'],
                }

                lines, created = UchPlanLines.objects.get_or_create(
                    planid_id=uchplan.id,
                    disid_id=transfer_line_data['disid_id'],
                    newdisid=transfer_line_data['newdisid'],
                    defaults=transfer_line_data,
                )

                # print(transfer_line_data)

                for semestr in semester_data:
                    if semestr['planlineid_id'] == line['id']:

                        transfer_semester_data = {
                            "planlineid_id": lines.id,
                            "num": semestr['num'],
                            "lekc": semestr['lekc'],
                            "lab": semestr['lab'],
                            "pr": semestr['pr'],
                            "srs": semestr['srs'],
                            "ekzhour": semestr['ekzhour'],
                            "zet": semestr['zet'],
                            "ekz": 't' if semestr['ekz'] else None,
                            "zach": 't' if semestr['zach'] else None,
                            "kp": 't' if semestr['kp'] else None,
                            "kp_hour": semestr['kp_hour'],
                            "kr": 't' if semestr['kr'] else None,
                            "kr_hour": semestr['kr_hour'],
                            "zacho": semestr['zacho'],
                            "eios": semestr['eios'],
                        }

                        semesters, created = UchPlanSemestr.objects.get_or_create(
                            planlineid_id=lines.id,
                            num=transfer_semester_data['num'],
                            defaults=transfer_semester_data,
                        )

            RPDFile.objects.filter(id=i.id).update(status=RPDFile.StatusChoice.finished)
