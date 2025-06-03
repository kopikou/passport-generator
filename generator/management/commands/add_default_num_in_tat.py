from pprint import pprint

from django.core.management import BaseCommand

from generator.models import AdditionalInfo
from rpd.models import LinesData


class Command(BaseCommand):
    def handle(self, *args, **options):

        data = AdditionalInfo.objects.filter(type='tat').select_related("planlineslink")

        lines = LinesData.objects

        for i in data:
            pprint(i.value)
            pprint(i.planlineslink.id)