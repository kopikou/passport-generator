from rest_framework import serializers

from auths.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user_id',
            "last_name",
            "first_name",
            "middle_name",
        ]