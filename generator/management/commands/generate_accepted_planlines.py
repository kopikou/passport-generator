from django.core.management import BaseCommand
from tqdm import tqdm

from generator.models import PlanLinesLink
from generator.services import ReportService
from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    def handle(self, *args, **options):
        links = PlanLinesLink.objects.filter(status=PlanLinesLink.StatusChoices.accepted)
        for l in tqdm(links):
            ReportService.generate_rpd_report(l)