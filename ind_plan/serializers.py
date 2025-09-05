from typing import Required

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User

from auths.serializer import UserSerializer
from ind_plan.models import Work, IndPlan, PlanWork, PreparingCoefficient, PlanWorkType
from ind_plan.services.indPlan_service import IndPlanService


class IndPlanListSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(source="user_created.userprofile")

    class Meta:
        model = IndPlan
        fields = ['id', 'year', 'user_created', 'user_confirmed', 'created_at', 'confirmed_at', 'status']

class PlanWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanWork
        fields = '__all__'

class IndPlanUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance

class PlanWorkAddUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    hours_count = serializers.FloatField(required=False)
    max_hours_count = serializers.FloatField(required=False)
    is_new = serializers.BooleanField(required=False)
    plan_id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        if 'is_new' in validated_data and validated_data['is_new'] != instance.is_new:
            if 'Подготовка к лекциям' in instance.name:
                hours_count = instance.max_hours_count / (PreparingCoefficient.old_lectures.value if validated_data['is_new'] else PreparingCoefficient.new_lectures.value)
                instance.hours_count = hours_count * (PreparingCoefficient.new_lectures.value if validated_data['is_new'] else PreparingCoefficient.old_lectures.value)
                instance.max_hours_count = instance.hours_count
                instance.is_new = validated_data['is_new']
            elif 'Подготовка к лабораторным, практическим, семинарским занятиям' in instance.name:
                hours_count = instance.max_hours_count / (PreparingCoefficient.old_labs_and_practices.value if validated_data['is_new'] else PreparingCoefficient.new_labs_and_practices.value)
                instance.hours_count = hours_count * (PreparingCoefficient.new_labs_and_practices.value if validated_data['is_new'] else PreparingCoefficient.old_labs_and_practices.value)
                instance.max_hours_count = instance.hours_count
                instance.is_new = validated_data['is_new']
        if 'hours_count' in validated_data and validated_data['hours_count'] != instance.hours_count:
            instance.hours_count = validated_data['hours_count']
        if 'name' in validated_data and validated_data['name'] != instance.name:
            instance.name = validated_data['name']

        instance.save()
        return instance

    def create(self, validated_data):
        plan_work = PlanWork.objects.create(
            name=validated_data['name'],
            type=validated_data['type'],
            plan=IndPlan.objects.get(id=validated_data['plan_id']),
        )

        if validated_data['type'] != PlanWorkType.work_with_students:
            plan_work.hours_count = validated_data['hours_count']
            plan_work.save()

        return plan_work

class IndPlanSerializer(serializers.Serializer):
    uch_nagr = serializers.ListField()
    preparing = PlanWorkSerializer(many=True, read_only=True)
    educ_method = PlanWorkSerializer(many=True, read_only=True)
    other_works = PlanWorkSerializer(many=True, read_only=True)
    work_with_students = PlanWorkSerializer(many=True, read_only=True)
    plan = IndPlanListSerializer(read_only=True)

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'type', 'hours_count']
        model = Work