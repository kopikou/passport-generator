from rest_framework import serializers
from rop_monitoring.models import RopMonitoring, RopMonitoringScore


class RopMonitoringSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RopMonitoring
        fields = [
            'id',
            'name',
            'year'
        ]


class RopMonitoringScoreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.SerializerMethodField()

    class Meta:
        model = RopMonitoringScore
        fields = [
            'id',
            'rop_monitoring',
            'admission',
            'admission_name',
            'admission_kind',
            'person',
            'person_name',
            'indicator',
            'value',
            'score',
            'count',
            'res'
        ]

    def get_value(self, obj):
        if obj.value_boolean is not None:
            return obj.value_boolean
        return obj.value_numeric
