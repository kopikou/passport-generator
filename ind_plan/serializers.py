from datetime import datetime

from rest_framework import serializers

from arim.services import AISServices
from auths.serializer import UserSerializer
from ind_plan.models import Work, IndPlan, PlanWork, PlanWorkType, PlanComment

class PlanCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source="author.userprofile", allow_null=True)

    class Meta:
        model = PlanComment
        fields = ['comment', 'author', 'date']

class IndPlanListSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(source="user_created.userprofile")
    comments = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    class Meta:
        model = IndPlan
        fields = ['id', 'user_created', 'user_accepted', 'created_at', 'accepted_at', 'status', 'zav', 'year', 'comments', 'additional_info']

    def get_additional_info(self, obj):
        data = AISServices.get_doljn_and_rate(obj.user_created.userprofile.mira_id)
        return {
            'doljn': data[0]['doljn'],
            'rate': data[0]['rate'],
        }

    def get_comments(self, obj):
        comments = PlanComment.objects.filter(plan=obj.id).all()
        return PlanCommentSerializer(comments, many=True).data

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'type']
        model = Work

class PlanWorkSerializer(serializers.ModelSerializer):
    work = WorkSerializer(read_only=True)

    class Meta:
        model = PlanWork
        fields = ['id', 'work', 'is_done', 'additional_info']

class IndPlanUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=False)
    comment = serializers.CharField(required=False)
    plan_comment = PlanCommentSerializer(required=False)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']

        if validated_data['status'] == IndPlan.IndPlanStatusChoice.accepted:
            instance.accepted_at = datetime.now()

        instance.save()

        if 'comment' in validated_data:
            comment = PlanComment.objects.create(plan=instance, comment=validated_data['comment'], author=self.context['request'].user)
            plan_comment = PlanCommentSerializer(comment).data
            return {
                'status': instance.status,
                'plan_comment': plan_comment,
            }
        else:
            return {
                'status': instance.status,
                'plan_comment': None,
            }

class PlanWorkAddUpdateSerializer(serializers.Serializer):
    # id = serializers.IntegerField(required=False)
    # name = serializers.CharField(required=False)
    plan_id = serializers.IntegerField(required=False)
    work_id = serializers.IntegerField(required=False)
    # type = serializers.CharField(required=False)
    # work = WorkSerializer(read_only=True, required=False)
    additional_info = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        if 'additional_info' in validated_data:
            instance.additional_info = validated_data['additional_info']
        instance.save()
        return instance

    def create(self, validated_data):
        plan_work = PlanWork.objects.create(
            plan_id=validated_data['plan_id'],
            work_id=validated_data['work_id'],
        )

        return plan_work

class IndPlanSerializer(serializers.Serializer):
    plan = IndPlanListSerializer(read_only=True)
    works = PlanWorkSerializer(many=True, read_only=True)