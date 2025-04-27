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
            'ckaf__ccatdep__nameshort',
            'cfac__name',
            'cadmkind',
            'cadmkind__name',
            'cadmkind__name_prof',
            'cdirection',
            'cdirection__name',
            'cdirection__cod',
            'cspec',
            'cspec__name',
            'cspec__code',
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
    def get_practice_by_person(id):

        q = f"""

            declare @id INT;

            SET @id = %s

            SELECT
            DISTINCT
            t.discpl,
            t.id_discpl,
            t.planlin,
            t.abbr,
            t.yr,
            t.id_admission,
            t.mira_id,
            cp.name AS person,
            t.type AS type
            FROM (
            SELECT d.name as discpl,d.id as id_discpl, u.id as planlin, p.abbrprofile as abbr, p.startyear as yr, p.cadmission as id_admission,  p.cperson AS mira_id, 'person' AS type  -- Преподаватель
            FROM uchplan_lines u
            left join uchplan_discpl d on (u.disid = d.id)
            left join uchplan_plan p on (p.id = u.planid)
            where p.cperson = @id and p.fordel = 'f' and u.fordel = 'f' and u.type = 3

            ) t
            LEFT JOIN dbo.catperson cp ON cp.id = t.mira_id
            WHERE t.mira_id IS NOT NULL
            """

        # r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
        #     "q": q
        # }, proxies={
        #     "http": "",
        #     "https": "",
        # })
        #
        # data = r.json()['RecordSet']

        data = Mira.fetch(q, [int(id)])

        return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_disciplines_by_person(id):

        # q = f"""exec rpd_list_for_person %s"""
        q = f"""

            declare @id INT;

            SET @id = %s

            SELECT
            DISTINCT
            t.discpl,
            t.id_discpl,
            t.planlin,
            t.abbr,
            t.yr,
            t.id_admission,
            t.mira_id,
            cp.name AS person,
            t.type AS type
            FROM (
            SELECT d.name as discpl,d.id as id_discpl, u.id as planlin, p.abbrprofile as abbr, p.startyear as yr, p.cadmission as id_admission,  u.cperson AS mira_id, 'person' AS type  -- Преподаватель
            FROM uchplan_lines u
            left join uchplan_discpl d on (u.disid = d.id)
            left join uchplan_plan p on (p.id = u.planid)
            where u.cperson = @id and p.fordel = 'f' and u.fordel = 'f' and u.type != 3

            UNION ALL

            select d.name as discpl,d.id as id_discpl, u.id as planlin, p.abbrprofile as abbr, p.startyear as yr, p.cadmission as id_admission, u.cperson AS mira_id, 'zav' AS type -- Заведующий кафедры
            FROM uchplan_lines u
            left join uchplan_discpl d on (u.disid = d.id)
            left join uchplan_plan p on (p.id = u.planid)
            LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
            where u.ckaf in (SELECT id FROM dbo.catkaf WHERE czav = @id AND isreal = 't') and p.fordel = 'f' and u.fordel = 'f' and  u.type != 3

            UNION ALL

            select d.name as discpl,d.id as id_discpl, u.id as planlin, p.abbrprofile as abbr, p.startyear as yr, p.cadmission as id_admission,  u.cperson AS mira_id, 'fac' AS type -- Заведующий факультета
            FROM uchplan_lines u
            left join uchplan_discpl d on (u.disid = d.id)
            left join uchplan_plan p on (p.id = u.planid)
            LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
            where a.cfac in (SELECT id FROM dbo.catfaculty WHERE cdean = @id AND realfac = 't') and p.fordel = 'f' and u.fordel = 'f' and  u.type != 3

            UNION ALL

            SELECT DISTINCT d.name as discpl,d.id as id_discpl, u.id as planlin, p.abbrprofile as abbr, p.startyear as yr, p.cadmission as id_admission,  u.cperson AS mira_id, 'rop' AS type  -- Руководитель программы
            FROM uchplan_lines u
            left join uchplan_discpl d on (u.disid = d.id)
            left join uchplan_plan p on (p.id = u.planid)
            LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
            where p.cperson = @id
            --a.cspec in (SELECT id FROM dbo.[cl$spec] WHERE cprepod = @id) OR a.cprofili in (SELECT id FROM dbo.[cl$spec] WHERE cprepod = @id)
            --OR a.cdirection in (SELECT id FROM dbo.[cl$direction] WHERE cperson = @id)
            AND p.fordel = 'f' and u.fordel = 'f' and  u.type != 3

            ) t
            LEFT JOIN dbo.catperson cp ON cp.id = t.mira_id
            WHERE t.mira_id IS NOT NULL
            """

        # r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
        #     "q": q
        # }, proxies={
        #     "http": "",
        #     "https": "",
        # })
        #
        # data = r.json()['RecordSet']

        data = Mira.fetch(q, [int(id)])

        return data

    @staticmethod
    def get_asp_old_plans(id):

        query = f"""
            select p2.id, p2.abbrprofile, p2.startyear, p2.species from uchplan_plan p
            left join uchplan_plan p2 on p.abbrprofile = p2.abbrprofile
            where p.id = %s and p2.fordel = 'f' and p2.id <> %s
            order by p2.startyear
            """

        data = Mira.fetch(query, [id, id])

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
    def get_all_asp(year):

        data = Mira.fetch(f"""
            SELECT c.name, p.species, p.id FROM uchplan_plan p
            LEFT JOIN catadmission c on p.cadmission = c.id
            WHERE startyear = %s and c.cadmkind = 5
            """, [year])

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

    @staticmethod
    def get_old_rpd_list(id):

        query = f"""
            select p2.abbrprofile, p2.startyear, l2.id, p2.species from uchplan_lines l
            left join uchplan_plan p on p.id = l.planid
            left join uchplan_plan p2 on p2.abbrprofile = p.abbrprofile
            left join uchplan_lines l2 on l2.planid = p2.id
			left join uchplan_discpl d on d.id = l.disid
			left join uchplan_discpl d2 on d2.id = l2.disid
            where l.id = %s and p2.fordel = 'f' and l2.fordel = 'f' and l2.id <> %s and d.name = d2.name
        """

        data = Mira.fetch(query, [id, id])

        return data