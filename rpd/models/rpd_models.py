from django.contrib.auth.models import User
from django.db import models

from app.dictionaries import FILE_STATUS
from rpd.utils import TimestampsModel


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
    abbrprofile = models.CharField(max_length=12, verbose_name='', null=True, blank=True)
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
    gosdate = models.DateField(verbose_name='', null=True)
    lastshifr = models.CharField(max_length=64, verbose_name='')
    napr_e = models.CharField(max_length=1024, verbose_name='')
    napr_t = models.CharField(max_length=1024, verbose_name='')
    vuzname = models.CharField(max_length=256, verbose_name='')
    head = models.CharField(max_length=256, verbose_name='', null=True, blank=True)
    faculty = models.CharField(max_length=256, verbose_name='', null=True, blank=True)


class Disciplines(TimestampsModel):
    name = models.CharField(max_length=256, verbose_name='')


class LinesData(TimestampsModel):
    plan = models.ForeignKey(PlanData, verbose_name='', on_delete=models.PROTECT)
    disid = models.ForeignKey(Disciplines, verbose_name='', on_delete=models.PROTECT, db_column='disid')
    dis = models.CharField(max_length=256, verbose_name='')
    newdisid = models.CharField(max_length=128, verbose_name='', null=True, blank=True)
    mustbesdudied = models.IntegerField(verbose_name='', null=True)
    hoursinzet = models.IntegerField(verbose_name='', null=True)
    caf = models.IntegerField(verbose_name='', null=True)
    nocalccontrol = models.BooleanField(verbose_name='', null=True)
    type = models.IntegerField(verbose_name='', null=True)
    viewpract = models.IntegerField(verbose_name='', null=True)
    viewobject = models.IntegerField(verbose_name='', null=True)
    kompetences = models.CharField(max_length=1024, verbose_name='', null=True, blank=True)
    synchronize = models.BooleanField(verbose_name='', default=1)


class SemesterData(TimestampsModel):
    planlineid = models.ForeignKey(LinesData, verbose_name='', on_delete=models.PROTECT, db_column="planlineid")
    num = models.IntegerField(verbose_name='')
    lekc = models.IntegerField(verbose_name='', null=True)
    lab = models.IntegerField(verbose_name='', null=True)
    pr = models.IntegerField(verbose_name='', null=True)
    srs = models.IntegerField(verbose_name='', null=True)
    ekzhour = models.IntegerField(verbose_name='', null=True)
    zet = models.IntegerField(verbose_name='', null=True)
    ekz = models.BooleanField(verbose_name='', null=True)
    zach = models.BooleanField(verbose_name='', null=True)
    kp_hour = models.IntegerField(verbose_name='', null=True)
    kp = models.BooleanField(verbose_name='', null=True)
    kr_hour = models.IntegerField(verbose_name='', null=True)
    kr = models.BooleanField(verbose_name='', null=True)
    zacho = models.IntegerField(verbose_name='', null=True)
    eios = models.IntegerField(verbose_name='', null=True)


class LinesIndicators(TimestampsModel):
    planlineid = models.ForeignKey(LinesData, verbose_name='', on_delete=models.PROTECT, db_column="planlineid")
    competence_index = models.CharField(max_length=32, verbose_name='', null=True, blank=True)
    competence = models.CharField(max_length=2048, verbose_name='', null=True, blank=True)
    indicator_index = models.CharField(max_length=32, verbose_name='')
    indicator = models.CharField(max_length=2048, verbose_name='')


class PlanDocuments(TimestampsModel):
    plan = models.ForeignKey(PlanData, verbose_name='', on_delete=models.PROTECT)
    name = models.CharField(max_length=256, verbose_name='')
    type = models.IntegerField(verbose_name='')
    synchronize = models.BooleanField(verbose_name='')
    manual = models.BooleanField(verbose_name='', default=False)


class ExceptionNames(TimestampsModel):
    name = models.CharField(max_length=256, verbose_name='')

    def __str__(self):
        return f"{self.name}"


class AllowedNames(TimestampsModel):
    name = models.CharField(max_length=256, verbose_name='')

    def __str__(self):
        return f"{self.name}"


class BaseDocuments(TimestampsModel):
    name = models.CharField(max_length=64, verbose_name='Наименование файла')
    type = models.IntegerField(verbose_name='Тип')
    specialist = models.BooleanField(verbose_name='Специалитет')
    bachelor = models.BooleanField(verbose_name='Бакалавр')
    magistrate = models.BooleanField(verbose_name='Магистратура')
    spo = models.BooleanField(verbose_name='СПО')
    aspirant = models.BooleanField(verbose_name='Аспирантура')

    def __str__(self):
        return f"{self.name}"

