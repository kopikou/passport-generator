from rest_framework import serializers

from generator.models import PlanLinesLink
from rpd.models import LinesData
from rpd.serializer import LinesDataSerializer, SemesterDataSerializer, LinesIndicatorsSerializer


class GeneratorLinesDataSerializer(LinesDataSerializer):
    semesters = SemesterDataSerializer(many=True)
    indicators = LinesIndicatorsSerializer(many=True)

    class Meta(LinesDataSerializer.Meta):
        fields = LinesDataSerializer.Meta.fields + ['semesters', 'indicators']

class PlanLinesLinkSerializer(serializers.Serializer):
    planlines = GeneratorLinesDataSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    cadmission = serializers.IntegerField()
    mira_id = serializers.IntegerField()
    person = serializers.IntegerField()
    status = serializers.IntegerField()
    status_verbose = serializers.CharField(read_only=True)

    class Meta:
        model = PlanLinesLink
        fields = [
            'planlines',

            'id',
            'cadmission',
            'mira_id',
            'person',
            'status',
            'status_verbose',
        ]

