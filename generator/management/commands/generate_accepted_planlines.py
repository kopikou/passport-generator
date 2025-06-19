from django.core.management import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from generator.models import PlanLinesLink
from generator.services import ReportService
from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    def handle(self, *args, **options):
        links = PlanLinesLink.objects.filter(
            Q(last_accepted_file__isnull=True) | Q(last_accepted_file__exact=''),
            status=PlanLinesLink.StatusChoices.accepted,
            uploaded_directly=False,
        )
        pbar = tqdm(links)
        for l in pbar:
            pbar.set_description(f"PlanLinesLink: {l.id}")
            ReportService.generate_rpd_report(l)