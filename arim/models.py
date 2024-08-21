from django.db import models
from django.db.models import TextChoices
from mssql import features

from rpd.utils import TimestampsModel


# Create your models here.
class BoolChoice(TextChoices):
    t = 't', "True"
    f = 'f', "False"


class Catadmission(models.Model):
    class Meta:
        db_table = "catadmission"
        managed = False

    yr = models.IntegerField()
    abbr = models.CharField(max_length=10)
    cuchplan = models.ForeignKey("UchPlanPlan", on_delete=models.CASCADE, null=True, blank=True, db_column="cuchplan")


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


