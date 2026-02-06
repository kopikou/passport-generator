from rest_framework.permissions import BasePermission, IsAuthenticated
from arim.services import AISServices
from django.conf import settings
from auths.models import UserProfile, Permissions
class CanViewCompetencePassport(IsAuthenticated):
    """Разрешение на просмотр паспорта компетенций — только для РОП"""
    message = 'У вас нет прав для просмотра паспорта компетенций'

    # def has_permission(self, request, view):
    #     if not super().has_permission(request, view):
    #         return False
            
    #     if request.user.is_superuser:
    #         return True
            
    #     pk = view.kwargs['pk']
    #     if settings.DISABLE_MIRA:
    #         return pk == '4107'
    #     info = AISServices.get_plan_users_info(pk)
    #     mira_id = request.user.userprofile.mira_id
        
    #     # Только РОП может просматривать
    #     return mira_id == info['rop']

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user

        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return False

        if Permissions.can_use_competence_passport_generator not in profile.permissions:
            return False

        return True


class CanEditCompetencePassport(IsAuthenticated):
    """Разрешение на редактирование паспорта компетенций — только для РОП"""
    message = 'У вас нет прав для редактирования паспорта компетенций'

    # def has_permission(self, request, view):
    #     if not super().has_permission(request, view):
    #         return False
            
    #     if request.user.is_superuser:
    #         return True
            
    #     pk = view.kwargs['pk']
    #     if settings.DISABLE_MIRA:
    #         return pk == '4107'
    #     info = AISServices.get_plan_users_info(pk)
    #     mira_id = request.user.userprofile.mira_id
        
    #     # Только РОП может редактировать
    #     return mira_id == info['rop']
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user

        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return False

        if Permissions.can_use_competence_passport_generator not in profile.permissions:
            return False

        return True
