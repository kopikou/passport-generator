from pprint import pprint

from django.core.management import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm

from arim.models import UchPlanPlan, UchPlanSemestr
from rpgen.models import Plan


class Command(BaseCommand):
    def handle(self, *args, **options):

        plans = Plan.objects.prefetch_related('planlines_set', 'planlines_set__semestr_set').filter(startyear__lte=2024)

        for plan in tqdm(plans):
            for line in plan.planlines_set.all():
                for semester in line.semestr_set.all():
                    data = {
                        'planlineid_id': semester.planlineid_id,
                        'num': semester.num,
                        'lekc': semester.lekc,
                        'lab': semester.lab,
                        'pr': semester.pr,
                        'srs': semester.srs,
                        'ekzhour': semester.ekzhour,
                        'zet': semester.zet,
                        'ekz': 't' if semester.ekz else 'f' ,
                        'zach': 't' if semester.zach else 'f' ,
                        'kp': 't' if semester.kp else 'f',
                        'kp_hour': semester.kp_hour,
                        'kr': 't' if semester.kr else 'f',
                        'kr_hour': semester.kr_hour,
                        'zacho': semester.zacho,
                        'eios': semester.eios,
                    }

                    try:
                        sem, created = UchPlanSemestr.objects.get_or_create(
                            num=semester.num,
                            planlineid_id=semester.planlineid_id,
                            defaults=data,
                        )

                        # print(sem, created)
                    except IntegrityError as e:
                        print(semester.planlineid_id)
                        print(e)
