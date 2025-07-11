from django.core.management import BaseCommand

from generator.models import PlanLinesLink
from rpd.models import LinesData


class Command(BaseCommand):

    def handle(self, *args, **options):
        lines_data = LinesData.objects.all()

        for lines in lines_data:
            plan_lines_link = PlanLinesLink.objects.filter(planlines=lines).first()

            if plan_lines_link:
                lines.mira_id = plan_lines_link.mira_id
                lines.save()