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


class PlanData(TimestampsModel):
    file = models.ForeignKey(RPDFile, verbose_name="Файл", on_delete=models.PROTECT)
    subtype = models.CharField(max_length=64, verbose_name='')
    shifr = models.CharField(max_length=8, verbose_name='')
    studyform = models.CharField(max_length=48, verbose_name='')
    studylevel = models.CharField(max_length=64, verbose_name='')
    studyprog = models.CharField(max_length=64, verbose_name='')
    elementsinweek = models.IntegerField(verbose_name='')
    species = models.CharField(max_length=4096, verbose_name='')
    usernum = models.IntegerField(verbose_name='')
    whoratif = models.CharField(max_length=128, verbose_name='')
    planname = models.CharField(max_length=256, verbose_name='')
    kafcode = models.IntegerField(verbose_name='', null=True)
    startyear = models.IntegerField(verbose_name='')
    dviga = models.BooleanField(verbose_name='')
    gviga = models.BooleanField(verbose_name='')
    igazetweek = models.FloatField(verbose_name='', null=True)
    igahourzet = models.FloatField(verbose_name='', null=True)
    semesteroncource = models.IntegerField(verbose_name='')
    gosdate = models.DateField(verbose_name='')
    lastshifr = models.CharField(max_length=64, verbose_name='')
    napr_e = models.CharField(max_length=1024, verbose_name='')
    napr_t = models.CharField(max_length=1024, verbose_name='')
    vuzname = models.CharField(max_length=256, verbose_name='')
    head = models.CharField(max_length=256, verbose_name='', null=True, blank=True)
    faculty = models.CharField(max_length=256, verbose_name='', null=True, blank=True)


class Competence(models.Model):
    code = models.IntegerField()
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_competences"
        managed = False

