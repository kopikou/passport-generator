from django.core.management import BaseCommand
from tqdm import tqdm

from generator.models import PlanLinesLink
from generator.services import ReportService


class Command(BaseCommand):
    def handle(self, *args, **options):
        links = PlanLinesLink.objects.filter(uploaded_directly=False)
        c = 0
        t = tqdm(links)
        for l in t:
            need_rebuild = False
            if l.file and not l.file.storage.exists(l.file.name):
                l.file = None
                need_rebuild = True
            if l.last_accepted_file and not l.last_accepted_file.storage.exists(l.last_accepted_file.name):
                l.last_accepted_file = None
                need_rebuild = True

            if need_rebuild:
                ReportService.generate_rpd_report(l)
            c += 1
        print(c)
