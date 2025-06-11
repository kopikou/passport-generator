from django.core.management import BaseCommand
from tqdm import tqdm

from generator.models import PlanLinesLink
from generator.services import ReportService
from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    def handle(self, *args, **options):
        links = PlanLinesLink.objects.filter(
            status=PlanLinesLink.StatusChoices.accepted,
            uploaded_directly=False
        )
        pbar = tqdm(links)
        for l in pbar:
            pbar.set_description(f"Link {l.id}")
            ReportService.generate_rpd_report(l)