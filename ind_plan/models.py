from datetime import datetime

from django.db import models

from django.contrib.auth.models import User
from app.utils import TimestampsModel


class PlanWorkType(models.TextChoices):
    scientific_research = 'Научно-исследовательская работа', 'scientific_research'
    organization = 'Организационно-методическая работа', 'organization'
    upbringing = 'Работа по воспитанию обучающихся', 'upbringing'
    qualification = 'Повышение квалификации', 'qualification'
    work_with_students = 'Работа с обучающимися и абитуриентами', 'work_with_students'
    educ_method = 'Учебно-методическая работа', 'educ_method'

class IndPlan(TimestampsModel):
    class IndPlanStatusChoice(models.IntegerChoices):
        created = 0, "Создан"
        waiting = 1, "Ожидает рассмотрения"
        accepted = 2, "Утвержден"
        on_refile = 3, "Требуются правки"

    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_created")
    user_accepted = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_accepted")
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=IndPlanStatusChoice.choices, default=IndPlanStatusChoice.created)
    zav = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="zav")
    year = models.IntegerField(null=True, blank=True)
    template = models.ForeignKey('IndPlanTemplate', on_delete=models.CASCADE, null=True)


class IndPlanTemplate(TimestampsModel):
    name = models.TextField()
    year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


class Work(TimestampsModel):
    template = models.ForeignKey(IndPlanTemplate, on_delete=models.CASCADE, null=True)
    name = models.TextField()
    type = models.TextField()
    order = models.IntegerField(default=0, db_default=0)
    # hours_count = models.IntegerField(null=True, blank=True)

class PlanWork(TimestampsModel):
    plan = models.ForeignKey(IndPlan, on_delete=models.CASCADE, related_name="plan")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="work",null=True, blank=True)
    is_done = models.BooleanField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)


class PlanComment(TimestampsModel):
    plan = models.ForeignKey(IndPlan, on_delete=models.CASCADE, related_name="ind_plan")
    comment = models.TextField()
    date = models.DateTimeField(null=True, blank=True, default=datetime.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author")

