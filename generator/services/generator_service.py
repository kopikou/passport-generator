from itertools import groupby

from constance import config
from django.conf import settings
from django.core.cache import cache

from app.utils import cache_function
from arim.models import CatPerson
from arim.services import AISServices
from auths.models import Permissions
from generator.models import PlanLinesLink, DefaultsResources, PlanLinesLinkComments, DisciplineThemes, \
    DisciplineWorkHours, AdditionalInfo, DisciplineIndicators, ScientificPlanData
from generator.serializer import PlanLinesLinkSerializer
from rpd.models import LinesData, LinesIndicators, SemesterData


class GeneratorService(object):

    @classmethod
    def reset_program_list_cache(cls, user_mira_id):
        key = f"rpd_get_program_list_{user_mira_id}"
        cache.delete(key)

    @classmethod
    def reset_practice_list_cache(cls, user_mira_id):
        key = f"rpd_get_practice_list_{user_mira_id}"
        cache.delete(key)

    @classmethod
    # @cache_function(timeout=60 * 1)
    def get_program_list(cls, user_mira_id, year=2025):
        cache_key = f"rpd_get_program_list_{user_mira_id}"
        if settings.ENABLE_CACHE_FUNCTION_DECORATOR:
            result = cache.get(cache_key)
            if result:
                return result

        data = AISServices.get_disciplines_by_person(user_mira_id, year)

        discpl_list = list(set(i['discpl'] for i in data))
        abbrprofile_list = list(set(i['abbr'] for i in data))
        startyear_list = list(set(i['yr'] for i in data))
        newdisid_list = list(set(i['newdisid'] for i in data))

        filtered_data = list(LinesData.objects.filter(dis__in=discpl_list, plan__abbrprofile__in=abbrprofile_list,
                                                 plan__startyear__in=startyear_list, newdisid__in=newdisid_list,
                                                 plan__file__status=4, synchronize=True).select_related("plan"))

        filtered_data_sorted = {f"{i.dis}_{i.plan.abbrprofile}_{i.newdisid}_{i.plan.startyear}": i for i in filtered_data}

        lineslink = PlanLinesLink.objects.filter(mira_id__in=[i['planlin'] for i in data]).select_related("planlines", "user_confirmed", "user_accepted")
        lineslink_sorted = sorted(lineslink, key=lambda x: x.mira_id)
        lineslink_by_id = {i.mira_id: i for i in lineslink_sorted}

        result = []
        for item in data:

            line = filtered_data_sorted.get(f"{item['discpl']}_{item['abbr']}_{item['newdisid']}_{item['yr']}")

            if line:

                res = lineslink_by_id.get(item['planlin'], [])

                if not res:
                    res, created = PlanLinesLink.objects.select_related("user_accepted__userprofile", "user_confirmed__userprofile").get_or_create(
                        cadmission=item['id_admission'],
                        mira_id=item['planlin'],
                        person=item['mira_id'],
                        defaults={
                            "cadmission": item['id_admission'],
                            "mira_id": item['planlin'],
                            "person": item['mira_id'],
                            "status": PlanLinesLink.StatusChoices.appointed,
                            "planlines_id": line.id,
                            "can_be_copied_by_anyone": False,
                        }
                    )

                if res.is_deleted:
                    continue

                result.append({
                    **item,
                    "id": res.id,
                    "plx_file": settings.SITE_URL + line.plan.file.file.url if line.plan.file else '',
                    "status": res.status,
                    "status_verbose": res.status_verbose,
                    "kafcode": res.planlines.caf,
                    "is_spo": item['ckaf'] in (1988516, 1988517),
                    "can_upload_file_directly": res.can_upload_file_directly,
                    "last_accepted_file_url": (settings.FORCE_SCRIPT_NAME or "") + res.last_accepted_file.url if res.last_accepted_file else None,
                    "user_confirmed": res.user_confirmed_id,
                    "can_be_copied_by_anyone": res.can_be_copied_by_anyone,
                    "user_confirmed_name": res.user_confirmed.username if res.user_confirmed else None,
                    "user_accepted": res.user_accepted_id,
                    "user_accepted_name": res.user_accepted.username if res.user_accepted else None,
                    "accept_date": res.accept_date,
                    "confirm_date": res.confirm_date,
                    "discode": res.planlines.newdisid,
                    "plan_id": line.plan_id,
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

        lst = config.RPD_DISCIPLINES_ONLY_ZAV_CONFIRM_REQUIRED.split("\n")
        for item in res:
            item['only_zav_required'] = item['discpl'] in lst \
                                        or item['kafcode'] in (208,) # кафедра физры
            if item['status'] == PlanLinesLink.StatusChoices.on_review:
                require_my_accept = 'zav' in item['type'] and not item['user_accepted']
                require_my_confirm = not item['only_zav_required'] \
                                     and 'rop' in item['type'] and not item['user_confirmed']
                if require_my_accept or require_my_confirm:
                    item['status_verbose'] = "Требует моего согласования/утверждения"

        cache.set(cache_key, res, 60)

        return res

    @classmethod
    @cache_function(timeout=60 * 1)
    def get_practice_list(cls, user_mira_id):
        cache_key = f"rpd_get_practice_list_{user_mira_id}"
        if settings.ENABLE_CACHE_FUNCTION_DECORATOR:
            result = cache.get(cache_key)
            if result:
                return result

        data = AISServices.get_practice_by_person(user_mira_id)

        discpl_list = [i['discpl'] for i in data]
        abbrprofile_list = [i['abbr'] for i in data]
        startyear_list = [i['yr'] for i in data]

        filtered_data = LinesData.objects.filter(dis__in=discpl_list, plan__abbrprofile__in=abbrprofile_list,
                                                 plan__startyear__in=startyear_list,
                                                 type=3,
                                                 plan__file__status=4, synchronize=True).select_related("plan")

        filtered_data_sorted = {f"{i.dis}_{i.plan.abbrprofile}_{i.plan.startyear}": i for i in filtered_data}

        lineslink = PlanLinesLink.objects.filter(mira_id__in=[i['planlin'] for i in data]).select_related("planlines")
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

        cache.set(cache_key, res, 60)

        return res

    @classmethod
    @cache_function(timeout=60 * 1)
    def get_asp_list(cls, year, user):
        data = AISServices.get_asp_napr(year, user.userprofile.mira_id)
        data = sorted(data, key=lambda x: x['species'])

        result = {"items": data}

        if Permissions.scientific_admin in user.userprofile.permissions:

            ais_plans = AISServices.get_all_asp(year)

            scientific_plan = ScientificPlanData.objects.filter(startyear=year).values_list('mira_id', flat=True)
            scientific_plan_ids = [i for i in scientific_plan]

            res = []
            for i in ais_plans:
                res.append({
                    **i,
                    "created": True if i['id'] in scientific_plan_ids else False
                })

            res = sorted(res, key=lambda x: x['species'])
            result.update({"admin_items": res})

        return result

    @classmethod
    def get_rpd_data(cls, plan_lines_link_id, user_mira_id=None):
        instance: PlanLinesLink = (PlanLinesLink.objects.filter(id=plan_lines_link_id)
                    .select_related("planlines", "planlines__plan", "user_accepted__userprofile", "user_confirmed__userprofile")
                    .prefetch_related("planlines__semesters", "planlines__indicators",
                                      "planlines__indicators__discipline_indicator", "discipline_themes",
                                      "discipline_work_hour").first())

        if instance.status == PlanLinesLink.StatusChoices.appointed:
            instance.status = PlanLinesLink.StatusChoices.is_filled
            instance.save()

        users = CatPerson.objects.in_bulk(
            [
                instance.person,
                instance.user_accepted.userprofile.mira_id if instance.user_accepted else None,
                instance.user_confirmed.userprofile.mira_id if instance.user_confirmed else None
            ]
        )

        serializer = PlanLinesLinkSerializer(instance)

        admission_info = AISServices.get_admissionn_info(serializer.data['cadmission'])

        other_discipline = list(LinesData.objects.filter(plan_id=serializer.data['planlines']['plan_id'],
                                                    synchronize=True).values("disid", "dis", "id"))


        # инфа по семестрам в которых идут дисциплины
        other_discipline_semesters = SemesterData.objects\
            .filter(planlineid__in=[i['id'] for i in other_discipline])\
            .values("planlineid_id", "num").order_by("planlineid_id", "num")
        other_discipline_semesters = {
            key: list([i['num'] for i in items])
            for key, items in groupby(other_discipline_semesters, key=lambda x: x['planlineid_id'])
        }

        resources = DefaultsResources.objects.all().values("id", "name", "type", "url")

        comment = PlanLinesLinkComments.objects.filter(planlineslink_id=instance.id).values(
            "id",
            "created_at",
            "comment",
            "user_id",
            "user__first_name",
            "user__last_name",
        ).last()

        old_rpd = AISServices.get_old_rpd_list(serializer.data['mira_id'])

        programs = []
        if user_mira_id:
            programs = cls.get_program_list(user_mira_id)

        common_links = PlanLinesLink\
            .objects\
            .filter(can_be_copied_by_anyone=True)\
            .select_related("planlines", "planlines__plan")

        result = {
            "admission": admission_info[0],
            "other_discipline": [
                {**i, "semesters": other_discipline_semesters.get(i['id'], [])} for i in other_discipline
            ],
            "resources": [i for i in resources],
            "comment": comment,
            "users": {
                "accepted": getattr(users.get(instance.user_accepted.userprofile.mira_id if instance.user_accepted else None), 'name', None),
                "developer": getattr(users.get(instance.person if instance.person else None), 'name', None),
                "confirmed": getattr(users.get(instance.user_confirmed.userprofile.mira_id if instance.user_confirmed else None), 'name', None),
            },
            "old": [i for i in old_rpd],
            "new": [{
                'abbrprofile': i['abbr'],
                'species': i['discpl'],
                'startyear': i['yr'],
                'id': i['id'],
            } for i in programs if 'person' in i['type']],
            "common": [{
                'abbrprofile': i.planlines.plan.abbrprofile,
                'species': i.planlines.dis,
                'startyear': i.planlines.plan.startyear,
                'id': i.id,
            } for i in common_links],
            "plx_file": settings.SITE_URL + instance.planlines.plan.file.file.url if instance.planlines.plan.file else '',
            **serializer.data,
        }
        return result

    @classmethod
    def copy_rpd_program(cls, from_planlineslink_id, to_planlineslink_id):
        themes_associations = {}

        DisciplineThemes.objects.filter(planlineslink_id=to_planlineslink_id).delete()
        from_themes = DisciplineThemes.objects.filter(planlineslink_id=from_planlineslink_id)

        from_line_link = PlanLinesLink.objects.filter(id=from_planlineslink_id).first()
        to_line_link = PlanLinesLink.objects.filter(id=to_planlineslink_id).first()

        from_indicators = {
            (i.indicator.indicator or "").replace(" ", "").replace(".",""): i
            for i in DisciplineIndicators.objects.filter(planlineid=from_line_link.planlines_id).select_related("indicator")
        }

        DisciplineIndicators.objects.filter(planlineid=to_line_link.planlines_id).delete()
        indicators = LinesIndicators.objects.filter(planlineid=to_line_link.planlines_id)

        for ind in indicators:
            indicator: DisciplineIndicators = from_indicators.get((ind.indicator or "").replace(" ", "").replace(".",""))
            if indicator:
                indicator.id = None
                indicator.planlineid_id = to_line_link.planlines_id
                indicator.indicator_id = ind.id
                indicator.save()

        for theme in from_themes:
            from_theme_id = theme.pk
            theme.pk = None
            theme.planlineslink_id = to_planlineslink_id
            theme.save()
            themes_associations[from_theme_id] = theme.pk

        DisciplineWorkHours.objects.filter(planlineslink_id=to_planlineslink_id).delete()
        from_work_hours = DisciplineWorkHours.objects.filter(planlineslink_id=from_planlineslink_id)
        for wh in from_work_hours:
            wh.planlineslink_id = to_planlineslink_id
            wh.id = None
            wh.theme_id = themes_associations[wh.theme_id]
            wh.save()

        AdditionalInfo.objects.filter(planlineslink_id=to_planlineslink_id).delete()
        from_additional_info = AdditionalInfo.objects.filter(planlineslink_id=from_planlineslink_id)
        for ai in from_additional_info:
            ai.planlineslink_id = to_planlineslink_id
            ai.id = None
            ai.save()

