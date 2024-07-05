from django.contrib.auth.models import User
from django.db import models
from rpd.utils import TimestampsModel

from app.dictionaries import FILE_STATUS


# Create your models here.
class RPDFile(TimestampsModel):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT)
    title = models.CharField(max_length=100, verbose_name="Наименование файла")
    file = models.FileField(upload_to="uploads/rpd_plan/%Y-%m-%d/", verbose_name="Файл РПД")
    status = models.IntegerField(choices=FILE_STATUS, default=FILE_STATUS[0])


class Competence(models.Model):
    code = models.IntegerField()
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_competences"
        managed = False
