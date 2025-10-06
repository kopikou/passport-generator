from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class PlanWorkType(models.TextChoices):
    scientific_research = 'Научно-исследовательская работа', 'scientific_research'
    organization = 'Организационно-методическая работа', 'organization'
    upbringing = 'Работа по воспитанию обучающихся', 'upbringing'
    qualification = 'Повышение квалификации', 'qualification'
    work_with_students = 'Работа с обучающимися и абитуриентами', 'work_with_students'
    educ_method = 'Учебно-методическая работа', 'educ_method'

class IndPlan(models.Model):
    class IndPlanStatusChoice(models.IntegerChoices):
        created = 0, "Создан"
        waiting = 1, "Ожидает рассмотрения"
        accepted = 2, "Утвержден"
        on_refile = 3, "Требуются правки"
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_created")
    user_confirmed = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_confirmed")
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=IndPlanStatusChoice.choices, default=IndPlanStatusChoice.created)
    zav = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="zav")
    year = models.IntegerField(null=True, blank=True)

class Work(models.Model):
    name = models.TextField()
    type = models.TextField(choices=PlanWorkType.choices)
    is_multiple = models.BooleanField(default=False)

class PlanWork(models.Model):
    plan = models.ForeignKey(IndPlan, on_delete=models.CASCADE, related_name="plan")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="work",null=True, blank=True)
    count_required = models.IntegerField(null=True, blank=True)
    is_done = models.BooleanField(null=True, blank=True)
    count_done = models.IntegerField(null=True, blank=True)
    type = models.TextField(choices=PlanWorkType.choices, null=True, blank=True)
    name = models.TextField(null=True, blank=True)

