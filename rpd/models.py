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


class Competence(models.Model):
    code = models.IntegerField()
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_competences"
        managed = False


class Indikator(models.Model):
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_indikator"
        managed = False


class Discipline(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "mleha_dis"
        managed = False


class Plan(models.Model):
    species = models.CharField(max_length=4096)
    subtype = models.CharField(max_length=64)
    shifr = models.CharField(max_length=8)
    studyprog = models.CharField(max_length=64)
    studyform = models.CharField(max_length=48)
    studylevel = models.CharField(max_length=64)
    fullplanname = models.CharField(max_length=256)
    planname = models.CharField(max_length=256)
    usernum = models.IntegerField()
    vuzname = models.CharField(max_length=256)
    head = models.CharField(max_length=256)
    whoratif = models.CharField(max_length=128)
    kafcode = models.CharField(max_length=256)
    faculty = models.CharField(max_length=256)
    lastshifr = models.CharField(max_length=64)
    abbrprofile = models.CharField(max_length=32)
    startyear = models.IntegerField()
    ekinhoursum = models.BooleanField()
    dviga = models.IntegerField()
    gviga = models.IntegerField()
    detailgia = models.IntegerField()
    igazetweek = models.FloatField()
    igahourzet = models.FloatField()
    ksriz = models.CharField(max_length=16)
    oopet = models.IntegerField()
    lekc = models.FloatField()
    dvv = models.FloatField()
    maxnagr = models.FloatField()
    vidplan = models.IntegerField()
    levelcode = models.CharField(max_length=4)
    sokrcontrolfact = models.IntegerField()
    semesteroncource = models.IntegerField()
    elementsinweek = models.IntegerField()
    gosdate = models.DateField
    gosdocument = models.IntegerField()
    gostype = models.FloatField()
    addition = models.CharField(max_length=64)
    additiondate = models.DateField()
    additionversion = models.IntegerField()
    naprcode = models.CharField(max_length=64)
    napr_e = models.CharField(max_length=1024)
    napr_t = models.CharField(max_length=1024)

    class Meta:
        db_table = "mleha_plan"
        managed = False


class Planlines(models.Model):
    planid = models.ForeignKey(Plan, on_delete=models.PROTECT, null=False, db_constraint=False)
    dis = models.CharField(max_length=1024)
    disid = models.ForeignKey(Discipline, on_delete=models.PROTECT, null=False, db_constraint=False)
    newcycle = models.CharField(max_length=32)
    newdisid = models.CharField(max_length=32)
    cycle = models.CharField(max_length=32)
    iddis = models.CharField(max_length=32)
    gos = models.IntegerField()
    sr = models.IntegerField()
    kompetences = models.CharField(max_length=4096)
    mustbesdudied = models.IntegerField()
    creditstodis = models.IntegerField()
    hoursinzet = models.IntegerField()
    caf = models.IntegerField()
    razdel = models.IntegerField()
    nocalccontrol = models.IntegerField()
    hourinter = models.IntegerField()
    disforraz = models.BooleanField()
    dsforraz = models.BooleanField()
    is_del = models.BooleanField(db_column='del')
    block = models.IntegerField()
    maxvar = models.IntegerField()
    type = models.IntegerField()
    viewpract = models.IntegerField()
    viewobject = models.IntegerField()

    class Meta:
        db_table = "mleha_planlines"
        managed = False


class PlanCompetence(models.Model):
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    competenceid = models.ForeignKey(Competence, on_delete=models.PROTECT, null=False, db_constraint=False)

    class Meta:
        db_table = "mleha_plancompetence"
        managed = False


class PlanIndikator(models.Model):
    indikid = models.ForeignKey(Indikator, on_delete=models.PROTECT, null=False, db_constraint=False)
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    competenceid = models.ForeignKey(Competence, on_delete=models.PROTECT, null=False, db_constraint=False)
    znat = models.CharField(max_length=4000)
    umet = models.CharField(max_length=4000)
    vladet = models.CharField(max_length=4000)
    kriteriy_oceniv = models.CharField(max_length=4000)
    metod_oceniv = models.CharField(max_length=4000)

    class Meta:
        db_table = "mleha_planindikator"
        managed = False

class Semestr(models.Model):
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    num = models.IntegerField()
    lekc = models.IntegerField()
    lab = models.IntegerField()
    pr = models.IntegerField()
    srs = models.IntegerField()
    ekzhour = models.IntegerField()
    zet = models.FloatField()
    ekz = models.BooleanField()
    zach = models.BooleanField()
    intpr = models.IntegerField()
    intlek = models.IntegerField()
    intlab = models.IntegerField()
    kp = models.BooleanField()
    kr = models.BooleanField()
    proektprvned = models.FloatField()
    proektlekvned = models.FloatField()
    proektlabvned = models.FloatField()
    proektzet = models.FloatField()
    zacho = models.IntegerField()
    contr = models.IntegerField()
    contrrab = models.IntegerField()
    sessnum = models.IntegerField()
    ip = models.IntegerField()
    sure_hour = models.IntegerField()
    cons_hour = models.IntegerField()
    ip_hour = models.IntegerField()
    kp_hour = models.IntegerField()
    kr_hour = models.IntegerField()
    maxvar = models.IntegerField()
    seminar = models.IntegerField()
    spo_pr_hours = models.IntegerField()
    eios = models.IntegerField()
    pp = models.IntegerField()

    class Meta:
        db_table = "mleha_semestr"
        managed = False