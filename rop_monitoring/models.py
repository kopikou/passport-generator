from django.db import models
from django.db.models import SET_NULL
from app.utils import TimestampsModel


class RopMonitoring(TimestampsModel):
    name = models.TextField(verbose_name="Название мониторинга")


class Indicator(TimestampsModel):
    name = models.TextField(verbose_name="Название показателя")


class RopMonitoringScore(TimestampsModel):
    rop_monitoring = models.ForeignKey("RopMonitoring", on_delete=SET_NULL, verbose_name="Мониторинг", null=True)
    admission = models.IntegerField(verbose_name="Программа")
    person = models.IntegerField(verbose_name="РОП")
    indicator = models.ForeignKey("Indicator", verbose_name="Индикатор", on_delete=SET_NULL, null=True)
    score = models.FloatField(verbose_name="Кол-во баллов")
