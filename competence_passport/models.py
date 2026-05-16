from django.db import models

from rpd.models import LinesData, LinesIndicators, PlanData
from app.utils import TimestampsModel

# Create your models here.
class Competence(TimestampsModel):
    """Модель для хранения всех компетенций плана"""
    plan = models.ForeignKey(PlanData, on_delete=models.CASCADE, db_column="plan_id", related_name="competence")
    competence_index = models.TextField(null=True, blank=True)
    competence = models.TextField(null=True, blank=True)
    relations = models.TextField(null=True, blank=True)
    final_indicator = models.TextField(null=True, blank=True)    

class Scheme(TimestampsModel):
    """Схема формирования компетенций дисциплинами по семестрам"""
    planlineid = models.ForeignKey(LinesData, on_delete=models.CASCADE, db_column="planlineid", related_name="competence_schemes")
    #competence_index = models.TextField(null=True, blank=True)
    # competence = models.TextField(null=True, blank=True)
    competence_id = models.ForeignKey(Competence,null=True, blank=True, on_delete=models.CASCADE, db_column="competence_id", related_name="competence_schemes")
    semester = models.IntegerField()
    ekz = models.BooleanField(null=True)
    zach = models.BooleanField(null=True)
    zacho = models.BooleanField(null=True)
    kp = models.BooleanField(null=True)
    kr = models.BooleanField(null=True)

