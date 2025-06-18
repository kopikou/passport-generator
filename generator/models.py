from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.enums import TextChoices, IntegerChoices

from auths.models import UserProfile
from rpd.models import LinesData, LinesIndicators
from app.utils import TimestampsModel, OverwriteStorage


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
    mira_id = models.IntegerField(verbose_name="id из UchPlanLines")
    person = models.IntegerField()
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.appointed)
    protocol_number = models.TextField(null=True, blank=True)
    protocol_date = models.DateField(null=True, blank=True)

    # user_accepted = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.IntegerField(choices=UserTypeChoices.choices, default=None, null=True, blank=True)

    user_confirmed = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кто согласовал, должен РОП", related_name="confirmed_plans")
    user_accepted = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кто утвердил, должен зав.каф", related_name="accepted_plans")

    meeting = models.TextField(null=True, blank=True)

    review_date = models.DateField(null=True, blank=True)
    accept_date = models.DateField(null=True, blank=True)
    confirm_date = models.DateField(null=True, blank=True)

    can_be_copied_by_anyone = models.BooleanField("Каждый ли может скопировать программу", default=False)

    file = models.FileField(upload_to="rpd_generator/", verbose_name="Файл программы", null=True)
    last_accepted_file = models.FileField(upload_to="rpd_generator/", verbose_name="Файл программы", null=True)
    file_updated_at = models.DateTimeField(null=True, blank=True)
    uploaded_directly = models.BooleanField("Был ли файл загружен напрямую", null=True, default=False)
    can_upload_file_directly = models.BooleanField("Можно ли файл загрузать напрямую", null=True, default=False)
    #
    # @property
    # def is_spo(self):
    #     return self.planlines.caf in (1988516, 1988517)

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
    formcontrol = models.ForeignKey("FormControl", on_delete=models.CASCADE, null=True, blank=True)
    formcontrol_list = ArrayField(models.IntegerField(), default=list, null=True)
    comment = models.TextField()
    num = models.IntegerField()

    @property
    def formcontrol_verbose(self):

        formcontrol_names_by_id = {i.id: i.name for i in FormControl.objects.all()}
        res = []
        for i in self.formcontrol_list:
            res.append(formcontrol_names_by_id[i])

        return ', '.join(res)
        # return FormControl.objects.get(id=self.formcontrol_id).name


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


class ScientificData(TimestampsModel):

    plan = models.ForeignKey(ScientificPlanData, on_delete=models.CASCADE)
    text = models.TextField()
    parameters = models.JSONField()


class ScientificWorkType(TimestampsModel):
    name = models.TextField()

    def __str__(self):
        return self.name


class ScientificDataDefault(TimestampsModel):

    class PartChoices(IntegerChoices):
        science_research = 0, 'Примерный план выполнения научного исследования'
        dissertation_preparation = 1, 'Примерный план подготовки диссертации'
        publish_preparation = 2, 'Примерный план подготовки публикаций'


    text = models.TextField(verbose_name='Текст')
    semester = models.IntegerField(verbose_name='Семестр')
    order = models.IntegerField(verbose_name='Порядок')
    kurs = models.IntegerField(verbose_name='Сколько курсов идет программа (3 или 4)')
    part = models.IntegerField(choices=PartChoices.choices)

    def __str__(self):
        return f"{self.kurs} | {self.semester} | {self.order} | {self.name}"


