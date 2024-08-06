from django.db import models

from rpd.models import LinesData
from rpd.utils import TimestampsModel


# Create your models here.
class PlanLinesLink(TimestampsModel):

    class StatusChoices(models.IntegerChoices):
        appointed = 1, "Назначен"
        is_filled = 2, "Заполняется"
        on_review = 3, "Отправлен на проверку"
        accepted = 4, "Подтвержден"
        on_refile = 5, "Требуются правки"

    cadmission = models.IntegerField(verbose_name='')
    planlines = models.ForeignKey(LinesData, on_delete=models.CASCADE, verbose_name='')
    person = models.IntegerField(verbose_name='')
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.appointed)

    @property
    def status_verbose(self):
        return PlanLinesLink.StatusChoices.labels[self.status]