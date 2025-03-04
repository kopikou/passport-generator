from django.contrib.auth.models import User
from django.db import models

from auths.models import UserProfile
from rpd.models import LinesData, LinesIndicators
from app.utils import TimestampsModel


# Create your models here.
class PlanLinesLink(TimestampsModel):
    class StatusChoices(models.IntegerChoices):
        appointed = 0, "Назначен"
        is_filled = 1, "Заполняется"
        on_review = 2, "Отправлен на проверку"
        accepted = 3, "Утвержден"
        on_refile = 4, "Требуются правки"

    class UserTypeChoices(models.IntegerChoices):
        rop = 0, "Руководитель программы"
        zav = 1, "Заведующий кафедрой"
        director = 2, "Директор института"

    cadmission = models.IntegerField()
    planlines = models.ForeignKey(LinesData, on_delete=models.CASCADE)
    mira_id = models.IntegerField()
    person = models.IntegerField()
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.appointed)
    protocol_number = models.TextField(null=True, blank=True)
    protocol_date = models.DateField(null=True, blank=True)
    user_accepted = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.IntegerField(choices=UserTypeChoices.choices, default=None, null=True, blank=True)
    meeting = models.TextField(null=True, blank=True)

    review_date = models.DateField(null=True, blank=True)
    accept_date = models.DateField(null=True, blank=True)

    @property
    def status_verbose(self):
        return PlanLinesLink.StatusChoices.labels[self.status]


class PlanLinesLinkComments(TimestampsModel):

    planlineslink = models.ForeignKey(PlanLinesLink, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_user_full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"


class FormControl(TimestampsModel):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64, unique=True)


class IndependentTypes(TimestampsModel):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64, unique=True)


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
    num = models.IntegerField()

    @property
    def formcontrol_verbose(self):
        return FormControl.objects.get(id=self.formcontrol_id).name


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
    num = models.IntegerField()

    @property
    def type_verbose(self):
        return DisciplineWorkHours.TypeChoices.labels[self.type]


class DefaultsResources(TimestampsModel):

    class TypeChoices(models.IntegerChoices):
        web_resources = 0, "Интернет"
        storage = 1, "База данных"

    name = models.TextField(verbose_name="Наименование ресурса")
    url = models.TextField(verbose_name="Ссылка на ресурс", null=True, blank=True)
    type = models.IntegerField(choices=TypeChoices.choices)


class AdditionalInfo(TimestampsModel):
    planlineslink = models.ForeignKey("PlanLinesLink", on_delete=models.CASCADE, related_name="additional_info")
    type = models.TextField()
    value = models.JSONField(default=dict)


class ScientificPlanData(TimestampsModel):

    cfac = models.TextField(null=True, blank=True)
    cfob = models.TextField(null=True, blank=True)
    ckaf = models.TextField(null=True, blank=True)
    director = models.TextField(null=True, blank=True)
    fgt = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    rng = models.CharField(null=True, blank=True)
    rop = models.TextField(null=True, blank=True)
    startyear = models.CharField(null=True, blank=True)
    viceRector = models.TextField(null=True, blank=True)
    year = models.CharField(null=True, blank=True)
    zavkaf = models.TextField(null=True, blank=True)
    mira_id = models.IntegerField()

    def __str__(self):
        return self.name
