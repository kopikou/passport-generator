from json import JSONDecodeError

import pendulum
import requests
from django.conf import settings
from django.db.models import Q

from app.utils import cache_function, Mira
from arim.models import UistLicense, OborudData, BoolChoice, UchPlanKaf, Catadmission, CatFaculty, CatKaf, RpdUsers, \
    UchPlanPlan


class AISServices(object):

    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_admissionn_info(pk):

        data = Catadmission.objects.filter(
            id=pk,
        ).select_related("ckaf", "cfac").values(
            'id',
            'yr',
            'abbr',
            'cuchplan_id',
            'spec_name',
            'direct_name',
            'kvalif_name',
            'ckaf_id',
            'cfac_id',
            'ckaf__name',
            'cfac__name',
            'cadmkind',
            'cadmkind__name',
            'cadmkind__name_prof',
            'cdirection',
            'cdirection__name',
            'cdirection__cod',
            'cfob',
            'cfob__name',
        )

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
    def get_admission_list_by_person(id):

        cfac = CatFaculty.objects.filter(cdean=id)
        ckaf = CatKaf.objects.filter(czav=id)
        adm_user = RpdUsers.objects.filter(cperson=id).first()

        now = pendulum.now().start_of("day")
        left_time = now.add(years=-6).year
        data = None
        query = Q()
        if adm_user:
            if adm_user.isadmin == 't':
                query |= Q(fordel='f', startyear__gte=left_time)
            elif adm_user.isspo == 't':
                query |= Q(fordel='f', startyear__gte=left_time, ckaf__in=[1988587, 1988517, 1988516])
        elif cfac:
            uchplans = [i.cuchplan for i in Catadmission.objects.filter(cfac__in=[j.id for j in cfac], active='t', yr__gte=left_time, cuchplan__isnull=False)]
            query |= Q(fordel='f', id__in=[i.id for i in uchplans])
        elif ckaf:
            query |= Q(fordel='f', ckaf__in=[i.id for i in ckaf], startyear__gte=left_time)
        else:
            query |= Q(fordel='f', cperson=id, startyear__gte=left_time)

        data = UchPlanPlan.objects.filter(query).values()

        return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_disciplines_by_person(id):

        q = f"""exec rpd_list_for_person {int(id)}"""

        # r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
        #     "q": q
        # }, proxies={
        #     "http": "",
        #     "https": "",
        # })
        #
        # data = r.json()['RecordSet']

        data = Mira.fetch(q)

        return data

    @staticmethod
    def get_asp_napr_detail(id):

        data = Mira.fetch(f"""
                SELECT 
                k.name AS ckaf, 
                up.species, 
                f.name AS cfac, 
                YEAR(c.dateend) - YEAR(c.datebegin) AS range, 
                c.datebegin, 
                c.dateend, 
                fo.name AS cfob,
                up.startyear,
                f.dean,
                k.zav,
                c.yr,
                p.name AS rop
                FROM uchplan_plan up
                left JOIN catadmission c ON c.id = up.cadmission
                left JOIN catkaf k ON up.ckaf = k.id
                LEFT JOIN catfaculty f ON f.id = k.cfac
                left JOIN cl$fob fo ON c.cfob = fo.id
                LEFT join catperson p ON up.cperson = p.id
                where up.id = %s
            """, [id])

        return data

    @staticmethod
    def get_asp_napr(year, user):

        data = Mira.fetch(f"""
            SELECT c.name, p.species, p.id FROM uchplan_plan p
            LEFT JOIN catadmission c on p.cadmission = c.id
            WHERE startyear = %s and c.cadmkind = 5 and cperson = %s 
            """, [year, user])

        return data


    @staticmethod
    def search_software(val):

        data = UistLicense.objects.filter(clicense__name__contains=val).values(
            "id",
            "cnt",
            "clicense__name"
        )[:100]

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
        )[:100]

        return data
