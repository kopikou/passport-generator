from rest_framework import serializers

from uplfile.models import UploadFiles


class UploadFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
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
        pass
