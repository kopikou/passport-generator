from django.contrib.auth.models import User
from django.db import models

from app.utils import TimestampsModel


class AreasProfActivity(TimestampsModel):
    title = models.TextField()


class TypeProfActivity(TimestampsModel):
    title = models.TextField()


class Areas2PlanProfActivity(TimestampsModel):
    area = models.ForeignKey(AreasProfActivity, on_delete=models.CASCADE)
    plan_mira_id = models.IntegerField()
    user_mira_id = models.IntegerField()


class Type2PlanProfActivity(TimestampsModel):
    type = models.ForeignKey(TypeProfActivity, on_delete=models.CASCADE)
    plan_mira_id = models.IntegerField()
    user_mira_id = models.IntegerField()
