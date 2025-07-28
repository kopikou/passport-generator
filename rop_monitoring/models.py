from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import SET_NULL
from django.utils.html import format_html

from app.utils import TimestampsModel


class AdmissionTypes(models.IntegerChoices):
    BACH_SPEC = 0, 'ООП бакалавриата, специалитета'
    MAG = 1, 'ООП магистратуры'
    NEW_BACH_SPEC = 2, 'Новые ООП бакалавриата, специалитета'
    NEW_MAG = 3, 'Новые ООП магистратуры'


class RopMonitoring(TimestampsModel):
    name = models.TextField(verbose_name="Название мониторинга")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мониторинг'
        verbose_name_plural = "Мониторинги"

class Indicator(TimestampsModel):
    name = models.TextField(verbose_name="Название показателя")
    description = models.TextField(verbose_name="Описание показателя", blank=True, null=True)
    types = ArrayField(
        base_field=models.IntegerField(choices=AdmissionTypes.choices),
        verbose_name='Типы ООП',
        default=list,
        blank=True,
    )

    def get_types_display(self):
        return format_html("<br>".join([f"<{AdmissionTypes(type_).label}>" for type_ in self.types]))

    get_types_display.short_description = "Типы ООП"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Показатель'
        verbose_name_plural = "Показатели"


class RopMonitoringScore(TimestampsModel):
    rop_monitoring = models.ForeignKey("RopMonitoring", on_delete=SET_NULL, verbose_name="Мониторинг", null=True)
    admission = models.IntegerField(verbose_name="Программа")
    person = models.IntegerField(verbose_name="РОП")
    indicator = models.ForeignKey("Indicator", verbose_name="Индикатор", on_delete=SET_NULL, null=True)
    value_numeric = models.FloatField(verbose_name="Значение показателя (численное)", null=True)
    value_boolean = models.BooleanField(verbose_name="Значение показателя (булевое)", null=True)
    score = models.FloatField(verbose_name="Кол-во баллов", null=True)

    @property
    def value(self):
        if self.value_boolean is not None:
            return self.value_boolean
        return self.value_numeric

    def __str__(self):
        return f"<{self.rop_monitoring}> ({self.person}) {self.indicator} -> {self.score}"

    class Meta:
        verbose_name = 'Балл РОПа по мониторингу'
        verbose_name_plural = "Баллы РОПов по мониторингу"
