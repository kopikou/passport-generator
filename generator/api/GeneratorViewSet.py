import datetime
import os
import platform
from itertools import groupby
from subprocess import run
from time import sleep

import pendulum
from constance import config
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile, UploadedFile
from django.db.models import Q, Max, F
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from arim_library.services import LibraryServices
from auths.models import Permissions
from generator.models import PlanLinesLink, FormControl, IndependentTypes, DisciplineThemes, DisciplineWorkHours, \
    PlanLinesLinkComments, ScientificPlanData, ScientificWorkType, ScientificData, \
    ScientificDataDefault, DisciplineIndicators, DefaultsResources, AdditionalInfo
from generator.permissions import CanEditRPDProgram, CanViewRPDProgram, CanConfirmRPDProgram, CanAcceptRPDProgram, CanEditScientificProgram
from generator.serializer import PlanLinesLinkSerializer, \
    DisciplineIndicatorsAddSerializer, DisciplineThemeSerializer, \
    DisciplineWorkHoursSerializer, AdditionalInfoSerializer, ScientificPlanSerializer, ScientificDataSerializer
from generator.services import ReportService
from generator.services.generator_service import GeneratorService
from rpd.models import PlanData, LinesIndicators
from rpd.services import RPDGenSerivce


class GeneratorViewSet(
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = PlanLinesLink.objects.all()
    serializer_class = PlanLinesLinkSerializer
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        result = GeneratorService.get_rpd_data(pk, self.request.user.userprofile.mira_id)
        return Response(result)


    @action(methods=['POST'], url_path='save-asp-program-data', detail=True, permission_classes=[CanEditScientificProgram])
    def save_asp_program_data(self, request, *args, **kwargs):

        data = self.request.data
        pk = self.kwargs['pk']

        instance = ScientificPlanData.objects.get(id=pk)

        serializer = ScientificPlanSerializer(instance, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(methods=['GET'], url_path='copy-asp-program-data', detail=True, permission_classes=[CanEditScientificProgram])
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

    @action(methods=['get'], url_path="get-asp-program-list", detail=False, permission_classes=[IsAuthenticated])
    def get_aps_program_list(self, request, *args, **kwargs):
        year = self.request.query_params.get('year', pendulum.now().year)

        res = GeneratorService.get_asp_list(year, self.request.user)

        return Response(data=res)

    @action(methods=['GET'], url_path="get-asp-program-detail", detail=True, permission_classes=[CanEditScientificProgram])
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

    @action(methods=['GET'], url_path="get-program-list", detail=False, permission_classes=[IsAuthenticated])
    def get_program_list(self, request, *args, **kwargs):

        res = GeneratorService.get_program_list(self.request.user.userprofile.mira_id)

        return Response(
            data=res,
        )

    @action(methods=['GET'], url_path="get-practice-list", detail=False, permission_classes=[IsAuthenticated])
    def get_practice_list(self, request, *args, **kwargs):
        user = self.request.user.userprofile.mira_id

        res = GeneratorService.get_practice_list(user)

        return Response(
            data=res,
        )

    @action(methods=['GET'], url_path="get-scientific-work", detail=False, permission_classes=[IsAuthenticated])
    def get_scientific_work(self, request, *args, **kwargs):

        data = ScientificWorkType.objects.all().values('id', 'name')

        return Response(data=data)

    @action(methods=['POST'], url_path="save-scientific-data", detail=True, permission_classes=[CanEditScientificProgram])
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

    @action(methods=['DELETE'], url_path="del-scientific-work", detail=True, permission_classes=[CanEditScientificProgram])
    def del_scientific_work(self, request, *args, **kwargs):

        ScientificData.objects.get(id=self.kwargs['pk']).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], url_path="get-scientific-report", detail=True, permission_classes=[IsAuthenticated])
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

    @action(methods=['GET'], url_path="search-book", detail=False, permission_classes=[IsAuthenticated])
    def search_book(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = LibraryServices.search_book(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-software", detail=False, permission_classes=[IsAuthenticated])
    def search_soft(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = AISServices.search_software(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-oborud", detail=False, permission_classes=[IsAuthenticated])
    def search_oborud(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')
        type = int(self.request.query_params.get('type'))
        caf = int(self.request.query_params.get('caf'))

        data = AISServices.search_oborud(val, type, caf)

        return Response(data)

    @action(methods=['GET'], url_path="get-form-control-data", detail=False, permission_classes=[IsAuthenticated])
    def get_form_control_data(self, request, *args, **kwargs):
        data = FormControl.objects.all().values("id", "name", "type")

        return Response(data)

    @action(methods=['GET'], url_path="get-independent-types-data", detail=False, permission_classes=[IsAuthenticated])
    def get_independent_types_data(self, request, *args, **kwargs):
        data = IndependentTypes.objects.all().values("id", "name", "type")

        return Response(data)

    @action(methods=['POST'], url_path="save-discipline-indicator", detail=True, permission_classes=[CanEditRPDProgram])
    def save_discipline_indicator(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineIndicatorsAddSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['POST'], url_path="save-discipline-themes", detail=True, permission_classes=[CanEditRPDProgram])
    def save_discipline_themes(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineThemeSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="delete-discipline-themes", detail=True, permission_classes=[CanEditRPDProgram])
    def delete_discipline_themes(self, request, *args, **kwargs):
        pk = self.request.query_params['id']

        DisciplineThemes.objects.filter(id=pk).delete()

        return Response({"success": True})

    @action(methods=['POST'], url_path="save-discipline-work-hour", detail=True, permission_classes=[CanEditRPDProgram])
    def save_discipline_work(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = DisciplineWorkHoursSerializer(data=data)
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="delete-discipline-work-hour", detail=True, permission_classes=[CanEditRPDProgram])
    def delete_discipline_work_hour(self, request, *args, **kwargs):
        pk = self.request.query_params.get('id')

        DisciplineWorkHours.objects.filter(id=pk).delete()

        return Response({"success": True})

    @action(methods=['POST'], url_path="save-additional-info", detail=True, permission_classes=[CanEditRPDProgram])
    def save_additional_info(self, request, *args, **kwargs):
        data = self.request.data

        serializer_data = AdditionalInfoSerializer(
            data={"planlineslink_id": self.kwargs['pk'], "type": data['type'], "value": data['value']})
        serializer_data.is_valid(raise_exception=True)
        serializer_data.save()

        return Response(serializer_data.data)

    @action(methods=['GET'], url_path="get-rpd-report", detail=True)
    def get_rpd_report(self, request, *args, **kwargs):
        instance: PlanLinesLink = self.get_object()

        updated_at_max = PlanLinesLink.objects.annotate(t_updated_at=F('updated_at')).values("t_updated_at").union(
            DisciplineIndicators.objects.values("updated_at"),
            DisciplineThemes.objects.values("updated_at"),
            DisciplineWorkHours.objects.values("updated_at"),
            DefaultsResources.objects.values("updated_at"),
            AdditionalInfo.objects.values("updated_at"),
        ).aggregate(updated_at=Max(F("t_updated_at")))

        if not instance.file or instance.file_updated_at  or instance.file_updated_at < updated_at_max['updated_at']:
            instance = ReportService.generate_rpd_report(instance)

        return redirect(instance.file.url)

    @action(methods=['GET'], url_path="get-rpd-annotation", detail=True)
    def get_rpd_annotation(self, request, *args, **kwargs):
        instance = self.get_object()
        result = self.retrieve(request, *args, **kwargs).data

        filename = f"Аннотация_{instance.planlines.dis}_{result['admission']['abbr']}-{result['admission']['yr']}.docx".replace(
            ',', ' ')

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f"attachment; filename={escape_uri_path(filename)}"

        doc = ReportService.get_rpd_annotation(result)
        doc.save(response)

        # return Response(result)
        return response

    @action(methods=['GET'], url_path="send-rpd-on-edit", detail=True, permission_classes=[CanEditRPDProgram])
    def send_rpd_on_edit(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.is_filled
        instance.user_confirmed = None
        instance.user_accepted = None
        instance.review_date = None
        instance.accept_date = None
        instance.confirm_date = None
        instance.save()
        GeneratorService.reset_program_list_cache(self.request.user.userprofile.mira_id)
        GeneratorService.reset_practice_list_cache(self.request.user.userprofile.mira_id)

        return Response(data={'status_verbose': PlanLinesLink.StatusChoices.is_filled.label,
                              'status': PlanLinesLink.StatusChoices.is_filled})


    @action(methods=['GET'], url_path="send-rpd-on-review", detail=True, permission_classes=[CanEditRPDProgram])
    def send_rpd_on_review(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.on_review
        instance.review_date = pendulum.now()
        instance.save()
        GeneratorService.reset_program_list_cache(self.request.user.userprofile.mira_id)
        GeneratorService.reset_practice_list_cache(self.request.user.userprofile.mira_id)

        return Response(data={'status_verbose': PlanLinesLink.StatusChoices.on_review.label,
                              'status': PlanLinesLink.StatusChoices.on_review})

    @action(methods=['POST'], url_path="accept-rpd", detail=True, permission_classes=[CanAcceptRPDProgram])
    def accept_rpd(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.status = PlanLinesLink.StatusChoices.accepted
        instance.protocol_number = self.request.data.get('number')
        instance.protocol_date = self.request.data.get('date')
        instance.meeting = self.request.data.get('meeting')
        # instance.user_type = self.request.data['userType']

        instance.user_accepted = self.request.user
        instance.accept_date = pendulum.now()

        if instance.planlines.dis in config.RPD_DISCIPLINES_ONLY_ZAV_CONFIRM_REQUIRED.split("\n"):
            instance.status = PlanLinesLink.StatusChoices.accepted
        elif instance.user_confirmed and instance.user_accepted:
            instance.status = PlanLinesLink.StatusChoices.accepted
        instance.save()

        GeneratorService.reset_program_list_cache(self.request.user.userprofile.mira_id)
        GeneratorService.reset_practice_list_cache(self.request.user.userprofile.mira_id)

        return Response({"success": True})

    @action(methods=['POST'], url_path="confirm-rpd", detail=True, permission_classes=[CanConfirmRPDProgram])
    def confirm_rpd(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user_confirmed = self.request.user
        instance.confirm_date = pendulum.now()

        if instance.user_confirmed and instance.user_accepted:
            instance.status = PlanLinesLink.StatusChoices.accepted
        instance.save()

        GeneratorService.reset_program_list_cache(self.request.user.userprofile.mira_id)
        GeneratorService.reset_practice_list_cache(self.request.user.userprofile.mira_id)

        return Response({"success": True})



    @action(methods=['POST'], url_path="toggle-can-be-copied-by-anyone", detail=True, permission_classes=[CanEditRPDProgram])
    def toggle_can_be_copied_by_anyone(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.can_be_copied_by_anyone = not instance.can_be_copied_by_anyone

        instance.save()

        return Response({"success": True})

    @action(methods=['POST'], url_path="send-rpd-on-refile", detail=True, permission_classes=[CanAcceptRPDProgram | CanConfirmRPDProgram])
    def send_rpd_on_refile(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = PlanLinesLink.StatusChoices.on_refile
        instance.save()

        GeneratorService.reset_program_list_cache(self.request.user.userprofile.mira_id)
        GeneratorService.reset_practice_list_cache(self.request.user.userprofile.mira_id)

        PlanLinesLinkComments.objects.create(comment=self.request.data['comment'], user_id=self.request.user.id,
                                             planlineslink_id=instance.id)

        return Response({"success": True})

    @action(methods=['GET'], url_path="get-old-comments", detail=True)
    def get_old_comments(self, request, *args, **kwargs):
        instance = self.get_object()

        data = PlanLinesLinkComments.objects.filter(planlineslink_id=instance.id).order_by('-created_at').values()

        return Response([i for i in data])

    @action(methods=['GET'], url_path="copy-old-rpd-program", detail=True, permission_classes=[CanEditRPDProgram])
    def get_old_rpd(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        old_pk = int(self.request.query_params['old_pk'])

        instance = self.retrieve(request, *args, **kwargs).data

        form_control = FormControl.objects.all()
        independent_types = IndependentTypes.objects.all()

        form_control_by_name = {i.name: i.id for i in form_control}
        independent_types_by_name = {i.name: i.id for i in independent_types}

        current_control = RPDGenSerivce.get_current_control()
        current_control_by_id = {i['id']: i['name'] for i in current_control}

        kind_srs = RPDGenSerivce.get_kind_srs()
        kind_srs_by_id = {i['id']: i['name'] for i in kind_srs}

        cattitle = RPDGenSerivce.get_rpd_line(old_pk)
        cattitle_id = cattitle[0]['id']

        DisciplineThemes.objects.filter(planlineslink_id=pk).delete()
        DisciplineWorkHours.objects.filter(planlineslink_id=pk).delete()
        DisciplineIndicators.objects.filter(planlineid_id=instance['planlines']['id']).delete()

        instance_indicators_by_index = {i['indicator_index']: i['id'] for i in instance['planlines']['indicators']}
        plan_indikators = RPDGenSerivce.get_mleha_planindikator(cattitle[0]['cplanlines'])

        for item in plan_indikators:
            indicator = RPDGenSerivce.get_mleha_indikator(item['indikid'])

            indicator_id = instance_indicators_by_index.get(indicator[0]['index'])

            if indicator_id:

                dis_indicator_serializer = DisciplineIndicatorsAddSerializer(data={
                    "indicator_id": indicator_id,
                    "planlineid_id": instance['planlines']['id'],
                    "know": item['znat'],
                    "able": item['umet'],
                    "own": item['vladet'],
                    "criteria": item['kriteriy_oceniv'],
                    "methods": item['metod_oceniv'],
                })
                dis_indicator_serializer.is_valid(raise_exception=True)
                dis_indicator_serializer.save()


        d2s = RPDGenSerivce.get_displ2semestr(cattitle_id)

        for item in d2s:

            d2lek = RPDGenSerivce.get_displ2lek(item['id'])

            for i in d2lek:

                control = current_control_by_id.get(i['ccurrent_control'], 'Отчет')
                form_control_id = form_control_by_name.get(control, None)

                theme_serializer = DisciplineThemeSerializer(data={
                    "planlineslink_id": pk,
                    "name": i['tema'] or '-',
                    "semester": item['semestr'],
                    "formcontrol_list": [form_control_id],
                    "comment": i['note'],
                    "num": i['num'] or 1,
                })
                theme_serializer.is_valid(raise_exception=True)
                theme_serializer.save()

                lek_serializer = DisciplineWorkHoursSerializer(data={
                    "planlineslink_id": pk,
                    "theme_id": theme_serializer.data['id'],
                    "type": DisciplineWorkHours.TypeChoices.lectures,
                    "name": i['tema'] or '-',
                    "hours": i['hour'] or 0,
                    "semester": item['semestr'],
                    "num": i['num'] or 1,
                })
                lek_serializer.is_valid(raise_exception=True)
                lek_serializer.save()

                d2sam = RPDGenSerivce.get_displ2sam(i['id'])

                for sam in d2sam:
                    independent = kind_srs_by_id.get(sam['ckindsrs'], '-')

                    sam_serializer = DisciplineWorkHoursSerializer(data={
                        "planlineslink_id": pk,
                        "theme_id": theme_serializer.data['id'],
                        "type": DisciplineWorkHours.TypeChoices.independent,
                        "name": independent or '-',
                        "hours": sam['hour'] or 0,
                        "semester": item['semestr'],
                        "num": sam['num'] or 1,
                    })
                    sam_serializer.is_valid(raise_exception=True)
                    sam_serializer.save()

                d2pract = RPDGenSerivce.get_displ2pract(i['id'])

                for pract in d2pract:
                    pract_serializer = DisciplineWorkHoursSerializer(data={
                        "planlineslink_id": pk,
                        "theme_id": theme_serializer.data['id'],
                        "type": DisciplineWorkHours.TypeChoices.practice,
                        "name": pract['tema'] or '-',
                        "hours": pract['hour'] or 0,
                        "semester": item['semestr'],
                        "num": pract['num'] or 1,
                    })
                    pract_serializer.is_valid(raise_exception=True)
                    pract_serializer.save()

                d2lab = RPDGenSerivce.get_displ2lab(i['id'])

                for lab in d2lab:
                    lab_serializer = DisciplineWorkHoursSerializer(data={
                        "planlineslink_id": pk,
                        "theme_id": theme_serializer.data['id'],
                        "type": DisciplineWorkHours.TypeChoices.laboratory,
                        "name": lab['tema'] or '-',
                        "hours": lab['hour'] or 0,
                        "semester": item['semestr'],
                        "num": lab['num'] or 1,
                    })
                    lab_serializer.is_valid(raise_exception=True)
                    lab_serializer.save()

        return Response(data={"success": True}, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path="copy-rpd-program", detail=True, permission_classes=[CanEditRPDProgram])
    def copy_new_rpd_program(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        from_pk = int(self.request.data['from_pk'])

        anyone_can_copy = PlanLinesLink.objects.filter(can_be_copied_by_anyone=True, id=from_pk).exists()
        programs = GeneratorService.get_program_list(self.request.user.userprofile.mira_id)
        if not anyone_can_copy and from_pk not in [i['id'] for i in programs if 'person' in i['type']]:
            raise APIException("Вы можете копировать только со своих програм")

        GeneratorService.copy_rpd_program(from_pk, pk)

        return Response(data={"success": True}, status=status.HTTP_200_OK)