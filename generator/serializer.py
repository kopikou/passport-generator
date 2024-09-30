from rest_framework import serializers

from generator.models import PlanLinesLink, DisciplineIndicators, DisciplineThemes, DisciplineWorkHours
from rpd.models import LinesData, LinesIndicators
from rpd.serializer import LinesDataSerializer, SemesterDataSerializer, LinesIndicatorsSerializer, PlanDataSerializer


class DisciplineIndicatorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    indicator_id = serializers.IntegerField()
    planlineid_id = serializers.IntegerField()
    know = serializers.CharField()
    able = serializers.CharField()
    own = serializers.CharField()
    criteria = serializers.CharField()
    methods = serializers.CharField()

    class Meta:
        model = DisciplineIndicators
        fields = [
            'id',
            'indicator_id',
            'planlineid_id',
            'know',
            'able',
            'own',
            'criteria',
            'methods',
        ]


class DisciplineIndicatorsAddSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    indicator_id = serializers.IntegerField(required=True)
    planlineid_id = serializers.IntegerField(required=True)
    know = serializers.CharField(allow_null=True, allow_blank=True)
    able = serializers.CharField(allow_null=True, allow_blank=True)
    own = serializers.CharField(allow_null=True, allow_blank=True)
    criteria = serializers.CharField(allow_null=True, allow_blank=True)
    methods = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = DisciplineIndicators
        fields = [
            'id',
            'indicator_id',
            'planlineid_id',
            'know',
            'able',
            'own',
            'criteria',
            'methods',
        ]

    def create(self, validate_data):
        discipline_indicators, created = DisciplineIndicators.objects.update_or_create(
            indicator_id=validate_data.get('indicator_id'),
            planlineid_id=validate_data.get('planlineid_id'),
            defaults=validate_data,
        )

        return discipline_indicators


class GeneratorLinesIndicatorsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    planlineid_id = serializers.IntegerField()
    competence_index = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    competence = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    indicator_index = serializers.CharField()
    indicator = serializers.CharField()

    discipline_indicator = DisciplineIndicatorsSerializer(many=True)


    class Meta:
        model = LinesIndicators
        fields = [
            'id',
            'planlineid_id',
            'competence_index',
            'competence',
            'indicator_index',
            'indicator',
            'discipline_indicator',
        ]


class GeneratorLinesDataSerializer(LinesDataSerializer):
    semesters = SemesterDataSerializer(many=True)
    indicators = GeneratorLinesIndicatorsSerializer(many=True)
    plan = PlanDataSerializer()

    class Meta(LinesDataSerializer.Meta):
        fields = LinesDataSerializer.Meta.fields + ['semesters', 'indicators', 'plan']


class DisciplineThemeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    planlineslink_id = serializers.IntegerField()
    name = serializers.CharField()
    semester = serializers.IntegerField()
    formcontrol_id = serializers.IntegerField()
    comment = serializers.CharField()

    class Meta:
        model = DisciplineThemes
        fields = [
            'id',
            'planlineslink_id',
            'name',
            'semester',
            'formcontrol_id',
            'comment',
        ]

    def create(self, validate_data):
        discipline_themes, created = DisciplineThemes.objects.update_or_create(
            id=validate_data['id'],
            defaults=validate_data,
        )

        return discipline_themes


class PlanLinesLinkSaveGeneratorDisciplineDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    precedence_discipline = serializers.ListSerializer(child=serializers.IntegerField(), allow_null=True,
                                                       allow_empty=True, required=False)
    subsequent_discipline = serializers.ListSerializer(child=serializers.IntegerField(), allow_null=True,
                                                       allow_empty=True, required=False)
    library = serializers.JSONField(allow_null=True, required=False)
    software = serializers.JSONField(allow_null=True, required=False)
    logistics = serializers.JSONField(allow_null=True, required=False)
    interactive_methods = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = PlanLinesLink
        fields = [
            'id',
            'precedence_discipline',
            'subsequent_discipline',
            'library',
            'software',
            'logistics',
            'interactive_methods',
        ]


class DisciplineWorkHoursSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    planlineslink_id = serializers.IntegerField()
    theme_id = serializers.IntegerField()
    type = serializers.IntegerField()
    name = serializers.CharField()
    hours = serializers.FloatField()
    semester = serializers.IntegerField()

    class Meta:
        model = DisciplineWorkHours
        fields = [
            'id',
            'planlineslink_id',
            'theme_id',
            'type',
            'type_verbose',
            'name',
            'hours',
            'semester',
        ]

    def create(self, validate_data):
        discipline_themes, created = DisciplineWorkHours.objects.update_or_create(
            id=validate_data['id'],
            defaults=validate_data,
        )

        return discipline_themes


class PlanLinesLinkSerializer(serializers.Serializer):
    planlines = GeneratorLinesDataSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    cadmission = serializers.IntegerField()
    mira_id = serializers.IntegerField()
    person = serializers.IntegerField()
    status = serializers.IntegerField()
    status_verbose = serializers.CharField(read_only=True)
    precedence_discipline = serializers.ListField(child=serializers.IntegerField(), allow_null=True, allow_empty=True,
                                                  required=False)
    subsequent_discipline = serializers.ListField(child=serializers.IntegerField(), allow_null=True, allow_empty=True,
                                                  required=False)

    discipline_themes = DisciplineThemeSerializer(many=True)
    discipline_work_hour = DisciplineWorkHoursSerializer(many=True)

    library = serializers.JSONField(allow_null=True, required=False)
    software = serializers.JSONField(allow_null=True, required=False)
    logistics = serializers.JSONField(allow_null=True, required=False)
    interactive_methods = serializers.CharField(allow_null=True, required=False)

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
            'precedence_discipline',
            'subsequent_discipline',

            'discipline_themes',
            'discipline_work_hour',
            'library',
            'software',
            'logistics',
            'interactive_methods',
        ]
