import pendulum
from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAuthenticated

from arim.services import AISServices
from generator.models import PlanLinesLink
from generator.services.generator_service import GeneratorService


class CanEditRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для редактирования этого РПД'

    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        practices = GeneratorService.get_practice_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_edit = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.appointed,
            PlanLinesLink.StatusChoices.is_filled,
            PlanLinesLink.StatusChoices.on_refile,
            PlanLinesLink.StatusChoices.accepted,
        ])

        program = int(pk) in [i['id'] for i in programms if 'person' in i['type']] and can_edit.exists()
        practice = int(pk) in [i['id'] for i in practices]

        return program or practice


class CanEditScientificProgram(IsAuthenticated):
    message = 'У вас нет прав для редактирования этого ПНД'

    def has_permission(self, request, view):
        pk = view.kwargs['pk']

        year = request.query_params.get('year', pendulum.now().year)
        plans = GeneratorService.get_asp_list(year, request.user)

        return int(pk) in [i['id'] for i in plans]


class CanViewRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для просмотра этого РПД'

    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        practices = GeneratorService.get_practice_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']
        program = int(pk) in [i['id'] for i in programms]
        practice = int(pk) in [i['id'] for i in practices]
        return program or practice


class CanAcceptRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для утверждения этого РПД'

    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        practices = GeneratorService.get_practice_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(
            Q(status__in=[PlanLinesLink.StatusChoices.on_review], planlines__viewpract__isnull=True)
            | (~Q(status__in=[PlanLinesLink.StatusChoices.accepted]) & Q(planlines__viewpract__isnull=False))
            , id=pk)

        program = int(pk) in [i['id'] for i in programms if 'zav' in i['type']] and can_accept.exists()
        practice = int(pk) in [i['id'] for i in practices]

        return program or practice


class CanConfirmRPDProgram(IsAuthenticated):
    message = 'У вас нет прав для согласования этого РПД'

    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']

        can_accept = PlanLinesLink.objects.filter(id=pk, status__in=[
            PlanLinesLink.StatusChoices.on_review,
        ])

        return int(pk) in [i['id'] for i in programms if 'rop' in i['type']] and can_accept.exists()

