from django.contrib.auth.models import User
from django.db import models

from rpd.utils import TimestampsModel


# Create your models here.
class RPDFile(TimestampsModel):

    class StatusChoice(models.IntegerChoices):
        download = 0, "Загружен"
        in_review = 1, "На рассмотрении"
        accepted = 2, "Принят, ожидает синхронизации"
        on_synchronize = 3, "Принят, синхронизируется"
        finished = 4, "Принят, уже в АИС"

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT)
    title = models.TextField(verbose_name="Наименование файла")
    file = models.FileField(upload_to="uploads/rpd_plan/%Y-%m-%d/", verbose_name="Файл РПД")
    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.download)

    @property
    def status_verbose(self):
        return RPDFile.StatusChoice.labels[self.status]


class PlanData(TimestampsModel):
    file = models.ForeignKey(RPDFile, verbose_name="Файл", on_delete=models.CASCADE)
    subtype = models.TextField( verbose_name='')
    shifr = models.TextField(verbose_name='')
    abbrprofile = models.TextField(verbose_name='', null=True, blank=True)
    studyform = models.TextField(verbose_name='')
    studylevel = models.TextField( verbose_name='')
    studyprog = models.TextField( verbose_name='')
    elementsinweek = models.IntegerField(verbose_name='')
    species = models.TextField(verbose_name='')
    usernum = models.IntegerField(verbose_name='')
    whoratif = models.TextField(verbose_name='')
    planname = models.TextField(verbose_name='')
    kafcode = models.IntegerField(verbose_name='', null=True)
    startyear = models.IntegerField(verbose_name='')
    dviga = models.BooleanField(verbose_name='')
    gviga = models.BooleanField(verbose_name='')
    igazetweek = models.FloatField(verbose_name='', null=True)
    igahourzet = models.FloatField(verbose_name='', null=True)
    semesteroncource = models.IntegerField(verbose_name='')
    gosdate = models.DateField(verbose_name='', null=True)
    gostype = models.FloatField(verbose_name='', null=True)
    gosdocument = models.IntegerField(verbose_name='', null=True)
    lastshifr = models.TextField( verbose_name='')
    napr_e = models.TextField(verbose_name='')
    napr_t = models.TextField(verbose_name='')
    vuzname = models.TextField(verbose_name='')
    head = models.TextField(verbose_name='', null=True, blank=True)
    faculty = models.TextField(verbose_name='', null=True, blank=True)
    mira_id = models.IntegerField(verbose_name='', null=True, blank=True)

class Disciplines(TimestampsModel):
    name = models.TextField(verbose_name='')


class LinesData(TimestampsModel):
    plan = models.ForeignKey(PlanData, verbose_name='', on_delete=models.CASCADE, related_name="lines")
    disid = models.ForeignKey(Disciplines, verbose_name='', on_delete=models.CASCADE, db_column='disid')
    dis = models.TextField(verbose_name='')
    newdisid = models.TextField(verbose_name='', null=True, blank=True)
    mustbesdudied = models.IntegerField(verbose_name='', null=True)
    hoursinzet = models.IntegerField(verbose_name='', null=True)
    caf = models.IntegerField(verbose_name='', null=True)
    nocalccontrol = models.BooleanField(verbose_name='', null=True)
    type = models.IntegerField(verbose_name='', null=True)
    viewpract = models.IntegerField(verbose_name='', null=True)
    viewobject = models.IntegerField(verbose_name='', null=True)
    kompetences = models.TextField(verbose_name='', null=True, blank=True)
    synchronize = models.BooleanField(verbose_name='', default=1)


class SemesterData(TimestampsModel):
    planlineid = models.ForeignKey(LinesData, verbose_name='', on_delete=models.CASCADE, db_column="planlineid", related_name="semesters")
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
    planlineid = models.ForeignKey(LinesData, verbose_name='', on_delete=models.CASCADE, db_column="planlineid", related_name="indicators")
    competence_index = models.TextField(verbose_name='', null=True, blank=True)
    competence = models.TextField(verbose_name='', null=True, blank=True)
    indicator_index = models.TextField(verbose_name='')
    indicator = models.TextField(verbose_name='')


class PlanDocuments(TimestampsModel):
    plan = models.ForeignKey(PlanData, verbose_name='', on_delete=models.CASCADE)
    name = models.TextField(verbose_name='')
    type = models.IntegerField(verbose_name='')
    synchronize = models.BooleanField(verbose_name='')
    manual = models.BooleanField(verbose_name='', default=False)
    mira_id = models.IntegerField(verbose_name='', null=True, blank=True)


class ExceptionNames(TimestampsModel):
    name = models.TextField(verbose_name='')

    def __str__(self):
        return f"{self.name}"


class AllowedNames(TimestampsModel):
    name = models.TextField(verbose_name='')

    def __str__(self):
        return f"{self.name}"


class BaseDocuments(TimestampsModel):
    name = models.TextField( verbose_name='Наименование файла')
    type = models.IntegerField(verbose_name='Тип')
    specialist = models.BooleanField(verbose_name='Специалитет')
    bachelor = models.BooleanField(verbose_name='Бакалавр')
    magistrate = models.BooleanField(verbose_name='Магистратура')
    spo = models.BooleanField(verbose_name='СПО')
    aspirant = models.BooleanField(verbose_name='Аспирантура')

    def __str__(self):
        return f"{self.name}"

