from itertools import groupby
from pprint import pprint

import pandas as pd
from django.core.management import BaseCommand
from django.db import connections
from openpyxl.workbook import Workbook

from app.utils import dictfetchall
from generator.models import PlanLinesLink


class Command(BaseCommand):
    def handle(self, *args, **options):

        exception_names = ['Microsoft', 'Adobe', 'Abbyy', 'AutoDesk', 'MS Office', 'MathLab', 'Visio', 'Autodesk', 'Coreldraw ABBYY']

        mira_data = []

        with connections['mira'].cursor() as cursor:

            sql = f"""
                    select 
                    COALESCE(s.code + ' ' + s.name, s1.code + ' ' + s1.name) as spec,
                    COALESCE(s.name, s1.name) as name,
                    COALESCE(s.id, s1.id) as id,
                    count(*) AS cnt
                    from catstud stud
                    left join catadmission a on a.id = stud.cadmission
                    left join cl$spec s on s.id = a.cspec
                    left join cl$spec s1 on s1.id = a.cprofili
                    where stud.cstudstate in (1, 10, 21, 5)
                    and a.cadmkind not in (4)
                    GROUP by s.code, s.name, s1.code, s1.name, s.id, s1.id
                    order by 1
                """
            cursor.execute(sql, [])
            mira_data = dictfetchall(cursor)


        admissions= []

        with connections['mira'].cursor() as cursor:
            sql = f"""
                SELECT id, cspec from catadmission where yr = 2025
                and cspec is not null
            """

            cursor.execute(sql, [])
            admissions = dictfetchall(cursor)

        admissions_sorted = sorted(admissions, key=lambda x: x['cspec'])
        admissions_by_spec = {key: list(items) for key, items in groupby(admissions_sorted, key=lambda x: x['cspec'])}

        planlines = PlanLinesLink.objects.prefetch_related('additional_info').select_related('planlines').all()
        planlines_sorted = sorted(planlines, key=lambda x: x.cadmission)
        planlines_grouped = {key: list(items) for key, items in groupby(planlines_sorted, key=lambda x: x.cadmission)}

        data = []
        discpls = []
        for spec in mira_data:
            tmp = []
            discpls = []
            for admission in admissions_by_spec.get(spec['id'], []):
                for planline in planlines_grouped.get(admission['id'], []):
                    discpls.append(planline.planlines.dis)
                    for val in planline.additional_info.all():
                        if val.type == 'software':
                            for app in val.value:
                                if 'clicense__type' not in app:
                                    find = False
                                    for exception_name in exception_names:
                                        if exception_name.lower() in app['clicense__name'].lower():
                                            find = True

                                    if not find:
                                        tmp.append(app['clicense__name'])

            data.append({
                'Специальность': spec['spec'],
                'Наименование': spec['name'],
                'Кол-во студентов': spec['cnt'],
                'Приложения': ', '.join(set(tmp)) if len(tmp) > 0 else '',
                'Дисциплина': ', '.join(set(discpls)) if len(discpls) > 0 else '',
            })

        df = pd.DataFrame(data)
        df.to_excel("test.xlsx", index=False)

        print(data)