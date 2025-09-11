from rest_framework.permissions import IsAuthenticated

from auths.models import UserProfile, Permissions


class CanEditRopMonitoring(IsAuthenticated):
    message = 'У вас нет прав для редактирования мониторингов РОПов'

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user

        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return False

        if Permissions.can_monitor_rops not in profile.permissions:
            return False

        return True