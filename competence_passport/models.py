from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.enums import TextChoices, IntegerChoices

from auths.models import UserProfile
from rpd.models import LinesData, LinesIndicators
from app.utils import TimestampsModel, OverwriteStorage

# Create your models here.
class Scheme(TimestampsModel):
    """Схема формирования компетенций дисциплинами по семестрам"""
    planlineid = models.ForeignKey(LinesData, on_delete=models.CASCADE, db_column="planlineid", related_name="competence_schemes")
    competence_index = models.TextField(null=True, blank=True)
    competence = models.TextField(null=True, blank=True)
    semester = models.IntegerField()
    ekz = models.BooleanField(null=True)
    zach = models.BooleanField(null=True)
    zacho = models.BooleanField(null=True)
    kp = models.BooleanField(null=True)
    kr = models.BooleanField(null=True)
    
    #indicator = models.OneToOneField(LinesIndicators, on_delete=models.SET_NULL, null=True, blank=True,)