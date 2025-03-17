from django.contrib.auth.models import User
from django.db import models

from app.utils import TimestampsModel


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
    file = models.FileField(upload_to="rpd_plan/%Y-%m-%d/", verbose_name="Файл РПД")
    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.download)

    @property
    def status_verbose(self):
        return RPDFile.StatusChoice.labels[self.status]


class PlanData(TimestampsModel):
    file = models.ForeignKey(RPDFile, verbose_name="Файл", on_delete=models.CASCADE)
    subtype = models.TextField()
    shifr = models.TextField()
    abbrprofile = models.TextField(null=True, blank=True)
    studyform = models.TextField()
    studylevel = models.TextField()
    studyprog = models.TextField()
    elementsinweek = models.IntegerField()
    species = models.TextField()
    usernum = models.IntegerField()
    whoratif = models.TextField()
    planname = models.TextField()
    kafcode = models.IntegerField(null=True)
    startyear = models.IntegerField()
    dviga = models.BooleanField()
    gviga = models.BooleanField()
    igazetweek = models.FloatField(null=True)
    igahourzet = models.FloatField(null=True)
    semesteroncource = models.IntegerField()
    gosdate = models.DateField(null=True)
    gostype = models.FloatField(null=True)
    gosdocument = models.IntegerField(null=True)
    lastshifr = models.TextField()
    napr_e = models.TextField()
    napr_t = models.TextField()
    vuzname = models.TextField()
    head = models.TextField(null=True, blank=True)
    faculty = models.TextField(null=True, blank=True)
    mira_id = models.IntegerField(null=True, blank=True)

class Disciplines(TimestampsModel):
    name = models.TextField()


class LinesData(TimestampsModel):
    plan = models.ForeignKey(PlanData, on_delete=models.CASCADE, related_name="lines")
    disid = models.ForeignKey(Disciplines, on_delete=models.CASCADE, db_column='disid')
    dis = models.TextField()
    parent = models.ForeignKey("LinesData", on_delete=models.CASCADE, null=True)
    newdisid = models.TextField(null=True, blank=True)
    mustbesdudied = models.IntegerField(null=True)
    hoursinzet = models.IntegerField(null=True)
    caf = models.IntegerField(null=True)
    nocalccontrol = models.BooleanField(null=True)
    type = models.IntegerField(null=True)
    viewpract = models.IntegerField(null=True)
    viewobject = models.IntegerField(null=True)
    kompetences = models.TextField(null=True, blank=True)
    synchronize = models.BooleanField(default=1)


class SemesterData(TimestampsModel):
    planlineid = models.ForeignKey(LinesData, on_delete=models.CASCADE, db_column="planlineid", related_name="semesters")
    num = models.IntegerField()
    lekc = models.IntegerField(null=True)
    lab = models.IntegerField(null=True)
    pr = models.IntegerField(null=True)
    srs = models.IntegerField(null=True)
    ekzhour = models.IntegerField(null=True)
    zet = models.FloatField(null=True)
    ekz = models.BooleanField(null=True)
    zach = models.BooleanField(null=True)
    kp_hour = models.IntegerField(null=True)
    kp = models.BooleanField(null=True)
    kr_hour = models.IntegerField(null=True)
    kr = models.BooleanField(null=True)
    zacho = models.IntegerField(null=True)
    eios = models.IntegerField(null=True)


class LinesIndicators(TimestampsModel):
    planlineid = models.ForeignKey(LinesData, on_delete=models.CASCADE, db_column="planlineid", related_name="indicators")
    competence_index = models.TextField(null=True, blank=True)
    competence = models.TextField(null=True, blank=True)
    indicator_index = models.TextField()
    indicator = models.TextField()


class PlanDocuments(TimestampsModel):
    plan = models.ForeignKey(PlanData, on_delete=models.CASCADE, related_name="plan_documents")
    name = models.TextField()
    type = models.IntegerField()
    new_type = models.ForeignKey("DocumentsTypes", on_delete=models.CASCADE, default=None, null=True)
    synchronize = models.BooleanField(default=True)
    manual = models.BooleanField(default=False)
    mira_id = models.IntegerField(null=True, blank=True)

    @property
    def new_type_verbose(self):
        return DocumentsTypes.objects.get(id=self.new_type).name


class DocumentsTypes(TimestampsModel):
    name = models.TextField()


class ExceptionNames(TimestampsModel):
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"


class AllowedNames(TimestampsModel):
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"


class BaseDocuments(TimestampsModel):
    name = models.TextField(verbose_name='Наименование файла')
    type = models.IntegerField(verbose_name='Тип')
    new_type = models.ForeignKey("DocumentsTypes", on_delete=models.CASCADE, default=None, null=True)
    specialist = models.BooleanField(verbose_name='Специалитет')
    bachelor = models.BooleanField(verbose_name='Бакалавр')
    magistrate = models.BooleanField(verbose_name='Магистратура')
    spo = models.BooleanField(verbose_name='СПО')
    aspirant = models.BooleanField(verbose_name='Аспирантура')

    def __str__(self):
        return f"{self.name}"
