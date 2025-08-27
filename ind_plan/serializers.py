from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User

from auths.serializer import UserSerializer
from ind_plan.models import Work, IndPlan, PlanWork


class IndPlanListSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(source="user_created.userprofile")

    class Meta:
        model = IndPlan
        fields = ['id', 'year', 'user_created', 'user_confirmed', 'created_at', 'confirmed_at']

class PlanWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanWork
        fields = ['id', 'name', 'hours_count', 'max_hours_count', 'is_new']

class IndPlanSerializer(serializers.Serializer):
    uch_nagr = serializers.ListField()
    preparing = serializers.ListField()
    educ_method = serializers.ListField()
    other_works = serializers.ListField()
    work_with_students = serializers.ListField()

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'type', 'hours_count']
        model = Work

class AddWorkSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    hours_count = serializers.IntegerField(required=False)