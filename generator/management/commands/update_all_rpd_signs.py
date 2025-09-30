from django.core.management import BaseCommand

from generator.models import PlanLinesLink
from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    help = 'Updates all rpd signatures'

    def handle(self, *args, **options):
        planlines = PlanLinesLink.objects.all()
        for planline_instance in planlines:
            sig_id, sig_string = GeneratorService.get_sig_id_string(planline_instance)

            if sig_id and sig_string:
                planline_instance.last_accepted_sig_id = sig_id
                planline_instance.last_accepted_sig = sig_string

                planline_instance.save(update_fields=['last_accepted_sig_id', 'last_accepted_sig'])
