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
    plan_id = serializers.IntegerField(required=False)
    work_id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    count_required = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        #TODO
        instance.save()
        return instance

    def create(self, validated_data):
        plan_work = PlanWork.objects.create(
            name=validated_data['name'],
            type=validated_data['type'],
            plan=IndPlan.objects.get(id=validated_data['plan_id']),
            work=Work.objects.get(id=validated_data['work_id']) if 'work_id' in validated_data else None,
            count_required=validated_data['count_required'],
        )

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
        fields = ['name', 'type', 'is_multiple']
        model = Work