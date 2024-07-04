from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rpd.api import UploadViewSet

router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")

urlpatterns = [
    path('api/', include(router.urls)),
]

