from rest_framework.permissions import BasePermission, IsAuthenticated

from generator.services.generator_service import GeneratorService


class CanEditRPDProgram(IsAuthenticated):
    def has_permission(self, request, view):
        programms = GeneratorService.get_program_list(request.user.userprofile.mira_id)
        pk = view.kwargs['pk']
        return int(pk) in [i['id'] for i in programms if 'person' in i['type']]

