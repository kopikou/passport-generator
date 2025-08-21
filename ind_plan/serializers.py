from django.db import transaction
from rest_framework import serializers

from ind_plan.models import Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'type', 'hours_count']
        model = Work