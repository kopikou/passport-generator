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
    admission_name = serializers.SerializerMethodField()
    person_name = serializers.SerializerMethodField()

    class Meta:
        model = RopMonitoringScore
        fields = [
            'id',
            'rop_monitoring',
            'admission',
            'admission_name',
            'person',
            'person_name',
            'indicator',
            'value',
            'score',
        ]

    def get_value(self, obj):
        if obj.value_boolean is not None:
            return obj.value_boolean
        return obj.value_numeric

    def get_admission_name(self, obj):
        from arim.models import Catadmission
        try:
            admission = Catadmission.objects.get(id=obj.admission)
            return admission.name
        except Catadmission.DoesNotExist:
            return None

    def get_person_name(self, obj):
        from arim.models import CatPerson
        try:
            person = CatPerson.objects.get(id=obj.person)
            return person.name
        except CatPerson.DoesNotExist:
            return None
