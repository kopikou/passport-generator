from rest_framework import serializers
from rop_monitoring.models import RopMonitoring, RopMonitoringScore


class RopMonitoringSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RopMonitoring
        fields = [
            'id',
            'name',
        ]


class RopMonitoringScoreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.SerializerMethodField()
    value_input = serializers.JSONField(write_only=True)

    class Meta:
        model = RopMonitoringScore
        fields = [
            'id',
            'rop_monitoring',
            'admission',
            'person',
            'indicator',
            'value',
            'value_input',
            'score',
        ]

    def get_value(self, obj):
        if obj.value_boolean is not None:
            return obj.value_boolean
        return obj.value_numeric

    def validate(self, attrs):
        value = attrs.pop('value_input', None)
        if value is None:
            raise serializers.ValidationError({'value_input': 'Это поле обязательно.'})

        if isinstance(value, bool):
            attrs['value_boolean'] = value
            attrs['value_numeric'] = None
        elif isinstance(value, (int, float)):
            attrs['value_numeric'] = float(value)
            attrs['value_boolean'] = None
        else:
            raise serializers.ValidationError({'value_input': 'Значение должно быть либо числом, либо булевым.'})

        return attrs
