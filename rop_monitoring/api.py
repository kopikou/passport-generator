from django.db import transaction
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from rop_monitoring.filters import RopMonitoringScoreFilter, RopMonitoringFilter
from rop_monitoring.models import (RopMonitoring, RopMonitoringScore, Indicator, AdmissionKinds, MiraAdmissionKinds,
                                   Indicators)
from rop_monitoring.permissions import CanEditRopMonitoring
from rop_monitoring.serializers import RopMonitoringSerializer, RopMonitoringScoreSerializer
from rop_monitoring.services import RopMonitor, IndicatorsCalculator, get_monitoring_scores


class RopMonitoringViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RopMonitoring.objects.all()
    serializer_class = RopMonitoringSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RopMonitoringFilter
    ordering_fields = ['name']
    ordering = ['name']


class RopMonitoringScoreViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RopMonitoringScore.objects.all()
    serializer_class = RopMonitoringScoreSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RopMonitoringScoreFilter
    ordering_fields = ['admission_name']
    ordering = ['admission_name']

    @action(methods=['GET'], url_path="update-monitoring-data", detail=True, permission_classes=[CanEditRopMonitoring])
    def update_monitoring_data(self, request, *args, **kwargs):
        monitoring_id = kwargs.get('pk')
        rop_monitoring = RopMonitoring.objects.filter(id=monitoring_id).first()
        rop_monitoring_scores = get_monitoring_scores(monitoring_id)

        with transaction.atomic():
            results = []
            for score_data in rop_monitoring_scores:
                indicator = Indicator.objects.get(id=score_data.get('indicator_id'))
                obj, created = RopMonitoringScore.objects.update_or_create(
                    rop_monitoring=rop_monitoring,
                    admission=score_data.get('admission'),
                    person=score_data.get('person_id'),
                    admission_name=score_data.get('admission_name'),
                    person_name=score_data.get('person_name'),
                    indicator=indicator,
                    defaults={
                        'value_numeric': score_data.get('value_numeric'),
                        'value_boolean': score_data.get('value_boolean'),
                        'score': score_data.get('score'),
                    }
                )
                results.append(obj)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
