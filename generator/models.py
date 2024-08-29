from django.db import models

from rpd.models import LinesData, LinesIndicators
from rpd.utils import TimestampsModel

from django.contrib.postgres.fields import ArrayField

# Create your models here.
class PlanLinesLink(TimestampsModel):
    class StatusChoices(models.IntegerChoices):
        appointed = 0, "Назначен"
        is_filled = 1, "Заполняется"
        on_review = 2, "Отправлен на проверку"
        accepted = 3, "Подтвержден"
        on_refile = 4, "Требуются правки"

    cadmission = models.IntegerField(verbose_name='')
    planlines = models.ForeignKey(LinesData, on_delete=models.CASCADE, verbose_name='')
    mira_id = models.IntegerField(verbose_name='')
    person = models.IntegerField(verbose_name='')
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.appointed)
    precedence_discipline = ArrayField(models.IntegerField(verbose_name=''), default=list, null=True, blank=True)
    subsequent_discipline = ArrayField(models.IntegerField(verbose_name=''), default=list, null=True, blank=True)
    library = ArrayField(models.IntegerField(verbose_name=''), default=list, null=True, blank=True)
    software = ArrayField(models.IntegerField(verbose_name=''), default=list, null=True, blank=True)
    logistics = ArrayField(models.IntegerField(verbose_name=''), default=list, null=True, blank=True)

    @property
    def status_verbose(self):
        return PlanLinesLink.StatusChoices.labels[self.status]


class FormControl(TimestampsModel):
    name = models.CharField(max_length=64)


class IndependentTypes(TimestampsModel):
    name = models.CharField(max_length=128)


class DisciplineIndicators(TimestampsModel):
    indicator = models.ForeignKey(LinesIndicators, on_delete=models.CASCADE, related_name="discipline_indicator")
    planlineid = models.ForeignKey(LinesData, on_delete=models.CASCADE)
    know = models.TextField(null=True, blank=True)
    able = models.TextField(null=True, blank=True)
    own = models.TextField(null=True, blank=True)
    criteria = models.TextField(null=True, blank=True)
    methods = models.TextField(null=True, blank=True)


class DisciplineThemes(TimestampsModel):
    planlineslink = models.ForeignKey("PlanLinesLink", on_delete=models.CASCADE, related_name="discipline_themes")
    name = models.TextField()
    semester = models.IntegerField()
    formcontrol = models.ForeignKey("FormControl", on_delete=models.CASCADE)
    comment = models.TextField()


class DisciplineWorkHours(TimestampsModel):

    class TypeChoices(models.IntegerChoices):
        lectures = 0, "Лекции"
        practice = 1, "Практики"
        independent = 2, "Самостоятельные"
        laboratory = 3, "Лабораторные"


    planlineslink = models.ForeignKey("PlanLinesLink", on_delete=models.CASCADE, related_name="discipline_work_hour")
    theme = models.ForeignKey("DisciplineThemes", on_delete=models.CASCADE)
    type = models.IntegerField(choices=TypeChoices.choices)
    name = models.TextField()
    hours = models.FloatField()
    semester = models.IntegerField()

    @property
    def type_verbose(self):
        return DisciplineWorkHours.TypeChoices.labels[self.type]
