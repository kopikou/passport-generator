from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import SET_NULL
from django.utils.html import format_html

from app.utils import TimestampsModel


class MiraAdmissionKinds(models.IntegerChoices):
    BACH = 2, 'ООП бакалавриата'
    SPEC = 1, 'ООП специалитета'
    MAG = 3, 'ООП магистратуры'


class AdmissionKinds(models.IntegerChoices):
    BACH_SPEC = 0, 'ООП бакалавриата, специалитета'
    MAG = 1, 'ООП магистратуры'
    NEW_BACH_SPEC = 2, 'Новые ООП бакалавриата, специалитета'
    NEW_MAG = 3, 'Новые ООП магистратуры'


class Indicators(models.IntegerChoices):
    EGE = 4, 'Средний балл ЕГЭ (ЕГЭ и ДВИ) обучающихся, зачисленных на ООП'
    STUD_CONTINGENT = 5,'	Доля обучающихся, успешно завершивших обучение / Доля сохранения контингента обучающихся'
    CELEV_STUD_CONTINGENT = 6, 'Доля обучающихся по договорам о целевом обучении, успешно завершивших обучение / Доля сохранения контингента обучающихся по договорам о целевом обучении'
    NPR = 7, 'Доля НПР ООП, принявших участие в опросах о качестве образования'
    STUD_SOP = 8, 'Доля обучающихся по ООП, принявших участие в опросах о качестве образования'
    EMPLOYER = 9, 'Участие работодателей в опросах о качестве подготовки выпускников'


class RopMonitoring(TimestampsModel):
    name = models.TextField(verbose_name="Название мониторинга")
    year = models.IntegerField(verbose_name="Год")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мониторинг'
        verbose_name_plural = "Мониторинги"

class Indicator(TimestampsModel):
    name = models.TextField(verbose_name="Название показателя")
    description = models.TextField(verbose_name="Описание показателя", blank=True, null=True)
    admission_kinds = ArrayField(
        base_field=models.IntegerField(choices=AdmissionKinds.choices),
        verbose_name='Типы ООП',
        default=list,
        blank=True,
    )

    def get_admission_kinds_display(self):
        return format_html("<br>".join([f"<{AdmissionKinds(kind_).label}>" for kind_ in self.admission_kinds]))

    get_admission_kinds_display.short_description = "Типы ООП"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Показатель'
        verbose_name_plural = "Показатели"


class RopMonitoringScore(TimestampsModel):
    rop_monitoring = models.ForeignKey("RopMonitoring", on_delete=SET_NULL, verbose_name="Мониторинг", null=True)
    admission = models.IntegerField(verbose_name="Программа", null=True)
    person = models.IntegerField(verbose_name="РОП", null=True)
    admission_name = models.TextField(verbose_name="Название ООП", null=True, blank=True)
    person_name = models.TextField(verbose_name="ФИО РОПа", null=True, blank=True)
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
        return f"<{self.rop_monitoring}> ({self.person_name}) {self.indicator} -> {self.score}"

    class Meta:
        verbose_name = 'Балл РОПа по мониторингу'
        verbose_name_plural = "Баллы РОПов по мониторингу"
