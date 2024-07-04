from django.contrib.auth.models import User
from django.db import models

from rpd.utils import TimestampsModel


# Create your models here.
class UserProfile(TimestampsModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bitrix_user_id = models.IntegerField(null=True, blank=True)
    mira_id = models.IntegerField(null=True, blank=True)

    is_student = models.BooleanField("Является студентом", default=True)
    is_teacher = models.BooleanField("Является преподавателем", default=False)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = "Профили пользователей"

