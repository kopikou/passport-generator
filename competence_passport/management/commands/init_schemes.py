from django.core.management.base import BaseCommand
from django.db import transaction
from rpd.models.rpd_models import LinesData, LinesIndicators, SemesterData
from competence_passport.models import Scheme
from django.db.models import Q

class Command(BaseCommand):
    help = 'Инициализация схем форм аттестации из существующих данных семестров'

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic(): 
            Scheme.objects.all().delete()
            # Для каждой дисциплины с компетенциями
            disciplines = LinesData.objects.filter(
                indicators__competence_index__isnull=False
            ).distinct()
            
            for discipline in disciplines:
                # Получаем все компетенции дисциплины
                competences = LinesIndicators.objects.filter(
                    planlineid=discipline,
                    competence_index__isnull=False
                ).values('competence_index', 'competence').distinct()
                
                # Получаем семестры дисциплины
                semesters = SemesterData.objects.filter(planlineid=discipline)
                
                for comp in competences:
                    for sem in semesters:
                        # Проверяем, есть ли формы аттестации в этом семестре
                        has_forms = sem.ekz or sem.zach or (sem.zacho and sem.zacho > 0) or sem.kp or sem.kr
                        
                        if has_forms:
                            # Создаем запись в Scheme
                            Scheme.objects.create(
                                planlineid=discipline,
                                competence_index=comp['competence_index'],
                                competence=comp['competence'],
                                semester=sem.num,
                                ekz=bool(sem.ekz),
                                zach=bool(sem.zach),
                                zacho=bool(sem.zacho and sem.zacho > 0),
                                kp=bool(sem.kp),
                                kr=bool(sem.kr)
                            )
                            count += 1
                            
                            if count % 100 == 0:
                                self.stdout.write(f'Created {count} schemes...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} scheme records'))