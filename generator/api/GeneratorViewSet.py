import os
from itertools import groupby

import pendulum
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission, RPGEN
from arim.services import AISServices
from arim_library.services import LibraryServices
from auths.models import Permissions
from generator.models import PlanLinesLink, FormControl, IndependentTypes, DisciplineThemes, DisciplineWorkHours, \
    DefaultsResources, PlanLinesLinkComments, ScientificPlanData, ScientificWorkType, ScientificData, \
    ScientificDataDefault
from generator.serializer import PlanLinesLinkSerializer, \
    DisciplineIndicatorsAddSerializer, DisciplineThemeSerializer, \
    DisciplineWorkHoursSerializer, AdditionalInfoSerializer, ScientificPlanSerializer, ScientificDataSerializer
from generator.services import ReportService
from rpd.models import LinesData, PlanData
from rpd.services import RPDGenSerivce


class GeneratorViewSet(
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = PlanLinesLink.objects.all()
    serializer_class = PlanLinesLinkSerializer
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator)]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        instance = (PlanLinesLink.objects.filter(id=pk)
                    .select_related("planlines", "planlines__plan")
                    .prefetch_related("planlines__semesters", "planlines__indicators",
                                      "planlines__indicators__discipline_indicator", "discipline_themes",
                                      "discipline_work_hour").first())

        if instance.status == PlanLinesLink.StatusChoices.appointed:
            instance.status = PlanLinesLink.StatusChoices.is_filled
            instance.save()

        serializer = self.get_serializer(instance)

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

        result = {
            "admission": admission_info[0],
            "other_discipline": [i for i in other_discipline],
            "resources": [i for i in resources],
            "comment": comment,
            "old": [i for i in old_rpd],
            **serializer.data,
        }

        return Response(result)

    @action(methods=['POST'], url_path='save-asp-program-data', detail=True)
    def save_asp_program_data(self, request, *args, **kwargs):

        data = self.request.data
        pk = self.kwargs['pk']

        instance = ScientificPlanData.objects.get(id=pk)

        serializer = ScientificPlanSerializer(instance, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(methods=['GET'], url_path='copy-asp-program-data', detail=True)
    def copy_asp_program_data(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        old_pk = self.request.query_params['old_pk']

        instance = ScientificPlanData.objects.get(mira_id=pk)

        old_data = RPDGenSerivce.get_asp_plan(old_pk)

        old_data_by_key = {i['id']: i for i in old_data if i['type_id'] == 15}

        for key, i in enumerate(old_data):
            if not i['sort']:
                old_data[key] = {
                    **i,
                    'sort': 0,
                }

        grouped_old_data = {key: list(i) for key, i in groupby(old_data, key=lambda x: x['type_id'])}

        data = []
        for key, items in grouped_old_data.items():
            if key == 16:
                for index, item in enumerate(sorted(items, key=lambda x: x['sort']), start=1):

                    semester = old_data_by_key.get(item['linked_id'], {}).get('value', None)

                    data.append({
                        "plan_id": instance.id,
                        "text": item['value'],
                        "parameters": {"order": index, "part": 0, "semester": semester},
                    })
            elif key == 17:
                for index, item in enumerate(sorted(items, key=lambda x: x['sort']), start=1):
                    data.append({
                        "plan_id": instance.id,
                        "text": item['value'],
                        "parameters": {"order": index, "part": 1},
                    })
            elif key == 18:
                for index, item in enumerate(sorted(items, key=lambda x: x['sort']), start=1):
                    data.append({
                        "plan_id": instance.id,
                        "text": item['value'],
                        "parameters": {"order": index, "part": 2},
                    })


        ScientificData.objects.filter(plan_id=instance.id).delete()

        serializer = ScientificDataSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    @action(methods=['get'], url_path="get-asp-program-list", detail=False)
    def get_aps_program_list(self, request, *args, **kwargs):
        user = self.request.user.userprofile.mira_id

        year = self.request.query_params.get('year', pendulum.now().year)

        data = AISServices.get_asp_napr(year, user)
        data = sorted(data, key=lambda x: x['species'])

        result = {"items": data}

        if Permissions.scientific_admin in request.user.userprofile.permissions:

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


        return Response(data=result)

    @action(methods=['GET'], url_path="get-asp-program-detail", detail=True)
    def get_asp_program_detail(self, request, *args, **kwargs):

        pk = int(self.kwargs['pk'])

        mira_data = AISServices.get_asp_napr_detail(pk)
        plan_data = PlanData.objects.filter(mira_id=pk).values()

        if not mira_data or not plan_data:
            return Response(data={"status": 'no data'})

        try:
            instance = ScientificPlanData.objects.get(mira_id=pk)

        except ObjectDoesNotExist:
            fgt = ''
            if plan_data[0]['gosdocument']:
                fgt += f"№ {plan_data[0]['gosdocument']}"

            if plan_data[0]['gosdate']:
                fgt += f" от {plan_data[0]['gosdate']}"

            result = {
                "ckaf": mira_data[0]['ckaf'],
                "name": mira_data[0]['species'],
                "cfac": mira_data[0]['cfac'],
                "rng": mira_data[0]['range'],
                "cfob": mira_data[0]['cfob'],
                "startyear": mira_data[0]['startyear'],
                "fgt": fgt,
                "viceRector": 'Смирнов Владимир Владимирович',
                "director": mira_data[0]['dean'],
                "zavkaf": mira_data[0]['zav'],
                "rop": mira_data[0]['rop'],
                "year": mira_data[0]['yr'],
                "mira_id": pk,
            }

            instance, created = ScientificPlanData.objects.get_or_create(
                mira_id=pk,
                defaults={
                    **result,
                }
            )

        serializer = ScientificPlanSerializer(instance)
        result = serializer.data

        scientific_data = ScientificData.objects.filter(plan_id=result['id']).values('id', 'text', 'parameters')

        if not scientific_data:
            query = Q(kurs=result['rng'])
            query |= Q(kurs=0)

            default_data = ScientificDataDefault.objects.filter(query)

            for item in default_data:
                ScientificData.objects.create(
                    plan_id=result['id'],
                    text=item.text,
                    parameters={'semester': item.semester, 'order': item.order, 'part': item.part},
                )

            scientific_data = ScientificData.objects.filter(plan_id=result['id']).values('id', 'text', 'parameters')

        old_plans = AISServices.get_asp_old_plans(pk)


        return Response(data={
            "plan": result,
            "data": scientific_data,
            "old": old_plans,
        })

    @action(methods=['GET'], url_path="get-program-list", detail=False)
    def get_program_list(self, request, *args, **kwargs):

        user = self.request.user.userprofile.mira_id

        data = AISServices.get_disciplines_by_person(user)

        discpl_list = [i['discpl'] for i in data]
        abbrprofile_list = [i['abbr'] for i in data]
        startyear_list = [i['yr'] for i in data]

        filtered_data = LinesData.objects.filter(dis__in=discpl_list, plan__abbrprofile__in=abbrprofile_list,
                                                 plan__startyear__in=startyear_list,
                                                 plan__file__status=4, synchronize=True).select_related("plan")

        filtered_data_sorted = {f"{i.dis}_{i.plan.abbrprofile}_{i.plan.startyear}": i for i in filtered_data}

        result = []
        for item in data:

            line = filtered_data_sorted.get(f"{item['discpl']}_{item['abbr']}_{item['yr']}")

            if line:
                lines, created = PlanLinesLink.objects.get_or_create(
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
                    "id": lines.id,
                    "status": lines.status,
                    "status_verbose": lines.status_verbose,
                    "kafcode": lines.planlines.caf,
                    "discode": lines.planlines.newdisid,
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

        return Response(
            data=res,
        )

    @action(methods=['POST'], url_path="save-scientific-data", detail=True)
    def save_scientific_data(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        serializer = ScientificDataSerializer(data={**request.data, "plan_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(methods=['GET'], url_path="get-scientific-work", detail=False)
    def get_scientific_work(self, request, *args, **kwargs):

        data = ScientificWorkType.objects.all().values('id', 'name')

        return Response(data=data)

    @action(methods=['POST'], url_path="save-scientific-data", detail=True)
    def save_scientific_data(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        res = []

        for i in self.request.data:
            res.append({
                'id': i.get('id', None),
                'plan_id': i.get('plan_id', None),
                'text': i.get('text', None),
                'parameters': i.get('parameters', None),
            })

        serializer = ScientificDataSerializer(data=res, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    @action(methods=['DELETE'], url_path="del-scientific-work", detail=True)
    def del_scientific_work(self, request, *args, **kwargs):

        ScientificData.objects.get(id=self.kwargs['pk']).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], url_path="get-scientific-report", detail=True)
    def get_scientific_report(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        result = ScientificPlanData.objects.get(mira_id=pk)

        rpd_data = PlanData.objects.get(mira_id=result.mira_id)
        filename = f"План_НИД_{str(rpd_data.startyear)[:2]}_{result.name}_{rpd_data.abbrprofile}.docx".replace(',', ' ')
        # filename = f"План_НИД_{str(rpd_data.startyear)[:2]}_{result.name}_{rpd_data.abbrprofile}.pdf"
        path = f'templates/outputs/'

        # response = HttpResponse(content_type='application/pdf')
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path(filename)}"

        if not os.path.exists(path):
            os.makedirs(path)

        path_doc_file = f"{os.path.abspath(path)}/{pk}.docx"
        path_pdf_file = f"{os.path.abspath(path)}/{pk}.pdf"

        tpl = ReportService.get_scientific_report(result)
        tpl.save(response)
        # tpl.save(path_doc_file)

        # if platform.system() == 'Linux':
        #     run([
        #         'libreoffice', '--headless', '--invisible', '--convert-to',
        #         'pdf', path_doc_file, '--outdir', os.path.dirname(path_pdf_file),
        #     ])
        #
        # elif platform.system() == 'Windows':
        #     from win32com.client import Dispatch
        #
        #     word = Dispatch('Word.Application')
        #     doc = word.Documents.Open(path_doc_file)
        #     doc.SaveAs(path_pdf_file, FileFormat=17)
        #     word.Quit()
        # else:
        #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        # with open(path_pdf_file, 'rb') as file:
        #     response.write(file.read())
        #
        # if os.path.exists(path_doc_file):
        #     os.remove(path_doc_file)
        #
        # if os.path.exists(path_pdf_file):
        #     os.remove(path_pdf_file)

        # return Response(result)
        return response

    @action(methods=['GET'], url_path="search-book", detail=False)
    def search_book(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = LibraryServices.search_book(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-software", detail=False)
    def search_soft(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = AISServices.search_software(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-oborud", detail=False)
    def search_oborud(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')
        type = int(self.request.query_params.get('type'))
        caf = int(self.request.query_params.get('caf'))

        data = AISServices.search_oborud(val, type, caf)

        return Response(data)

    @action(methods=['GET'], url_path="get-form-control-data", detail=False)
    def get_form_control_data(self, request, *args, **kwargs):
        data = FormControl.objects.all().values("id", "name", "type")

        return Response(data)

    @action(methods=['GET'], url_path="get-independent-types-data", detail=False)
    def get_independent_types_data(self, request, *args, **kwargs):
        data = IndependentTypes.objects.all().values("id", "name", "type")

        return Response(data)

    @action(methods=['POST'], url_path="save-discipline-indicator", detail=False)
    def save_discipline_indicator(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineIndicatorsAddSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['POST'], url_path="save-discipline-themes", detail=False)
    def save_discipline_themes(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineThemeSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="delete-discipline-themes", detail=False)
    def delete_discipline_themes(self, request, *args, **kwargs):
        pk = self.request.query_params['id']

        DisciplineThemes.objects.filter(id=pk).delete()

        return Response({"success": True})

    @action(methods=['POST'], url_path="save-discipline-work-hour", detail=False)
    def save_discipline_work(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineWorkHoursSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="delete-discipline-work-hour", detail=False)
    def delete_discipline_work_hour(self, request, *args, **kwargs):
        pk = self.request.query_params.get('id')

        DisciplineWorkHours.objects.filter(id=pk).delete()

        return Response({"success": True})

    @action(methods=['POST'], url_path="save-additional-info", detail=True)
    def save_additional_info(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = AdditionalInfoSerializer(
            data={"planlineslink_id": self.kwargs['pk'], "type": data['type'], "value": data['value']})
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="get-rpd-report", detail=True)
    def get_rpd_report(self, request, *args, **kwargs):
        instance = self.get_object()
        result = self.retrieve(request, *args, **kwargs).data

        filename = f"РПД_{instance.planlines.dis}_{result['admission']['abbr']}-{result['admission']['yr']}.docx".replace(',', ' ')

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path(filename)}"

        doc = ReportService.get_rpd_report(result)
        doc.save(response)

        # return Response(result)
        return response

    @action(methods=['GET'], url_path="get-rpd-annotation", detail=True)
    def get_rpd_annotation(self, request, *args, **kwargs):
        instance = self.get_object()
        result = self.retrieve(request, *args, **kwargs).data

        filename = f"Аннотация_{instance.planlines.dis}_{result['admission']['abbr']}-{result['admission']['yr']}.docx".replace(',', ' ')

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path(filename)}"

        doc = ReportService.get_rpd_annotation(result)
        doc.save(response)

        # return Response(result)
        return response

    @action(methods=['GET'], url_path="send-rpd-on-review", detail=True)
    def send_rpd_on_review(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.on_review
        instance.review_date = pendulum.now()
        instance.save()

        return Response(data={'status_verbose': PlanLinesLink.StatusChoices.on_review.label,
                              'status': PlanLinesLink.StatusChoices.on_review})

    @action(methods=['POST'], url_path="accept-rpd", detail=True)
    def accept_rpd(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.accepted
        instance.protocol_number = self.request.data['number']
        instance.protocol_date = self.request.data['date']
        instance.user_type = self.request.data['userType']
        instance.meeting = self.request.data['meeting']
        instance.user_accepted = self.request.user
        instance.accept_date = pendulum.now()
        instance.save()

        return Response({"success": True})

    @action(methods=['POST'], url_path="send-rpd-on-refile", detail=True)
    def send_rpd_on_refile(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.on_refile
        instance.save()

        PlanLinesLinkComments.objects.create(comment=self.request.data['comment'], user_id=self.request.user.id,
                                             planlineslink_id=instance.id)

        return Response({"success": True})

    @action(methods=['GET'], url_path="get-old-comments", detail=True)
    def get_old_comments(self, request, *args, **kwargs):
        instance = self.get_object()

        data = PlanLinesLinkComments.objects.filter(planlineslink_id=instance.id).order_by('-created_at').values()

        return Response([i for i in data])

    @action(methods=['GET'], url_path="copy-old-rpd-program", detail=True)
    def get_old_rpd(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        old_pk = int(self.request.query_params['old_pk'])

        instance = self.retrieve(request, *args, **kwargs).data

        current_control = RPDGenSerivce.get_current_control()
        current_control_by_id = {i['id']: i['name'] for i in current_control}

        kind_srs = RPDGenSerivce.get_kind_srs()
        kind_srs_by_id = {i['id']: i['name'] for i in kind_srs}

        cattitle = RPDGenSerivce.get_rpd_line(old_pk)
        cattitle_id = cattitle[0]['id']

        d2s = RPDGenSerivce.get_displ2semestr(cattitle_id)

        for item in d2s:

            d2lek = RPDGenSerivce.get_displ2lek(item['id'])

            for i in d2lek:
                d2sam = RPDGenSerivce.get_displ2sam(i['id'])
                d2pract = RPDGenSerivce.get_displ2pract(i['id'])
                d2lab = RPDGenSerivce.get_displ2lab(i['id'])

        return Response()
