from app import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from arim.api import ArimViewSet
from auths.views import LoginView, LogoutView, BitrixAuthView
from auths.api import UserApiViewSet
from generator.api.GeneratorViewSet import GeneratorViewSet
from prof_activity.api import ProfActivityViewSet
from rop_monitoring.api import RopMonitoringViewSet, RopMonitoringScoreViewSet
from rpd.api.AccreditationInfoViewSet import AccreditationInfoViewSet
from rpd.api.PlxUploadViewSet import PlxUploadViewSet
from uplfile.api import UploadFileViewSet

from esia_login.urls import urlpatterns as esia_login_urls

router = routers.DefaultRouter()
router.register(r'user', UserApiViewSet, basename="user")
router.register(r'plx', PlxUploadViewSet, basename="plx")
router.register(r'arim', ArimViewSet, basename="arim")
router.register(r'accreditation', AccreditationInfoViewSet, basename="accreditation")
router.register(r'generator', GeneratorViewSet, basename="generator")
router.register(r'upload', UploadFileViewSet, basename="upload")
router.register(r'activity', ProfActivityViewSet, basename="activity")
router.register(r'rop-monitoring', RopMonitoringViewSet, basename="rop-monitoring")
router.register(r'rop-monitoring-score', RopMonitoringScoreViewSet, basename="rop-monitoring-score")

# router_old = routers.DefaultRouter()
# router_old.register(r'asp', AspPlanViewSet, basename="asp")

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', include('loginas.urls')),
    path('api/accounts/login/', LoginView.as_view()),
    path('api/accounts/logout/', LogoutView.as_view()),
    path('api/accounts/bitrix-auth/', BitrixAuthView.as_view()),
    path('admin/', admin.site.urls),
] + esia_login_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


