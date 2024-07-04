from rest_framework import serializers

from rpd.models import RPDFile


class RpdFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    file = serializers.FileField()

    class Meta:
        model = RPDFile
        fields = [
            'id',
            'user_id',
            'title',
            'file',
        ]