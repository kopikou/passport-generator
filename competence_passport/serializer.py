from rest_framework import serializers
from competence_passport.models import Scheme, Competence
from rpd.serializer import PlanDataSerializer, LinesIndicatorsSerializer
from rpd.models import LinesIndicators, PlanData

class PlanSerializer(PlanDataSerializer):
    id = serializers.IntegerField()
    class Meta(PlanDataSerializer.Meta):
        model = PlanData
        fields = [
            'id',
            'mira_id',
            'file_id',
            'planname',
            'studyform',
            'studylevel',
            'vuzname',
            'faculty',
            'kafcode',
            'species',
            'napr_e',
            'napr_t',
            'lastshifr',
            'abbrprofile',
            'startyear',
        ]

class IndicatorSerializer(LinesIndicatorsSerializer):
    indicator_index = serializers.CharField(allow_blank=True, allow_null=True)
    indicator = serializers.CharField(allow_blank=True, allow_null=True)
    class Meta:
        model = LinesIndicators
        fields = [
            'indicator_index',
            'indicator'
        ]

class CompetenceSerializer(LinesIndicatorsSerializer):
    type = serializers.CharField(allow_blank=True, allow_null=True)
    indicator_list = IndicatorSerializer(many=True, allow_empty=True)
    class Meta:
        model = LinesIndicators
        fields = [
            'type',
            'competence_index',
            'competence',
            'indicator_list'
        ]

class CompetenceMatrixSerializer(serializers.Serializer):
    """Сериализатор для одного элемента матрицы (группа или дисциплина)"""
    type = serializers.CharField()  # 'group' или 'discipline'
    level = serializers.IntegerField()  # Уровень вложенности
    discipline_id = serializers.IntegerField()
    discipline_index = serializers.CharField() 
    discipline_name = serializers.CharField()
    competence_list = CompetenceSerializer(many=True, allow_empty=True)


class SchemeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    planlineid_id = serializers.IntegerField()
    competence_id = serializers.IntegerField()
    semester = serializers.IntegerField()
    ekz = serializers.BooleanField(allow_null=True)
    zach = serializers.BooleanField(allow_null=True)
    zacho = serializers.BooleanField(allow_null=True)
    kp = serializers.BooleanField(allow_null=True)
    kr = serializers.BooleanField(allow_null=True)
    class Meta:
        model = Scheme
        fields = [
            'id',
            'planlineid_id',
            'competence_id',
            'semester',
            'ekz',
            'zach',
            'zacho',
            'kp',
            'kr',
        ]
class SemesterSerializer(serializers.Serializer):
    semester = serializers.IntegerField()
    form_control = serializers.ListField()

class DisciplineSerializer(serializers.Serializer):
    discipline_id = serializers.IntegerField()
    discipline_index = serializers.CharField() 
    discipline_name = serializers.CharField()
    semester_data = SemesterSerializer(many=True, allow_empty=True)

class CompetenceSchemaSerializer(serializers.Serializer):
    """Serializer для одного элемента схемы компетенций"""
    competence_index = serializers.CharField()
    competence = serializers.CharField()
    discipline_list = DisciplineSerializer(many=True, allow_empty=True)

class CompetenceRelationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    plan_id = serializers.IntegerField()
    competence_index = serializers.CharField(allow_blank=True, allow_null=True)
    competence = serializers.CharField(allow_blank=True, allow_null=True)
    relations = serializers.CharField(allow_blank=True, allow_null=True, required=False, default="")

    class Meta:
        model = Competence
        fields = ['id', 'plan_id', 'competence_index', 'competence', 'relations']

    def create(self, validated_data):
        validated_data.pop('id', None)

        obj, created = Competence.objects.update_or_create(
            plan_id=validated_data['plan_id'],
            competence_index=validated_data['competence_index'],
            defaults=validated_data
        )
        return obj

class CompetenceFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id', 'plan_id', 'competence_index', 'competence', 'relations', 'final_indicator']

class CompetenceWithDisciplineIndicators(serializers.Serializer):
    """Serializer для индикаторов дисциплин"""
    indicator_id = serializers.IntegerField()
    indicator_index = serializers.CharField(allow_blank=True, allow_null=True)
    indicator = serializers.CharField(allow_blank=True, allow_null=True)
    discipline_id = serializers.IntegerField()
    discipline_index = serializers.CharField() 
    discipline_name = serializers.CharField()
    know = serializers.CharField(allow_blank=True, allow_null=True)
    able = serializers.CharField(allow_blank=True, allow_null=True)
    own = serializers.CharField(allow_blank=True, allow_null=True)
    criteria = serializers.CharField(allow_blank=True, allow_null=True)
    methods = serializers.CharField(allow_blank=True, allow_null=True)


class CompetencePassportSerializer(serializers.Serializer):
    """Serializer для одного элемента паспорта компетенций"""
    competence_index = serializers.CharField(allow_null=True, allow_blank=True)
    type = serializers.CharField(allow_blank=True, allow_null=True)
    competence = serializers.CharField(allow_null=True, allow_blank=True)
    competence_relations = serializers.CharField(allow_null=True, allow_blank=True)
    competence_final_indicator = serializers.CharField(allow_null=True, allow_blank=True)
    indicator_list = CompetenceWithDisciplineIndicators(many=True, allow_empty=True)

class CompetenceSerializer(serializers.Serializer):
    """Serializer для компетенции"""
    competence_index = serializers.CharField(allow_null=True, allow_blank=True)
    competence = serializers.CharField(allow_null=True, allow_blank=True)
    type = serializers.CharField(allow_blank=True, allow_null=True)
    
class DisciplineSerializer(serializers.Serializer):
    """Serializer для дисциплины"""
    discipline_id = serializers.IntegerField()
    discipline_index = serializers.CharField() 
    discipline_name = serializers.CharField()
    type = serializers.ListField(child=serializers.CharField(), allow_empty=True)


class CompetencePassportDataSerializer(serializers.Serializer):
    """Serializer для всех данных матрицы, схемы и паспорта"""
    plan = PlanSerializer()
    admission_info = serializers.DictField()
    competences = CompetenceSerializer(many=True)
    disciplines = DisciplineSerializer(many=True)
    matrix = CompetenceMatrixSerializer(many=True)
    schema = CompetenceSchemaSerializer(many=True)
    passport = CompetencePassportSerializer(many=True)

class PlanAdmissionInfoSerializer(serializers.Serializer):
    plan = PlanSerializer()
    admission_info = serializers.DictField()

class ReferenceDataSerializer(serializers.Serializer):
    competences = CompetenceSerializer(many=True)
    disciplines = DisciplineSerializer(many=True)

class MatrixDataSerializer(serializers.Serializer):
    matrix = CompetenceMatrixSerializer(many=True)

class SchemaDataSerializer(serializers.Serializer):
    schema = CompetenceSchemaSerializer(many=True)

class PassportDataSerializer(serializers.Serializer):
    passport = CompetencePassportSerializer(many=True)

class UpdateDisciplineCompetencesSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    discipline_id = serializers.IntegerField()
    selected_competences = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_blank=True, allow_null=True)
        )
    )

class SchemeUpdateSerializer(serializers.Serializer):
    """Serializer для обновления схемы"""
    plan_id = serializers.IntegerField(required=True)
    discipline_id = serializers.IntegerField(required=True)
    competence_index = serializers.CharField(required=True)
    competence = serializers.CharField(required=True)
    semester = serializers.IntegerField(required=True)
    forms = serializers.DictField(child=serializers.BooleanField(),required=True)

class FinalIndicatorUpdateSerializer(serializers.Serializer):
    """Serializer для обновления итогового индикатора"""
    plan_id = serializers.IntegerField(required=True)
    competence_index = serializers.CharField(required=True)
    final_indicator_text = serializers.CharField(required=True)
    indicator_id = serializers.IntegerField(required=False, allow_null=True)

class IndicatorDetailsSerializer(serializers.Serializer):
    """Serializer для деталей индикатора"""
    indicator_id = serializers.IntegerField(required=True)
    know = serializers.CharField(allow_blank=True, required=False)
    able = serializers.CharField(allow_blank=True, required=False)
    own = serializers.CharField(allow_blank=True, required=False)
    criteria = serializers.CharField(allow_blank=True, required=False)
    methods = serializers.CharField(allow_blank=True, required=False)

class UpdateIndicatorSerializer(serializers.Serializer):
    """Serializer для полного обновления индикатора"""
    indicator_id = serializers.IntegerField(required=True)
    discipline_id = serializers.IntegerField(required=False, allow_null=True)
    indicator_index = serializers.CharField(required=False, allow_null=True)
    indicator_content = serializers.CharField(required=False, allow_null=True)

class FullIndicatorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    indicator_index = serializers.CharField()
    indicator = serializers.CharField()
    competence_index = serializers.CharField()
    discipline_id = serializers.IntegerField()
    discipline_index = serializers.CharField()
    discipline_name = serializers.CharField()

class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinesIndicators
        fields = [
            'id',
            'planlineid',  
            'competence_index',
            'competence',
            'indicator_index',
            'indicator'
        ]

    def create(self, validated_data):
        from competence_passport.services.ruleService import RuleService
        
        indicator = LinesIndicators.objects.create(**validated_data)
        
        # Обновляем кэш дисциплины
        RuleService.update_discipline_kompetences(indicator.planlineid)
        
        return indicator

    def update(self, instance, validated_data):
        from competence_passport.services.ruleService import RuleService
        
        old_discipline = instance.planlineid
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем кэш старой и новой дисциплины
        RuleService.update_discipline_kompetences(old_discipline)
        if old_discipline != instance.planlineid:
            RuleService.update_discipline_kompetences(instance.planlineid)
            
        return instance

    def validate(self, data):
        planlineid = data.get('planlineid')
        competence_index = data.get('competence_index')
        indicator_index = data.get('indicator_index')
        
        if LinesIndicators.objects.filter(
            planlineid=planlineid,
            competence_index=competence_index,
            indicator_index=indicator_index
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Индикатор с таким индексом уже существует")
        
        return data

class FixSchemaSerializer(serializers.Serializer):
    """Serializer для исправления схемы индикаторов"""
    plan_id = serializers.IntegerField(required=True)
    discipline_id = serializers.IntegerField(required=True)
    competence_index = serializers.CharField(required=True)
    scheme_forms_count = serializers.IntegerField(required=True)
    indicators_count = serializers.IntegerField(required=True)
    semester = serializers.IntegerField(required=False, allow_null=True)