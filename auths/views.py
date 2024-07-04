from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import json
import django.middleware.csrf
import requests
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from auths.models import UserProfile
from auths.serializer import UserSerializer


# Create your views here.
class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        login_form = AuthenticationForm(request, data)
        response_data = {}
        if login_form.is_valid():
            auth_login(self.request, login_form.get_user())
            response_data['result'] = 'Success!'
            response_data['message'] = 'You"re logged in'
            response_data['csrf'] = django.middleware.csrf.get_token(request)
        else:
            response_data['result'] = 'Failed'
            response_data['message'] = 'Неправильный пароль и пользователь'

        return JsonResponse(response_data)


class LogoutView(View):
    def get(self, *args, **kwargs):
        auth_logout(self.request)
        return redirect("/")


class BitrixAuthView(APIView):
    permission_classes = []

    class InnerSerializer(serializers.Serializer):
        code = serializers.CharField()
        state = serializers.CharField(required=False)
        domain = serializers.CharField(required=False)
        member_id = serializers.CharField(required=False)
        scope = serializers.CharField(required=False)
        server_domain = serializers.CharField(required=False)

    def default_auth_processor(self, state, user):
        auth_login(self.request, user)
        return redirect("/")

    def visit_auth_processor(self, state, user):
        auth_login(self.request, user)
        return redirect(f"/view/visit-confirmed/{state['data']}")

    def get(self, request, *args, **kwargs):
        serializer = self.InnerSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        HTTP_REFERER = request.META.get('HTTP_REFERER') or "/"

        r = requests.get("https://int.istu.edu/oauth/token/?grant_type=authorization_code", {
            "code": serializer.validated_data['code'],
            "client_id": settings.BITRIX_CLIENT_ID,
            "client_secret": settings.BITRIX_SECRET_KEY,
        }, verify=False)

        response_data = {}

        data = r.json()
        if r.status_code != 200:
            # messages.add_message(request, messages.WARNING, data['error_description'])
            return redirect(HTTP_REFERER)

        data = r.json()
        r = requests.get(data['client_endpoint'] + 'user.info.json', {
            "auths": data['access_token'],
        })
        if r.status_code != 200:
            response_data['result'] = 'Failed'
            response_data['message'] = data['error_description']
            return redirect(HTTP_REFERER)

        data = r.json()
        result = data['result']

        bitrix_user_id = result['id']
        email = result['email']
        user, created = User.objects.get_or_create(
            userprofile__bitrix_user_id=bitrix_user_id,
            defaults={
                "username": email,
                "last_name": result['last_name'] or "",
                "first_name": result['name'] or "",
                "email": result['email'],
            }
        )

        if created:
            user.userprofile.bitrix_user_id = bitrix_user_id
            user.userprofile.save()

        user.userprofile.is_teacher = bool(result['is_teacher'])
        user.userprofile.is_student = bool(result['is_student'])

        mira_id = int(result['mira_id'][0] if result['mira_id'] or 0 else 0)
        if mira_id > 2:
            user.userprofile.mira_id = mira_id

        user.userprofile.save()

        return redirect("/")


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
            })

        return JsonResponse(data)

