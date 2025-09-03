from collections import defaultdict

from django.db import transaction
from rest_framework.exceptions import NotFound
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
from rop_monitoring.services import RopMonitor, IndicatorsCalculator, get_monitoring_scores, export_answers_to_excel


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

    INDICATOR_NAMES = {
        4: 'ege',
        5: 'student_contingent',
        6: 'celev_student_contingent',
        7: 'npr',
        8: 'student_sop',
        9: 'employer',
    }

    @action(detail=False, methods=['get'], url_path='grouped')
    def grouped_by_admission(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        rop_monitoring_id = request.query_params.get('rop_monitoring')
        if rop_monitoring_id:
            queryset = queryset.filter(rop_monitoring=rop_monitoring_id)

        grouped_data = self._group_by_admission(queryset, 'get_table')

        grouped_data.sort(key=lambda x: x.get('admission_name', ''))

        return Response(grouped_data)

    @action(methods=["GET"], url_path="export", detail=False)
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        rop_monitoring_id = request.query_params.get('rop_monitoring')
        if rop_monitoring_id:
            queryset = queryset.filter(rop_monitoring=rop_monitoring_id)

            grouped_data = self._group_by_admission(queryset, 'export')

            grouped_data.sort(key=lambda x: x.get('admission_name', ''))
            excel_response = export_answers_to_excel(grouped_data)
            return excel_response
        else:
            raise NotFound

    def _group_by_admission(self, queryset, query_type):
        admission_groups = defaultdict(dict)

        for item in queryset:
            admission_id = item.admission

            if not admission_groups[admission_id]:
                admission_groups[admission_id] = {
                    'id': item.id,
                    'rop_monitoring': item.rop_monitoring.id,
                    'admission': admission_id,
                    'admission_name': item.admission_name,
                    'admission_kind': item.admission_kind,
                    'admission_cprofili': item.admission_cprofili,
                    'admission_cspec': item.admission_cspec,
                    'admission_cdirection': item.admission_cdirection,
                    'person': item.person,
                    'person_name': item.person_name,
                }

            indicator_name = self.INDICATOR_NAMES.get(item.indicator_id)
            if indicator_name:
                admission_groups[admission_id][f'{indicator_name}_score'] = item.score
                admission_groups[admission_id][f'{indicator_name}_value'] = item.value

        if query_type == 'get_table':
            grouped_result = defaultdict(list)

            for admission_dict in admission_groups.values():
                group_key = (
                    admission_dict['admission_cprofili'],
                    admission_dict['admission_cspec'],
                    admission_dict['admission_cdirection']
                )
                grouped_result[group_key].append(admission_dict)

            return list(grouped_result.values())
        else:
            return list(admission_groups.values())

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
                    admission_name=score_data.get('admission_name'),
                    admission_kind=score_data.get('admission_kind'),
                    person=score_data.get('person_id'),
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
