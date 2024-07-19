from rest_framework import serializers

from rpd.models import RPDFile, PlanData, Disciplines, LinesData, SemesterData, LinesIndicators, PlanDocuments


class RpdFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    file = serializers.FileField()
    status = serializers.IntegerField()

    class Meta:
        model = RPDFile
        fields = [
            'id',
            'user_id',
            'title',
            'file',
            'status',
        ]


class SemesterDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    planlineid_id = serializers.IntegerField()
    num = serializers.IntegerField()
    lekc = serializers.IntegerField(allow_null=True)
    lab = serializers.IntegerField(allow_null=True)
    pr = serializers.IntegerField(allow_null=True)
    srs = serializers.IntegerField(allow_null=True)
    ekzhour = serializers.IntegerField(allow_null=True)
    zet = serializers.IntegerField(allow_null=True)
    ekz = serializers.BooleanField(allow_null=True)
    zach = serializers.BooleanField(allow_null=True)
    kp_hour = serializers.IntegerField(allow_null=True)
    kp = serializers.BooleanField(allow_null=True)
    kr_hour = serializers.IntegerField(allow_null=True)
    kr = serializers.BooleanField(allow_null=True)
    zacho = serializers.IntegerField(allow_null=True)
    eios = serializers.IntegerField(allow_null=True)

    class Meta:
        model = SemesterData
        fields = [
            'id',
            'planlineid_id',
            'num',
            'lekc',
            'lab',
            'pr',
            'srs',
            'ekzhour',
            'zet',
            'ekz',
            'zach',
            'kp_hour',
            'kp',
            'kr_hour',
            'kr',
            'zacho',
            'eios',
        ]


class PlanDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file_id = serializers.IntegerField()
    subtype = serializers.CharField()
    shifr = serializers.CharField()
    abbrprofile = serializers.CharField(allow_null=True, allow_blank=True)
    studyform = serializers.CharField()
    studylevel = serializers.CharField()
    studyprog = serializers.CharField()
    elementsinweek = serializers.IntegerField()
    species = serializers.CharField()
    usernum = serializers.IntegerField()
    whoratif = serializers.CharField()
    planname = serializers.CharField()
    kafcode = serializers.IntegerField(allow_null=True)
    startyear = serializers.IntegerField()
    dviga = serializers.BooleanField()
    gviga = serializers.BooleanField()
    igazetweek = serializers.FloatField()
    igahourzet = serializers.FloatField()
    semesteroncource = serializers.IntegerField()
    gosdate = serializers.DateField()
    lastshifr = serializers.CharField()
    napr_e = serializers.CharField()
    napr_t = serializers.CharField()
    vuzname = serializers.CharField()
    head = serializers.CharField(allow_null=True, allow_blank=True)
    faculty = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = PlanData
        fields = [
            'id',
            'file_id',
            'subtype',
            'shifr',
            'abbrprofile',
            'studyform',
            'studylevel',
            'studyprog',
            'elementsinweek',
            'species',
            'usernum',
            'whoratif',
            'planname',
            'kafcode',
            'startyear',
            'dviga',
            'gviga',
            'igazetweek',
            'igahourzet',
            'semesteroncource',
            'gosdate',
            'lastshifr',
            'napr_e',
            'napr_t',
            'vuzname',
            'head',
            'faculty',
        ]


class LinesDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    plan_id = serializers.IntegerField()
    disid_id = serializers.IntegerField()
    dis = serializers.CharField()
    newdisid = serializers.CharField(allow_null=True, allow_blank=True)
    mustbesdudied = serializers.IntegerField(allow_null=True)
    hoursinzet = serializers.IntegerField(allow_null=True)
    caf = serializers.IntegerField(allow_null=True)
    nocalccontrol = serializers.BooleanField(allow_null=True)
    type = serializers.IntegerField(allow_null=True)
    viewpract = serializers.IntegerField(allow_null=True)
    viewobject = serializers.IntegerField(allow_null=True)
    kompetences = serializers.CharField(allow_null=True, allow_blank=True)
    synchronize = serializers.BooleanField()

    class Meta:
        model = LinesData
        fields = [
            'id',
            'plan_id',
            'disid_id',
            'dis',
            'newdisid',
            'mustbesdudied',
            'hoursinzet',
            'caf',
            'nocalccontrol',
            'type',
            'viewpract',
            'viewobject',
            'kompetences',
            'synchronize',
        ]


class LinesIndicatorsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    planlineid_id = serializers.IntegerField()
    competence_index = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    competence = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    indicator_index = serializers.CharField()
    indicator = serializers.CharField()

    class Meta:
        model = LinesIndicators
        fields = [
            'id',
            'planlineid_id',
            'competence_index',
            'competence',
            'indicator_index',
            'indicator',
        ]


class PlanDocumentsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    plan_id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.IntegerField()
    synchronize = serializers.BooleanField()
    manual = serializers.BooleanField(required=False)

    class Meta:
        model = PlanDocuments
        fields = [
            'id',
            'plan_id',
            'name',
            'type',
            'synchronize',
            'manual',
        ]


class DisciplinesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = Disciplines
        fields = [
            'id',
            'name',
        ]

