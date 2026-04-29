from django.core.management.base import BaseCommand
from django.db import transaction
from competence_passport.models import Scheme, Competence

class Command(BaseCommand):
    help = 'Заполняет поле competence_id в модели Scheme на основе competence_index'

    def handle(self, *args, **options):   
        updated_count = 0
        
        with transaction.atomic():
            schemes_to_update = Scheme.objects.filter(
                competence_id__isnull=True,
                competence_index__isnull=False
            ).select_related('planlineid')
            
            total = schemes_to_update.count()
            self.stdout.write(f'Найдено записей для обработки: {total}')
            
            for scheme in schemes_to_update:
                competence = Competence.objects.get(
                    competence_index=scheme.competence_index,
                    plan_id=scheme.planlineid.plan_id
                )

                scheme.competence_id = competence
                scheme.save(update_fields=['competence_id'])
                updated_count += 1
                        
        self.stdout.write(self.style.SUCCESS(f'Обновлено: {updated_count}, '))