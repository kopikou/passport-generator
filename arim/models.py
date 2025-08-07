from django.db import models, connections
from django.db.models import TextChoices

from app.utils import TimestampsModel


# Create your models here.
class BoolChoice(TextChoices):
    t = 't', "True"
    f = 'f', "False"

class CatPerson(models.Model):
    class Meta:
        db_table = "catperson"
        managed = False

    name = models.CharField(max_length=128)
    ckaf = models.ForeignKey("CatKaf", on_delete=models.CASCADE, db_column="ckaf")
    prepod = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)


class Catadmission(models.Model):
    class Meta:
        db_table = "catadmission"
        managed = False

    yr = models.IntegerField()
    abbr = models.CharField(max_length=10)
    cuchplan = models.ForeignKey("UchPlanPlan", on_delete=models.CASCADE, null=True, blank=True, db_column="cuchplan")
    cdirection = models.ForeignKey("CLDirection", on_delete=models.CASCADE, null=True, blank=True, db_column="cdirection")
    cspec = models.ForeignKey("CLSpec", on_delete=models.CASCADE, null=True, blank=True, db_column="cspec", related_name="clspec_cspec")
    cprofili = models.ForeignKey("CLSpec", on_delete=models.CASCADE, null=True, blank=True, db_column="cprofili", related_name="clspec_cprofili")
    spec_name = models.CharField(max_length=250, null=True, blank=True)
    direct_name = models.CharField(max_length=150, null=True, blank=True)
    active = models.CharField(max_length=1, choices=BoolChoice)
    onsite = models.CharField(max_length=1, choices=BoolChoice)
    cfac = models.ForeignKey("CatFaculty", null=True, on_delete=models.CASCADE, db_column="cfac")
    ckaf = models.ForeignKey("CatKaf", null=True,  on_delete=models.CASCADE, db_column="ckaf")
    kvalif_name = models.CharField(max_length=100)
    cadmkind = models.ForeignKey("CLAdmKind", null=True,  on_delete=models.CASCADE, db_column="cadmkind")
    cfob = models.ForeignKey("CLFob", null=True, on_delete=models.CASCADE, db_column="cfob")
    name = models.CharField(max_length=10)


class CLFob(models.Model):
    class Meta:
        db_table = "cl$fob"
        managed = False

    name = models.CharField(max_length=32)


class CLDirection(models.Model):
    class Meta:
        db_table = "cl$direction"
        managed = False

    name = models.CharField(max_length=150)
    cod = models.CharField(max_length=8)


class CLSpec(models.Model):
    class Meta:
        db_table = "cl$spec"
        managed = False

    name = models.CharField(max_length=250)
    code = models.CharField(max_length=8)
    cprepod = models.IntegerField()


class CLAdmKind(models.Model):
    class Meta:
        db_table = "cl$admkind"
        managed = False

    name = models.CharField(max_length=50)
    name_prof = models.CharField(max_length=50)
    name_ak = models.CharField(max_length=50)


class CatDepartment(models.Model):
    class Meta:
        db_table = "catdep"
        managed = False

    nameshort = models.CharField(max_length=512)
    name = models.CharField(max_length=512)



class CatKaf(models.Model):
    class Meta:
        db_table = "catkaf"
        managed = False

    name = models.CharField(max_length=128)
    zav = models.CharField(max_length=50)
    cfac = models.ForeignKey("CatFaculty", on_delete=models.CASCADE, db_column="cfac")
    ccatdep = models.ForeignKey("CatDepartment", on_delete=models.CASCADE, db_column="ccatdep")
    czav = models.IntegerField()



class CatFaculty(models.Model):
    class Meta:
        db_table = "catfaculty"
        managed = False

    name = models.CharField(max_length=64)
    dean = models.CharField(max_length=128)
    cdean = models.IntegerField()


class UchPlanKaf(models.Model):
    class Meta:
        db_table = "uchplan_kaf"
        managed = False

    ckaf2istu = models.IntegerField()
    ckaf2rpgen = models.IntegerField()
    name2rpgen = models.CharField(max_length=250)
    ckaf2asp = models.IntegerField(null=True, blank=True)


class UchPlanPlan(models.Model):
    class Meta:
        db_table = 'uchplan_plan'
        managed = False

    species = models.CharField(max_length=4096, null=True, blank=True)
    studyprog = models.CharField(max_length=64, null=True, blank=True)
    studyform = models.CharField(max_length=16, null=True, blank=True)
    fullplanname = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    kafcode = models.ForeignKey("UchPlanKaf", on_delete=models.CASCADE, null=True, blank=True, db_column="kafcode")
    ckaf = models.IntegerField(null=True, blank=True)
    lastshifr = models.CharField(max_length=64, null=True, blank=True)
    abbrprofile = models.CharField(max_length=16, null=True, blank=True)
    startyear = models.IntegerField(null=True, blank=True)
    gosdate = models.CharField(max_length=16, null=True, blank=True)
    gosdocument = models.IntegerField(null=True, blank=True)
    gostype = models.FloatField(null=True, blank=True)
    additiondate = models.CharField(max_length=16, null=True, blank=True)
    cadmission = models.ForeignKey("Catadmission", null=True, blank=True, on_delete=models.CASCADE, db_column="cadmission")
    fordel = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)
    cperson = models.IntegerField(null=True, blank=True)
    cobrazstandart = models.IntegerField(null=True, blank=True)
    moved = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)
    guid = models.CharField(max_length=64, null=True, blank=True)


class UchPlanDiscpl(models.Model):
    class Meta:
        db_table = 'uchplan_discpl'
        managed = False

    name = models.CharField(max_length=256)


class UchPlanLines(models.Model):
    class Meta:
        db_table = "uchplan_lines"
        managed = False

    planid = models.ForeignKey("UchPlanPlan", on_delete=models.CASCADE, db_column="planid")
    disid = models.ForeignKey("UchPlanDiscpl", on_delete=models.CASCADE, db_column="disid")
    cperson = models.IntegerField(null=True, blank=True)
    newdisid = models.CharField(max_length=32, null=True, blank=True)
    iddis = models.CharField(max_length=32, null=True, blank=True)
    kompetences = models.CharField(max_length=2048, null=True, blank=True)
    mustbesdudied = models.IntegerField(null=True, blank=True)
    hoursinzet = models.IntegerField(null=True, blank=True)
    kafcode = models.ForeignKey("UchPlanKaf", on_delete=models.CASCADE, null=True, blank=True, db_column="kafcode")
    ckaf = models.IntegerField(null=True, blank=True)
    nocalccontrol = models.IntegerField(null=True, blank=True)
    fordel = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)
    type = models.IntegerField(null=True, blank=True)
    viewobject = models.IntegerField(null=True, blank=True)
    viewpract = models.IntegerField(null=True, blank=True)


class UchPlanSemestr(models.Model):
    class Meta:
        db_table = "uchplan_semestr"
        managed = False

    planlineid = models.ForeignKey("UchPlanLines", on_delete=models.CASCADE, db_column="planlineid")
    num = models.IntegerField()
    lekc = models.IntegerField(null=True, blank=True)
    lab = models.IntegerField(null=True, blank=True)
    pr = models.IntegerField(null=True, blank=True)
    srs = models.IntegerField(null=True, blank=True)
    ekzhour = models.IntegerField(null=True, blank=True)
    zet = models.IntegerField(null=True, blank=True)
    ekz = models.CharField(max_length=1, choices=BoolChoice, null=True, blank=True)
    zach = models.CharField(max_length=1, choices=BoolChoice, null=True, blank=True)
    kp = models.CharField(max_length=1, choices=BoolChoice, null=True, blank=True)
    kp_hour = models.IntegerField()
    kr = models.CharField(max_length=1, choices=BoolChoice, null=True, blank=True)
    kr_hour = models.IntegerField()
    zacho = models.IntegerField()
    eios = models.IntegerField()


class UchPlanFiles(models.Model):
    class Meta:
        db_table = "uchplan_files"
        managed = False

    cplan = models.ForeignKey("UchPlanPlan", db_column="cplan", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    ctype = models.IntegerField()
    fordel = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)


class UistLicense(models.Model):
    class Meta:
        db_table = "uistlicense"
        managed = False

    cnt = models.IntegerField()
    clicense = models.ForeignKey("ClLicense", db_column="clicense", on_delete=models.CASCADE)


class ClLicense(models.Model):
    class Meta:
        db_table = "cl$license"
        managed = False

    name = models.CharField(max_length=128)


class OborudData(models.Model):
    class Meta:
        db_table = "oborud_data"
        managed = False

    name = models.CharField(max_length=250)
    inv = models.CharField(max_length=12, null=True, blank=True)
    caud = models.ForeignKey("CatAud", db_column="caud", on_delete=models.CASCADE, null=True)
    ismobile = models.CharField(max_length=1, choices=BoolChoice)


class CatAud(models.Model):
    class Meta:
        db_table = "cataud"
        managed = False

    name = models.CharField(max_length=16, null=True, blank=True)
    ckaf = models.IntegerField(null=True)
    cnazn = models.IntegerField(null=True)


class RpdUsers(models.Model):
    class Meta:
        db_table = "rpdusers"
        managed = False

    name = models.CharField(max_length=50)
    cperson = models.ForeignKey("CatPerson", on_delete=models.CASCADE, db_column="cperson")
    isadmin = models.CharField(max_length=1, choices=BoolChoice)
    isspo = models.CharField(max_length=1, choices=BoolChoice)
    cfac = models.ForeignKey("CatFaculty", on_delete=models.CASCADE, db_column="cfac")
    isspoadm = models.CharField(max_length=1, choices=BoolChoice)
    can_upload = models.CharField(max_length=1, choices=BoolChoice)

class UchNagr(models.Model):
    name = models.CharField(max_length=50)
    cperson = models.ForeignKey("CatPerson", on_delete=models.CASCADE, db_column="cperson")
    discpl = models.CharField(max_length=1000)
    grup = models.CharField(max_length=10)
    hour = models.IntegerField()
    sem = models.IntegerField()
    metka = models.CharField(max_length=10)
    direction = models.CharField(max_length=50)
    realhour = models.FloatField()
    doljnost = models.CharField(max_length=50)
    done = models.BooleanField()
    ddat = models.DateTimeField()

    class Meta:
        db_table = "person2uchnagr"
        managed = False

