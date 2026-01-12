from rest_framework import serializers
from competence_passport.models import Scheme, CompetenceRelations


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'


class CompetenceRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetenceRelations
        fields = '__all__'


class UpdateDisciplineCompetencesSerializer(serializers.Serializer):
    """Сериализатор для обновления компетенций дисциплины"""
    plan_id = serializers.CharField(required=True)
    discipline_id = serializers.IntegerField(required=True)
    selected_competences = serializers.ListField(
        child=serializers.DictField(), required=True
    )


class SchemeUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления схемы"""
    plan_id = serializers.CharField(required=True)
    discipline_id = serializers.IntegerField(required=True)
    competence_index = serializers.CharField(required=True)
    semester = serializers.IntegerField(required=True)
    forms = serializers.DictField(required=True)


class CompetenceRelationsUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления связей компетенций"""
    plan_id = serializers.CharField(required=True)
    competence_index = serializers.CharField(required=True)
    relations_text = serializers.CharField(allow_blank=True, required=True)


class FinalIndicatorUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления итогового индикатора"""
    plan_id = serializers.CharField(required=True)
    competence_index = serializers.CharField(required=True)
    final_indicator_text = serializers.CharField(required=True)
    indicator_id = serializers.IntegerField(required=False, allow_null=True)

class UpdateIndicatorContentSerializer(serializers.Serializer):
    """Сериализатор для обновления содержания индикатора"""
    indicator_id = serializers.IntegerField(required=True)
    indicator_content = serializers.CharField(required=True)


class IndicatorDetailsSerializer(serializers.Serializer):
    """Сериализатор для деталей индикатора (знать/уметь/владеть)"""
    indicator_id = serializers.IntegerField(required=True)
    know = serializers.CharField(allow_blank=True, required=False)
    able = serializers.CharField(allow_blank=True, required=False)
    own = serializers.CharField(allow_blank=True, required=False)
    criteria = serializers.CharField(allow_blank=True, required=False)
    methods = serializers.CharField(allow_blank=True, required=False)


class FixSchemeRequestSerializer(serializers.Serializer):
    """Сериализатор для исправления схемы индикаторов"""
    plan_id = serializers.CharField(required=True)
    discipline_id = serializers.IntegerField(required=True)
    competence_index = serializers.CharField(required=True)
    scheme_forms_count = serializers.IntegerField(required=True)
    indicators_count = serializers.IntegerField(required=True)
    semester = serializers.IntegerField(required=False, allow_null=True)