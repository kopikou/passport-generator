from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from rop_monitoring.models import RopMonitoring
from rop_monitoring.serializers import RopMonitoringSerializer
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

    @action(methods=['GET'], url_path="count-rop-score", detail=False)
    def count_rop_score(self, request, *args, **kwargs):
        monitor = RopMonitor()
        admissions = monitor.get_admissions()
        ege_indicator = monitor.get_ege_indicator()
        student_contingent_indicator = monitor.get_student_contingent_indicator()
        celev_student_contingent_indicator = monitor.get_celev_student_contingent_indicator()

        admission_indicators = []
        for id, admission in admissions.items():
            ege = ege_indicator.get(id)
            contingent = student_contingent_indicator.get(id)
            celev = celev_student_contingent_indicator.get(id)

            if ege:
                admission_indicators.append({
                    'id': id,
                    'name': admission['admission_name'],
                    'rop_id': admission['admission_rop_id'],
                    'rop': admission['admission_rop'],
                    'ege_avg_marks': ege['avg_marks'] if ege else 0,
                    'ege_avg_marks_score': ege['avg_marks_score'] if ege else 0,
                    'contingent_students_ratio': contingent['contingent_students_ratio'] if contingent else 0,
                    'contingent_students_ratio_score': contingent[
                        'contingent_students_ratio_score'] if contingent else 0,
                    'celev_students_ratio': celev['celev_students_ratio'] if celev else 0,
                    'celev_students_ratio_score': celev['celev_students_ratio_score'] if celev else 0,
                })

        admission_indicators.sort(key=lambda admission: admission["name"])
        return Response(admission_indicators, status=status.HTTP_200_OK)
