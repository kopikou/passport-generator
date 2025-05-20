from itertools import groupby

from constance import config
from django.conf import settings
from django.core.cache import cache

from app.utils import cache_function
from arim.services import AISServices
from generator.models import PlanLinesLink, DefaultsResources, PlanLinesLinkComments, DisciplineThemes, \
    DisciplineWorkHours, AdditionalInfo, DisciplineIndicators
from generator.serializer import PlanLinesLinkSerializer
from rpd.models import LinesData, LinesIndicators


class GeneratorService(object):

    @classmethod
    def reset_program_list_cache(cls, user_mira_id):
        key = f"rpd_get_program_list_{user_mira_id}"
        cache.delete(key)

    @classmethod
    # @cache_function(timeout=60 * 1)
    def get_program_list(cls, user_mira_id):
        cache_key = f"rpd_get_program_list_{user_mira_id}"
        if settings.ENABLE_CACHE_FUNCTION_DECORATOR:
            result = cache.get(cache_key)
            if result:
                return result

        data = AISServices.get_disciplines_by_person(user_mira_id)

        discpl_list = list(set(i['discpl'] for i in data))
        abbrprofile_list = list(set(i['abbr'] for i in data))
        startyear_list = list(set(i['yr'] for i in data))

        filtered_data = list(LinesData.objects.filter(dis__in=discpl_list, plan__abbrprofile__in=abbrprofile_list,
                                                 plan__startyear__in=startyear_list,
                                                 plan__file__status=4, synchronize=True).select_related("plan"))

        filtered_data_sorted = {f"{i.dis}_{i.plan.abbrprofile}_{i.plan.startyear}": i for i in filtered_data}

        lineslink = PlanLinesLink.objects.filter(mira_id__in=[i['planlin'] for i in data])
        lineslink_sorted = sorted(lineslink, key=lambda x: x.mira_id)
        lineslink_by_id = {i.mira_id: i for i in lineslink_sorted}

        result = []
        for item in data:

            line = filtered_data_sorted.get(f"{item['discpl']}_{item['abbr']}_{item['yr']}")

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
                        }
                    )

                result.append({
                    **item,
                    "id": res.id,
                    "status": res.status,
                    "status_verbose": res.status_verbose,
                    "kafcode": res.planlines.caf,
                    "user_confirmed": res.user_confirmed_id,
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
            item['only_zav_required'] = item['discpl'] in lst
            if item['status'] == PlanLinesLink.StatusChoices.on_review:
                require_my_accept = 'zav' in item['type'] and not item['user_accepted']
                require_my_confirm = not item['only_zav_required'] \
                                     and 'rop' in item['type'] and not item['user_confirmed']
                if require_my_accept or require_my_confirm:
                    item['status_verbose'] = "Требует моего согласования/утверждения"
                # item['require_my_accept'] = require_my_accept
                # item['require_my_confirm'] = require_my_confirm
            # elif require_my_accept:
            #     item['status_verbose'] = "Требует согласования"
            # elif require_my_confirm:
            #     item['status_verbose'] = "Требует утверждения"

        cache.set(cache_key, res, 60)

        return res

    @classmethod
    def get_rpd_data(cls, plan_lines_link_id, user_mira_id=None):
        instance = (PlanLinesLink.objects.filter(id=plan_lines_link_id)
                    .select_related("planlines", "planlines__plan")
                    .prefetch_related("planlines__semesters", "planlines__indicators",
                                      "planlines__indicators__discipline_indicator", "discipline_themes",
                                      "discipline_work_hour").first())

        if instance.status == PlanLinesLink.StatusChoices.appointed:
            instance.status = PlanLinesLink.StatusChoices.is_filled
            instance.save()

        serializer = PlanLinesLinkSerializer(instance)

        admission_info = AISServices.get_admissionn_info(serializer.data['cadmission'])

        other_discipline = LinesData.objects.filter(plan_id=serializer.data['planlines']['plan_id'],
                                                    synchronize=True).values("disid", "dis")

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

        result = {
            "admission": admission_info[0],
            "other_discipline": [i for i in other_discipline],
            "resources": [i for i in resources],
            "comment": comment,
            "old": [i for i in old_rpd],
            "new": [{
                'abbrprofile': i['abbr'],
                'species': i['discpl'],
                'startyear': i['yr'],
                'id': i['id'],
            } for i in programs if 'person' in i['type']],
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
            (i.indicator.indicator or "").replace(" ", ""): i
            for i in DisciplineIndicators.objects.filter(planlineid=from_line_link.planlines_id).select_related("indicator")
        }

        DisciplineIndicators.objects.filter(planlineid=to_line_link.planlines_id).delete()
        indicators = LinesIndicators.objects.filter(planlineid=to_line_link.planlines_id)

        for ind in indicators:
            indicator: DisciplineIndicators = from_indicators.get((ind.indicator or "").replace(" ", ""))
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

