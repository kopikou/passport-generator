from django.db import transaction
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from rop_monitoring.filters import RopMonitoringScoreFilter, RopMonitoringFilter
from rop_monitoring.models import RopMonitoring, RopMonitoringScore, Indicator, AdmissionTypes, Indicators
from rop_monitoring.permissions import CanEditRopMonitoring
from rop_monitoring.serializers import RopMonitoringSerializer, RopMonitoringScoreSerializer
from rop_monitoring.services import RopMonitor


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
    ordering_fields = ['rop_monitoring']
    ordering = ['rop_monitoring']

    @action(methods=['GET'], url_path="update-monitoring-data", detail=True, permission_classes=[CanEditRopMonitoring])
    def update_monitoring_data(self, request, *args, **kwargs):
        monitoring_id = kwargs.get('pk')

        monitor = RopMonitor()
        admissions = monitor.get_admissions()
        # ege_indicator = monitor.get_ege_indicator()
        # student_contingent_indicator = monitor.get_student_contingent_indicator()
        # celev_student_contingent_indicator = monitor.get_celev_student_contingent_indicator()

        calculator = CalcIndiators()

        rop_monitoring_scores = []
        for admission_id, admission in admissions.items():
            # ege = ege_indicator.get(admission_id)
            # contingent = student_contingent_indicator.get(admission_id)
            # celev = celev_student_contingent_indicator.get(admission_id)

            # if ege:
                # admission_type = None

                # if admission['admission_type'] in [1, 2]:
                #     admission_type = AdmissionTypes.BACH_SPEC.value
                # elif admission['admission_type'] in [3]:
                #     admission_type = AdmissionTypes.MAG.value

                # if admission_type is not None:
                indicators = list(Indicator.objects.filter(types__contains=[admission_type]).values())

                for indicator in indicators:
                    value = None
                    score = None
                    value, score = calculator.get_inidcator_score_value(admission_id, indicator['id'])
                    # if indicator['id'] == Indicators.EGE.value:
                    #     value, score = calculator.get_ege_indicator(admission_id=admission_id)
                    #     # value = ege['avg_marks'] if ege else 0
                    #     # score = ege['avg_marks_score'] if ege else 0
                    # elif indicator['id'] == Indicators.STUD_CONTINGENT.value:
                    #     value = contingent['contingent_students_ratio'] if contingent else 0
                    #     score = contingent['contingent_students_ratio_score'] if contingent else 0
                    # elif indicator['id'] == Indicators.CELEV_STUD_CONTINGENT.value:
                    #     value = celev['celev_students_ratio'] if celev else 0
                    #     score = celev['celev_students_ratio_score'] if celev else 0

                    if value is not None:
                        rop_id = admission['admission_rop_id']

                        rop_monitoring_scores.append({
                            "rop_monitoring": monitoring_id,
                            "admission": admission_id,
                            "person": rop_id,
                            "indicator": indicator['id'],
                            "value": value,
                            "score": score,
                        })

        with transaction.atomic():
            results = []
            for data in rop_monitoring_scores:
                rop_monitoring = RopMonitoring.objects.filter(id=data['rop_monitoring']).first()
                indicator = Indicator.objects.filter(id=data['indicator']).first()

                value = data.get('value')
                value_numeric = None
                value_boolean = None

                if isinstance(value, bool):
                    value_boolean = value
                elif isinstance(value, (int, float)):
                    value_numeric = float(value)
                elif value is None:
                    pass
                else:
                    raise ValueError(f"Unexpected value type: {type(value)} for value: {value}")

                obj, created = RopMonitoringScore.objects.update_or_create(
                    rop_monitoring=rop_monitoring,
                    admission=data['admission'],
                    person=data['person'],
                    indicator=indicator,
                    defaults={
                        'value_numeric': value_numeric,
                        'value_boolean': value_boolean,
                        'score': data.get('score'),
                    }
                )
                results.append(obj)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
