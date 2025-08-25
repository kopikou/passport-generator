from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import TextChoices
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.utils import TimestampsModel


class Permissions(TextChoices):
    can_upload_plx_files = "can_upload_plx_files", "Может загружать plx файлы"
    can_edit_rpd = "can_edit_rpd", "Может редактировать РПД"
    can_use_generator = "can_use_generator", "Может использовать генератор"
    can_upload_files = "can_upload_files", "Может загружать файлы Программы"
    scientific_admin = "scientific_admin", "Просмотр всех ПНД по программе аспирантуры"
    can_monitor_rops = "can_monitor_rops", "Может мониторить РОПов",


# Create your models here.
class UserProfile(TimestampsModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bitrix_user_id = models.IntegerField(null=True, blank=True)
    mira_id = models.IntegerField(null=True, blank=True)

    is_student = models.BooleanField("Является студентом", default=True)
    is_teacher = models.BooleanField("Является преподавателем", default=False)

    middle_name = models.CharField(max_length=256, null=True, blank=True)

    permissions = ArrayField(models.TextField(choices=Permissions.choices), default=list, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = "Профили пользователей"

    @property
    def fio(self):
        return f"{self.user.last_name} {self.user.first_name} {self.middle_name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except User.userprofile.RelatedObjectDoesNotExist as ex:
        UserProfile.objects.create(user=instance)
