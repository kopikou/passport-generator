from rest_framework import serializers

from rpd.models import RPDFiles

class RpdFilesSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    file = serializers.FileField()

    class Meta:
        model = RPDFiles
        fields = [
            'user',
            'title',
            'file',
        ]