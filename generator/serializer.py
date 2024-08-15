from rest_framework import serializers

from generator.models import PlanLinesLink


class PlanLinesLinkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cadmission = serializers.IntegerField()
    mira_id = serializers.IntegerField()
    person = serializers.IntegerField()
    status = serializers.IntegerField()
    status_verbose = serializers.CharField(read_only=True)

    class Meta:
        model = PlanLinesLink
        fields = [
            'id',
            'cadmission',
            'mira_id',
            'person',
            'status',
            'status_verbose',
        ]

