from rest_framework import serializers

from rpd.models import RPDFile


class RpdFileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    file = serializers.FileField()

    class Meta:
        model = RPDFile
        fields = [
            'user_id',
            'title',
            'file',
        ]