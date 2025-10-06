from typing import Required

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User

from auths.serializer import UserSerializer
from ind_plan.models import Work, IndPlan, PlanWork, PlanWorkType


class IndPlanListSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(source="user_created.userprofile")

    class Meta:
        model = IndPlan
        fields = ['id', 'user_created', 'user_confirmed', 'created_at', 'confirmed_at', 'status', 'zav', 'year']

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'type', 'is_multiple']
        model = Work

class PlanWorkSerializer(serializers.ModelSerializer):
    work = WorkSerializer(read_only=True)

    class Meta:
        model = PlanWork
        fields = ['id', 'name', 'type', 'work', 'count_required', 'is_done', 'count_done']

class IndPlanUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance

class PlanWorkAddUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    plan_id = serializers.IntegerField(required=False)
    work_id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    count_required = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        if 'count_required' in validated_data:
            instance.count_required = validated_data['count_required']
        instance.save()
        return instance

    def create(self, validated_data):
        plan_work = PlanWork.objects.create(
            name=validated_data['name'] if 'name' in validated_data else None,
            type=validated_data['type']  if 'type' in validated_data else None,
            plan=IndPlan.objects.get(id=validated_data['plan_id']),
            work=Work.objects.get(pk=validated_data['work_id']) if 'work_id' in validated_data else None,
            count_required=validated_data['count_required'] if 'count_required' in validated_data else None,
        )

        return plan_work

class IndPlanSerializer(serializers.Serializer):
    plan = IndPlanListSerializer(read_only=True)
    works = PlanWorkSerializer(many=True, read_only=True)