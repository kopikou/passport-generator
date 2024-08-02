from django.conf import settings
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin

from auths.models import UserProfile
from auths.serializer import UserSerializer

import django.middleware.csrf
import requests



class UserApiViewSet(ListModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(is_teacher=True)

        return queryset

    @action(['GET'], url_path="checkLogin", detail=False, permission_classes=[])
    def check_login(self, request, *args, **kwargs):
        data = {
            "authenticated": bool(self.request.user and self.request.user.is_authenticated),
            'csrf': django.middleware.csrf.get_token(request),
            'BITRIX_CLIENT_ID': settings.BITRIX_CLIENT_ID,
        }

        if self.request.user.is_authenticated:
            data.update({
                "user_id": self.request.user.id,
                "username": self.request.user.username,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                'is_superuser': self.request.user.is_superuser,
                'is_staff': self.request.user.is_staff,
                'is_student': self.request.user.userprofile.is_student,
                'is_teacher': self.request.user.userprofile.is_teacher,
                'permissions': self.request.user.userprofile.permissions,
            })

        return JsonResponse(data)