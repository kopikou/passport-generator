import pendulum
from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAuthenticated

from arim.services import AISServices
from generator.models import PlanLinesLink
from generator.services.generator_service import GeneratorService
from uplfile.service import UploadFileService


class ProgramListPermissionMixin(object):
    def get_program_list(self, request, view):
        programs = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        setattr(view, 'programs', programs)
        return programs


class CanEditRPDProgram(ProgramListPermissionMixin, IsAuthenticated):
    message = 'У вас нет прав для редактирования этого РПД'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        pk = view.kwargs['pk']

        can_edit = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.appointed,
            PlanLinesLink.StatusChoices.is_filled,
            PlanLinesLink.StatusChoices.on_refile,
            PlanLinesLink.StatusChoices.accepted,
        ])

        pk = view.kwargs['pk']
        info = AISServices.get_plan_users_info(pk)
        mira_id = request.user.userprofile.mira_id

        return (mira_id == info['razrab']) and can_edit.exists()


class CanEditScientificProgram(ProgramListPermissionMixin,IsAuthenticated):
    message = 'У вас нет прав для редактирования этого ПНД'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        pk = view.kwargs['pk']

        year = request.query_params.get('year', pendulum.now().year)
        plans = GeneratorService.get_asp_list(year, request.user).get('items', [])

        return int(pk) in [i['id'] for i in plans]


class CanViewRPDProgram(ProgramListPermissionMixin, IsAuthenticated):
    message = 'У вас нет прав для просмотра этого РПД'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.user.is_superuser:
            return True

        pk = view.kwargs['pk']
        info = AISServices.get_plan_users_info(pk)
        mira_id = request.user.userprofile.mira_id

        return mira_id == info['razrab'] \
            or mira_id == info['zavkaf'] \
            or mira_id == info['rop'] \
            or mira_id == info['fac']


class CanAcceptRPDProgram(ProgramListPermissionMixin, IsAuthenticated):
    message = 'У вас нет прав для утверждения этого РПД'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(
            Q(status__in=[PlanLinesLink.StatusChoices.on_review], planlines__viewpract__isnull=True)
            | (~Q(status__in=[PlanLinesLink.StatusChoices.accepted]) & Q(planlines__viewpract__isnull=False))
            , id=pk)

        info = AISServices.get_plan_users_info(pk)
        mira_id = request.user.userprofile.mira_id

        return (mira_id == info['zavkaf']) and can_accept.exists()


class CanConfirmRPDProgram(ProgramListPermissionMixin, IsAuthenticated):
    message = 'У вас нет прав для согласования этого РПД'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.on_review,
        ])

        info = AISServices.get_plan_users_info(pk)
        mira_id = request.user.userprofile.mira_id

        return (mira_id == info['zavkaf']) and can_accept.exists()


class CanUploadRPDProgramFile(ProgramListPermissionMixin, IsAuthenticated):
    message = 'У вас нет прав для загрузки файла этого РПД напрямую '

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        programms = self.get_program_list(request, view)
        pk = view.kwargs['pk']

        return int(pk) in [i['id'] for i in programms if 'person' in i['type'] and i['can_upload_file_directly']]


class CanViewFileList(IsAuthenticated):
    # message = 'У вас нет прав для просмотра файлов'
    message = 'Нет файлов для просмотра'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        programms = UploadFileService.get_admission_data(request.user.userprofile.mira_id)

        return len(programms) > 0


class CanUploadFiles(IsAuthenticated):
    message = 'У вас нет прав для отправки файлов'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        programms = UploadFileService.get_admission_data(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        return int(pk) in [i['plan_id'] for i in programms]

