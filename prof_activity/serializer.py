import os

from rest_framework import serializers

from prof_activity.models import Areas2PlanProfActivity, Type2PlanProfActivity


class Areas2PlanProfActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas2PlanProfActivity
        fields = [
            'area',
            'plan_mira_id',
            'user_mira_id',
        ]
    def create(self, validate_data):
        area2plan, create = Areas2PlanProfActivity.objects.update_or_create(
            area=validate_data.get("area"),
            plan_mira_id=validate_data.get("plan_mira_id"),
            user_mira_id=validate_data.get("user_mira_id"),
        )

        return area2plan

class Type2PlanProfActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Type2PlanProfActivity
        fields = [
            'type',
            'plan_mira_id',
            'user_mira_id',
        ]
    def create(self, validate_data):
        type2plan, create = Type2PlanProfActivity.objects.update_or_create(
            type=validate_data.get("type"),
            plan_mira_id=validate_data.get("plan_mira_id"),
            user_mira_id=validate_data.get("user_mira_id"),
        )

        return type2plan
