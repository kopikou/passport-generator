from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, NumberFilter

from rop_monitoring.models import RopMonitoringScore, RopMonitoring


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class RopMonitoringFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = RopMonitoring
        fields = [
            'name',
        ]


class RopMonitoringScoreFilter(filters.FilterSet):
    rop_monitoring = NumberInFilter()

    class Meta:
        model = RopMonitoringScore
        fields = [
            'id',
            'rop_monitoring',
        ]
