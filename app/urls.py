from app import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from arim.api import ArimViewSet
from auths.views import LoginView, LogoutView, BitrixAuthView
from auths.api import UserApiViewSet
from generator.api.GeneratorViewSet import GeneratorViewSet
from rpd.api.AccreditationInfoViewSet import AccreditationInfoViewSet
from rpd.api.PlxUploadViewSet import PlxUploadViewSet
from uplfile.api import UploadFileViewSet

router = routers.DefaultRouter()
router.register(r'user', UserApiViewSet, basename="user")
router.register(r'plx', PlxUploadViewSet, basename="plx")
router.register(r'arim', ArimViewSet, basename="arim")
router.register(r'accreditation', AccreditationInfoViewSet, basename="accreditation")
router.register(r'generator', GeneratorViewSet, basename="generator")
router.register(r'upload', UploadFileViewSet, basename="upload")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', include('loginas.urls')),
    path('api/accounts/login/', LoginView.as_view()),
    path('api/accounts/logout/', LogoutView.as_view()),
    path('api/accounts/bitrix-auth/', BitrixAuthView.as_view()),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

