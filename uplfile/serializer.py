import os

from rest_framework import serializers

from uplfile.models import UploadFiles


class UploadFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    file = serializers.FileField()
    type_id = serializers.IntegerField()
    rpd_id = serializers.IntegerField()
    line_id = serializers.IntegerField(required=False)

    class Meta:
        model = UploadFiles
        fields = [
            'id',
            'user_id',
            'title',
            'type_id',
            'file',
            'rpd_id',
            'line_id',
        ]

    def create(self, validated_data):

        uplfile = [i for i in UploadFiles.objects.filter(
            type_id=validated_data['type_id'],
            rpd_id=validated_data['rpd_id'],
        )]

        if uplfile:
            if os.path.exists(path=uplfile[0].file.path):
                os.remove(path=uplfile[0].file.path)

        result, created = UploadFiles.objects.update_or_create(
            type_id=validated_data['type_id'],
            rpd_id=validated_data['rpd_id'],
            defaults=validated_data,
        )

        return result
