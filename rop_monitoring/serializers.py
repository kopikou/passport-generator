from rest_framework import serializers
from rop_monitoring.models import RopMonitoring


class RopMonitoringSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RopMonitoring
        fields = [
            'id',
            'name',
        ]