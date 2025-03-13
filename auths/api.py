from django.conf import settings
from django.db import models, connection
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin

from auths.models import UserProfile
from auths.serializer import UserSerializer

import django.middleware.csrf
import requests

from rpd.models import RPDFile

def foreign_tables(table, all_tables):
    result = []

    for model in all_tables:
        # print(model.objects.all())
        for field in model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                # print(field.related_model._meta.db_table)
                if field.related_model._meta.db_table == table:
                    result.append(model._meta.db_table)

    return result

class UserApiViewSet(ListModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], url_path="test", detail=False)
    def test(self, request, *args, **kwargs):

        instance = RPDFile.objects.get(id=1)

        result = []

        table = instance._meta.db_table
        tables = connection.introspection.table_names()
        seen_models = connection.introspection.installed_models(tables)

        res = foreign_tables(table, seen_models)
        ftables = []
        while res:
            for r in res:
                ftables.append(r)
                res = foreign_tables(r, seen_models)

        print(ftables)
        return Response(result)

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
            'FORCE_SCRIPT_NAME': settings.FORCE_SCRIPT_NAME or "",
        }

        if self.request.user.is_authenticated:
            data.update({
                "user_id": self.request.user.id,
                "username": self.request.user.username,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "mira_id": self.request.user.userprofile.mira_id,
                'is_superuser': self.request.user.is_superuser,
                'is_staff': self.request.user.is_staff,
                'is_student': self.request.user.userprofile.is_student,
                'is_teacher': self.request.user.userprofile.is_teacher,
                'permissions': self.request.user.userprofile.permissions,
            })

        return JsonResponse(data)