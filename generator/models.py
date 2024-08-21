from django.db import models

from rpd.models import LinesData
from rpd.utils import TimestampsModel


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

    @property
    def status_verbose(self):
        return PlanLinesLink.StatusChoices.labels[self.status]
