from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class PlanWorkType(models.TextChoices):
    educ_method = 'Учебно-методическая работа', 'educ_method'
    preparing = 'Подготовка к учебным занятиям', 'preparing'
    scientific_research = 'Учебно-исследовательская работа', 'scientific_research'
    organization = 'Организационная работа', 'organization'
    upbringing = 'Работа по воспитанию обучающихся', 'upbringing'
    qualification = 'Повышение квалификации', 'qualification'
    work_with_students = 'Работа с обучающимися и абитуриентами', 'work_with_students'

class IndPlan(models.Model):
    year = models.IntegerField()
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_created")
    user_confirmed = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_confirmed")
    created_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

class Work(models.Model):
    name = models.TextField()
    type = models.TextField(choices=PlanWorkType.choices)
    hours_count = models.IntegerField()

class PlanWork(models.Model):
    plan = models.ForeignKey(IndPlan, on_delete=models.CASCADE, related_name="plan")
    name = models.TextField()
    type = models.TextField(choices=PlanWorkType.choices)
    hours_count = models.FloatField(null=True, blank=True)
    max_hours_count = models.FloatField(null=True, blank=True)
    is_new = models.BooleanField(null=True, blank=True)