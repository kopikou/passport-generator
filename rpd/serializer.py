from rest_framework import serializers

from rpd.models import RPDFile, PlanData, Disciplines, LinesData


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


class PlanDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    file_id = serializers.IntegerField()
    subtype = serializers.CharField()
    shifr = serializers.CharField()
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
    disid = serializers.IntegerField()
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

    class Meta:
        model = LinesData
        fields = [
            'id',
            'disid',
            'dis',
            'newdisid',
            'iddis',
            'mustbesdudied',
            'hoursinzet',
            'caf',
            'nocalccontrol',
            'type',
            'viewpract',
            'viewobject',
            'kompetences',
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

