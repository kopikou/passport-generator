from json import JSONDecodeError

import pendulum
import requests
from django.conf import settings
from django.db.models import Q

from app.utils import cache_function, Mira
from arim.models import UistLicense, OborudData, BoolChoice, UchPlanKaf, Catadmission, CatFaculty, CatKaf, RpdUsers, \
    UchPlanPlan, CatPerson
from generator.models import PlanLinesLink


class AISServices(object):

    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_admissionn_info(pk):

        data = Catadmission.objects.filter(
            id=pk,
        ).values(
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

        admin = False

        now = pendulum.now().start_of("day")
        left_time = now.add(years=-6).year
        query = Q(fordel='f', startyear__gte=left_time)
        if adm_user:
            admin = True
            if adm_user.isspo == 't':
                query &= Q(ckaf__in=[1988587, 1988517, 1988516])
            if adm_user.cfac_id:
                uchplans = [i.cuchplan for i in
                            Catadmission.objects.filter(cfac=adm_user.cfac_id, active='t', yr__gte=left_time,
                                                        cuchplan__isnull=False)]
                query &= Q(id__in=[i.id for i in uchplans])
        else:
            query &= Q(cperson=id)

        if cfac:
            uchplans = [i.cuchplan for i in
                        Catadmission.objects.filter(cfac__in=[j.id for j in cfac], active='t', yr__gte=left_time,
                                                    cuchplan__isnull=False)]
            query |= Q(id__in=[i.id for i in uchplans])
        if ckaf:
            query |= Q(ckaf__in=[i.id for i in ckaf], fordel='f', startyear__gte=left_time)

        data = [i for i in UchPlanPlan.objects.filter(query).values()]

        for i in range(len(data)):
            data[i] = {
                **data[i],
                "admin": admin,
                "can_upload": adm_user.can_upload if adm_user else 'f'
            }

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
    def get_plan_users_info(plan_link_id):
        plan_link_mira_id = PlanLinesLink.objects.filter(id=plan_link_id).values('mira_id').first()
        data = None
        if plan_link_mira_id:
            q = f"""
                SELECT u.cperson AS razrab
                , ck.czav AS zavkaf
                , p.cperson AS rop
                , f.cdean AS fac
                FROM uchplan_lines u
                    LEFT JOIN uchplan_discpl d ON u.disid = d.id
                    LEFT JOIN uchplan_plan p ON p.id = u.planid
                    LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
                    LEFT JOIN dbo.catkaf ck ON  ck.id = u.ckaf
                    LEFT JOIN dbo.catfaculty f ON f.id = a.cfac
                    LEFT JOIN dbo.catperson cp1 ON cp1.id = u.cperson
                    LEFT JOIN dbo.catperson cp2 ON cp2.id = p.cperson
                WHERE 
                    u.cperson IS NOT NULL 
                    AND p.fordel = 'f' 
                    AND u.fordel = 'f' 
                    AND u.id = %s
                """

            data = Mira.fetch(q, [int(plan_link_mira_id['mira_id'])])
            return data[0]

        # return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_disciplines_by_person(id, year):
        q = f"""

            declare @id INT;
            declare @year INT;
            declare @cfacADM int;
            DECLARE @adm varchar;
            SET @id = %s;
            SET @year = %s;
            (SELECT @cfacADM = cfac, @adm = isadmin from rpdusers where cperson = @id)

            SELECT
            DISTINCT
            d.name as discpl
            , d.id as id_discpl
            , u.id as planlin
            , u.newdisid
            , p.abbrprofile as abbr
            , p.startyear as yr
            , p.cadmission as id_admission
            , u.cperson AS mira_id
            , p.ckaf as ckaf
            , u.planid
            , u.cperson AS razrab
            , ck.czav AS zavkaf
            , p.cperson AS rop
            , f.cdean AS fac
			, ck.zav AS zavkaf_name
			, f.dean AS fac_name
			, cp1.name AS razrab_name
			, cp2.name AS rop_name
            FROM uchplan_lines u
                LEFT JOIN uchplan_discpl d ON u.disid = d.id
                LEFT JOIN uchplan_plan p ON p.id = u.planid
                LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
                LEFT JOIN dbo.catkaf ck ON  ck.id = u.ckaf
                LEFT JOIN dbo.catfaculty f ON f.id = a.cfac
                LEFT JOIN dbo.catperson cp1 ON cp1.id = u.cperson
                LEFT JOIN dbo.catperson cp2 ON cp2.id = p.cperson
            WHERE 
                u.cperson IS NOT NULL 
                AND p.fordel = 'f' 
                AND u.fordel = 'f' 
                AND (
                    u.cperson = @id
                    OR ck.czav = @id
                    OR f.cdean = @id
                    OR p.cperson = @id
                    OR ((@cfacADM is not null and a.cfac = @cfacADM) OR @adm = 't')
                )
                AND p.startyear = @year
            """

        # r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
        #     "q": q
        # }, proxies={
        #     "http": "",
        #     "https": "",
        # })
        #
        # data = r.json()['RecordSet']

        data = Mira.fetch(q, [int(id), int(year)])

        return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_groups_by_person(id, year):
        q = f"""
                declare @id INT;
                declare @year INT;
                declare @cfacADM int;
                DECLARE @adm varchar;
                SET @id = %s;
                SET @year = %s;
                (SELECT @cfacADM = cfac, @adm = isadmin from rpdusers where cperson = @id)

                SELECT
                DISTINCT
                d.name as discpl
                , u.id as planlin
                , p.abbrprofile as abbr
                , p.startyear as yr
                , p.cadmission as id_admission
                , p.ckaf as ckaf
                , u.planid
                , u.cperson AS razrab
                , ck.czav AS zavkaf
                , p.cperson AS rop
                , f.cdean AS fac
                FROM uchplan_lines u
                    LEFT JOIN uchplan_discpl d ON u.disid = d.id
                    LEFT JOIN uchplan_plan p ON p.id = u.planid
                    LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
                    LEFT JOIN dbo.catkaf ck ON  ck.id = u.ckaf
                    LEFT JOIN dbo.catfaculty f ON f.id = a.cfac
                WHERE 
                    u.cperson IS NOT NULL 
                    AND p.fordel = 'f' 
                    AND u.fordel = 'f' 
                    AND (
                        u.cperson = @id
                        OR ck.czav = @id
                        OR f.cdean = @id
                        OR p.cperson = @id
                        OR ((@cfacADM is not null and a.cfac = @cfacADM) OR @adm = 't')
                    )
                    AND p.startyear = @year
                """

        data = Mira.fetch(q, [int(id), int(year)])

        return data

    @staticmethod
    # @cache_function(timeout=10 * 1)
    def get_programs_by_plan(plan_id):
        q = f"""
                declare @plan_id INT;
                SET @plan_id = %s;
                
                SELECT
                DISTINCT
                d.name as discpl
                , u.id as planlin
                , d.id as id_discpl
                , u.newdisid
                , ck.czav AS zavkaf
                , p.cperson AS rop
    			, ck.zav AS zavkaf_name
    			, f.dean AS fac_name
    			, cp1.name AS razrab_name
    			, cp2.name AS rop_name
                FROM uchplan_lines u
                    LEFT JOIN uchplan_discpl d ON u.disid = d.id
                    LEFT JOIN uchplan_plan p ON p.id = u.planid
                    LEFT JOIN dbo.catadmission a ON a.cuchplan = p.id
                    LEFT JOIN dbo.catkaf ck ON  ck.id = u.ckaf
                    LEFT JOIN dbo.catfaculty f ON f.id = a.cfac
                    LEFT JOIN dbo.catperson cp1 ON cp1.id = u.cperson
                    LEFT JOIN dbo.catperson cp2 ON cp2.id = p.cperson
                WHERE 
                    u.planid = @plan_id
                """
        data = Mira.fetch(q, [int(plan_id)])

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
            where l.id = %s /*and p2.fordel = 'f' and l2.fordel = 'f' */ and l2.id <> %s and d.name = d2.name
        """

        data = Mira.fetch(query, [id, id])

        return data
