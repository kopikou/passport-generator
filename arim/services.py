from json import JSONDecodeError

import pendulum
import requests
from django.conf import settings
from django.db.models import Q

from app.utils import cache_function
from arim.models import UistLicense, OborudData, BoolChoice, UchPlanKaf, Catadmission


class AISServices(object):

    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_admissionn_info(pk):

        data = Catadmission.objects.filter(
            id=pk,
        ).values()

        return data

    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_kaf_codes():


        data = UchPlanKaf.objects.extra(
            select={
                "value": "ckaf2rpgen",
                "label": "name2rpgen",
                "ckaf2istu": "ckaf2istu",
            }
        ).values()

        # q = """
        #     SELECT ckaf2rpgen as value, name2rpgen as label, ckaf2istu FROM dbo.uchplan_kaf ORDER BY name2rpgen
        #     """
        #
        # r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
        #     "q": q
        # }, proxies={
        #     "http": "",
        #     "https": "",
        # })
        #
        # data = r.json()['RecordSet']

        return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_disciplines_by_person(id):

        q = f"""exec rpd_list_for_person {int(id)}"""

        r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
            "q": q
        }, proxies={
            "http": "",
            "https": "",
        })

        data = r.json()['RecordSet']

        return data

    @staticmethod
    def search_software(val):

        data = UistLicense.objects.filter(clicense__name__contains=val).values(
            "id",
            "cnt",
            "clicense__name"
        )

        return data

    @staticmethod
    def search_oborud(val, type, caf):

        query = Q()
        query_second = Q()
        query_third = Q()

        query |= Q(caud__name__contains=val)
        query |= Q(name__contains=val)
        query |= Q(inv__contains=val)

        if type != 3:
            сkaf = UchPlanKaf.objects.get(ckaf2rpgen=caf)
            query_second |= Q(caud__ckaf=сkaf.ckaf2istu)

            if type == 1:
                query_third |= Q(caud__cnazn=7)
                query_third |= Q(ismobile=BoolChoice.t)
                query_third |= Q(caud__ckaf=сkaf.ckaf2istu)

        data = OborudData.objects.filter(query, query_second, query_third).values(
            'id',
            'name',
            'inv',
            'caud__name',
        )

        return data
