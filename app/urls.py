from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from auths.views import LoginView, LogoutView, BitrixAuthView
from auths.api import UserApiViewSet

from rpd.api import PlxUploadViewSet

router = routers.DefaultRouter()
router.register(r'user', UserApiViewSet, basename="user")
router.register(r'upload', PlxUploadViewSet, basename="upload")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', include('loginas.urls')),
    path('api/accounts/login/', LoginView.as_view()),
    path('api/accounts/logout/', LogoutView.as_view()),
    path('api/accounts/bitrix-auth/', BitrixAuthView.as_view()),
    path('admin/', admin.site.urls),
]

