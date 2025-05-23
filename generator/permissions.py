from rest_framework.permissions import BasePermission, IsAuthenticated

from arim.services import AISServices
from generator.models import PlanLinesLink
from generator.services.generator_service import GeneratorService
from uplfile.service import UploadFileService


class CanEditRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для редактирования этого РПД'
    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_edit = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.appointed,
            PlanLinesLink.StatusChoices.is_filled,
            PlanLinesLink.StatusChoices.on_refile,
            PlanLinesLink.StatusChoices.accepted,
        ])

        return int(pk) in [i['id'] for i in programms if 'person' in i['type']] and can_edit.exists()


class CanViewRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для просмотра этого РПД'

    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']
        return int(pk) in [i['id'] for i in programms]

class CanAcceptRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для утверждения этого РПД'
    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.on_review,
        ])

        return int(pk) in [i['id'] for i in programms if 'zav' in i['type']] and can_accept.exists()


class CanConfirmRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для согласования этого РПД'
    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.on_review,
        ])

        return int(pk) in [i['id'] for i in programms if 'rop' in i['type']] and can_accept.exists()


class CanViewFileList(IsAuthenticated):
    message = 'У вас нет прав для просмотра файлов'

    def has_permission(self, request, view):
        programms = UploadFileService.get_admission_data(request.user.userprofile.mira_id)

        return len(programms) > 0


class CanUploadFiles(IsAuthenticated):
    message = 'У вас нет прав для отправки файлов'

    def has_permission(self, request, view):
        programms = UploadFileService.get_admission_data(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        return int(pk) in [i['plan_id'] for i in programms if i['cperson'] == request.user.userprofile.mira_id]