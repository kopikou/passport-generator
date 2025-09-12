from django.db import models

class AspPlan(models.Model):
    class Meta:
        db_table = 'asp_plan'
        managed = False

    admis_id = models.IntegerField()
    plan_id = models.IntegerField()
    start_date = models.DateField()
    edit_date = models.DateField()
    author_id = models.IntegerField()


class AspParamValue(models.Model):
    class Meta:
        db_table = 'asp_param_value'
        managed = False

    type_id = models.IntegerField()
    value = models.TextField()
    linked = models.ForeignKey('AspParamValue', on_delete=models.CASCADE, null=True, blank=True)
    plan_id = models.IntegerField()
    sort = models.IntegerField(null=True, blank=True)


class AspParamType(models.Model):
    class Meta:
        db_table = 'asp_param_type'
        managed = False

    descr = models.TextField()
    name = models.TextField()
    group_id = models.IntegerField(null=True, blank=True)
    is_group = models.IntegerField(default=0)


class Competence(models.Model):
    code = models.IntegerField()
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_competences"
        managed = False


class Indikator(models.Model):
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_indikator"
        managed = False


class Discipline(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "mleha_dis"
        managed = False


class Plan(models.Model):
    species = models.CharField(max_length=4096)
    subtype = models.CharField(max_length=64)
    shifr = models.CharField(max_length=8)
    studyprog = models.CharField(max_length=64)
    studyform = models.CharField(max_length=48)
    studylevel = models.CharField(max_length=64)
    fullplanname = models.CharField(max_length=256)
    planname = models.CharField(max_length=256)
    usernum = models.IntegerField()
    vuzname = models.CharField(max_length=256)
    head = models.CharField(max_length=256)
    whoratif = models.CharField(max_length=128)
    kafcode = models.CharField(max_length=256)
    faculty = models.CharField(max_length=256)
    lastshifr = models.CharField(max_length=64)
    abbrprofile = models.CharField(max_length=32)
    startyear = models.IntegerField()
    ekinhoursum = models.BooleanField()
    dviga = models.IntegerField()
    gviga = models.IntegerField()
    detailgia = models.IntegerField()
    igazetweek = models.FloatField()
    igahourzet = models.FloatField()
    ksriz = models.CharField(max_length=16)
    oopet = models.IntegerField()
    lekc = models.FloatField()
    dvv = models.FloatField()
    maxnagr = models.FloatField()
    vidplan = models.IntegerField()
    levelcode = models.CharField(max_length=4)
    sokrcontrolfact = models.IntegerField()
    semesteroncource = models.IntegerField()
    elementsinweek = models.IntegerField()
    gosdate = models.DateField
    gosdocument = models.IntegerField()
    gostype = models.FloatField()
    addition = models.CharField(max_length=64)
    additiondate = models.DateField()
    additionversion = models.IntegerField()
    naprcode = models.CharField(max_length=64)
    napr_e = models.CharField(max_length=1024)
    napr_t = models.CharField(max_length=1024)

    class Meta:
        db_table = "mleha_plan"
        managed = False


class Planlines(models.Model):
    planid = models.ForeignKey(Plan, on_delete=models.PROTECT, null=False, db_constraint=False)
    dis = models.CharField(max_length=1024)
    disid = models.ForeignKey(Discipline, on_delete=models.PROTECT, null=False, db_constraint=False)
    newcycle = models.CharField(max_length=32)
    newdisid = models.CharField(max_length=32)
    cycle = models.CharField(max_length=32)
    iddis = models.CharField(max_length=32)
    gos = models.IntegerField()
    sr = models.IntegerField()
    kompetences = models.CharField(max_length=4096)
    mustbesdudied = models.IntegerField()
    creditstodis = models.IntegerField()
    hoursinzet = models.IntegerField()
    caf = models.IntegerField()
    razdel = models.IntegerField()
    nocalccontrol = models.IntegerField()
    hourinter = models.IntegerField()
    disforraz = models.BooleanField()
    dsforraz = models.BooleanField()
    is_del = models.BooleanField(db_column='del')
    block = models.IntegerField()
    maxvar = models.IntegerField()
    type = models.IntegerField()
    viewpract = models.IntegerField()
    viewobject = models.IntegerField()

    class Meta:
        db_table = "mleha_planlines"
        managed = False


class PlanCompetence(models.Model):
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    competenceid = models.ForeignKey(Competence, on_delete=models.PROTECT, null=False, db_constraint=False)

    class Meta:
        db_table = "mleha_plancompetence"
        managed = False


class PlanIndikator(models.Model):
    indikid = models.ForeignKey(Indikator, on_delete=models.PROTECT, null=False, db_constraint=False)
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    competenceid = models.ForeignKey(Competence, on_delete=models.PROTECT, null=False, db_constraint=False)
    znat = models.CharField(max_length=4000)
    umet = models.CharField(max_length=4000)
    vladet = models.CharField(max_length=4000)
    kriteriy_oceniv = models.CharField(max_length=4000)
    metod_oceniv = models.CharField(max_length=4000)

    class Meta:
        db_table = "mleha_planindikator"
        managed = False

class Semestr(models.Model):
    planlineid = models.ForeignKey(Planlines, on_delete=models.PROTECT, null=False, db_constraint=False)
    num = models.IntegerField()
    lekc = models.IntegerField()
    lab = models.IntegerField()
    pr = models.IntegerField()
    srs = models.IntegerField()
    ekzhour = models.IntegerField()
    zet = models.FloatField()
    ekz = models.BooleanField()
    zach = models.BooleanField()
    intpr = models.IntegerField()
    intlek = models.IntegerField()
    intlab = models.IntegerField()
    kp = models.BooleanField()
    kr = models.BooleanField()
    proektprvned = models.FloatField()
    proektlekvned = models.FloatField()
    proektlabvned = models.FloatField()
    proektzet = models.FloatField()
    zacho = models.IntegerField()
    contr = models.IntegerField()
    contrrab = models.IntegerField()
    sessnum = models.IntegerField()
    ip = models.IntegerField()
    sure_hour = models.IntegerField()
    cons_hour = models.IntegerField()
    ip_hour = models.IntegerField()
    kp_hour = models.IntegerField()
    kr_hour = models.IntegerField()
    maxvar = models.IntegerField()
    seminar = models.IntegerField()
    spo_pr_hours = models.IntegerField()
    eios = models.IntegerField()
    pp = models.IntegerField()

    class Meta:
        db_table = "mleha_semestr"
        managed = False