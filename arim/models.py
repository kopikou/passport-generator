from django.db import models
from django.db.models import TextChoices


# Create your models here.

class BoolChoice(TextChoices):
    t = 't', "True"
    f = 'f', "False"


class UchPlanPlan(models.Model):

    species = models.CharField(max_length=4096, null=True, blank=True)
    studyprog = models.CharField(max_length=64, null=True, blank=True)
    studyform = models.CharField(max_length=16, null=True, blank=True)
    fullplanname = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    kafcode = models.CharField(max_length=256, null=True, blank=True)
    ckaf = models.IntegerField(null=True, blank=True)
    lastshifr = models.CharField(max_length=64, null=True, blank=True)
    abbrprofile = models.CharField(max_length=16, null=True, blank=True)
    startyear = models.IntegerField(null=True, blank=True)
    gosdate = models.CharField(max_length=16, null=True, blank=True)
    gosdocument = models.IntegerField(null=True, blank=True)
    gostype = models.FloatField(null=True, blank=True)
    additiondate = models.CharField(max_length=16, null=True, blank=True)
    cadmission = models.IntegerField(null=True, blank=True)
    fordel = models.CharField(max_length=1, choices=BoolChoice, default=BoolChoice.f)
    cperson = models.IntegerField(null=True, blank=True)
    cobrazstandart = models.IntegerField(null=True, blank=True)
    moved = models.CharField(max_length=1, choices=BoolChoice)
    guid = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'uchplan_plan'
        managed = False
