from rest_framework import serializers

from arim.services import AISServices
from auths.serializer import UserSerializer
from ind_plan.models import Work, IndPlan, PlanWork, PlanWorkType, PlanComment


class IndPlanListSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(source="user_created.userprofile")
    comment = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    class Meta:
        model = IndPlan
        fields = ['id', 'user_created', 'user_confirmed', 'created_at', 'confirmed_at', 'status', 'zav', 'year', 'comment', 'additional_info']

    def get_comment(self, obj):
        plan_comment = PlanComment.objects.filter(plan=obj).last()
        if plan_comment:
            return plan_comment.comment
        else:
            return None

    def get_additional_info(self, obj):
        data = AISServices.get_doljn_and_rate(obj.user_created.userprofile.mira_id)
        return {
            'doljn': data[0]['doljn'],
            'rate': data[0]['rate'],
        }

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
    comment = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()

        if 'comment' in validated_data:
            comment = PlanComment.objects.create(plan=instance, status=instance.status, comment=validated_data['comment'])
            return {
                'status': instance.status,
                'comment': comment.comment,
            }
        else:
            return {
                'status': instance.status,
                'comment': '',
            }

class PlanWorkAddUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    plan_id = serializers.IntegerField(required=False)
    work_id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    count_required = serializers.IntegerField(required=False)
    work = WorkSerializer(read_only=True, required=False)

    def update(self, instance, validated_data):
        if 'count_required' in validated_data:
            instance.count_required = validated_data['count_required']
        instance.save()
        return instance

    def create(self, validated_data):
        plan_work = PlanWork.objects.create(
            name=validated_data['name'] if 'name' in validated_data else None,
            type=PlanWorkType.work_with_students if 'name' in validated_data else None,
            plan=IndPlan.objects.get(id=validated_data['plan_id']),
            work=Work.objects.get(pk=validated_data['work_id']) if 'work_id' in validated_data else None,
            count_required=validated_data['count_required'] if 'count_required' in validated_data else None,
        )

        return plan_work

class IndPlanSerializer(serializers.Serializer):
    plan = IndPlanListSerializer(read_only=True)
    works = PlanWorkSerializer(many=True, read_only=True)