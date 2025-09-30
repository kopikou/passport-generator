from django.core.management import BaseCommand
from tqdm import tqdm

from generator.models import PlanLinesLink
from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    help = 'Updates all rpd signatures'

    def handle(self, *args, **options):
        planlines = PlanLinesLink.objects.all()
        total_count = planlines.count()

        print(f"Найдено {total_count} записей PlanLinesLink")

        for index, planline_instance in enumerate(tqdm(planlines, total=total_count, desc="Обновление подписей РПД"), 1):
            sig_id, sig_string = GeneratorService.get_sig_id_string(planline_instance)

            if sig_id and sig_string:
                planline_instance.last_accepted_sig_id = sig_id
                planline_instance.last_accepted_sig = sig_string
                planline_instance.save(update_fields=['last_accepted_sig_id', 'last_accepted_sig'])
