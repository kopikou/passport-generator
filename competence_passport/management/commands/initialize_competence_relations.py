from django.core.management.base import BaseCommand
from django.db import transaction
from rpd.models.rpd_models import PlanData, LinesIndicators
from competence_passport.models import CompetenceRelations
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Инициализация записей CompetenceRelations для всех компетенций всех учебных планов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--plan-id',
            type=int,
            help='ID конкретного учебного плана для инициализации'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Обработать все учебные планы'
        )

    def handle(self, *args, **options):
        plan_id = options.get('plan_id')
        process_all = options.get('all')
        clean = options.get('clean')
        skip_existing = options.get('skip_existing')
        
        if plan_id:
            plans = PlanData.objects.filter(id=plan_id)
            if not plans.exists():
                self.stdout.write(self.style.ERROR(f'Учебный план с ID {plan_id} не найден'))
                return
        elif process_all:
            plans = PlanData.objects.all().order_by('id')
        else:
            self.stdout.write(self.style.WARNING(
                'Укажите --plan-id для конкретного плана или --all для всех планов'
            ))
            return
        
        total_created = 0
        total_updated = 0
        total_plans = 0
        
        with transaction.atomic():
            if clean:
                deleted_count = CompetenceRelations.objects.filter(plan__in=plans).delete()[0]
                self.stdout.write(f'Удалено {deleted_count} существующих записей')
            
            for plan in plans:
                total_plans += 1
                self.stdout.write(f'Обрабатывается план: {plan.planname} (ID: {plan.id}, MIRA ID: {plan.mira_id})')
                
                # Получаем все уникальные компетенции для этого плана
                competences = LinesIndicators.objects.filter(
                    planlineid__plan=plan,
                    competence_index__isnull=False
                ).values('competence_index', 'competence').distinct()
                
                self.stdout.write(f'  Найдено уникальных компетенций: {len(competences)}')
                
                plan_created = 0
                plan_updated = 0
                
                for comp in competences:
                    competence_index = comp['competence_index']
                    competence_name = comp['competence'] or ''

                    existing_relation = CompetenceRelations.objects.filter(
                        plan=plan,
                        competence_index=competence_index
                    ).first()
                    
                    if existing_relation:
                        if skip_existing:
                            continue

                        needs_update = False
                        
                        if existing_relation.competence != competence_name:
                            existing_relation.competence = competence_name
                            needs_update = True
                        
                        if needs_update:
                            existing_relation.save()
                            plan_updated += 1
                            if plan_updated % 100 == 0:
                                self.stdout.write(f'    Обновлено {plan_updated} записей...')
                    else:
                        CompetenceRelations.objects.create(
                            plan=plan,
                            competence_index=competence_index,
                            competence=competence_name,
                            relations='' 
                        )
                        plan_created += 1
                        total_created += 1
                        
                        if plan_created % 100 == 0:
                            self.stdout.write(f'    Создано {plan_created} записей...')
                
                total_updated += plan_updated
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  План {plan.id}: создано {plan_created}, обновлено {plan_updated}, '
                        f'всего компетенций {len(competences)}'
                    )
                )
        
        self.stdout.write(f'Обработано учебных планов: {total_plans}')
        self.stdout.write(f'Создано новых записей: {total_created}')
        self.stdout.write(f'Всего записей в базе: {CompetenceRelations.objects.count()}')
        
        plans_without_relations = []
        for plan in PlanData.objects.all():
            if not CompetenceRelations.objects.filter(plan=plan).exists():
                plans_without_relations.append(plan)
        
        if plans_without_relations:
            self.stdout.write(self.style.WARNING(f'\nПланы без записей CompetenceRelations: {len(plans_without_relations)}'))
            for plan in plans_without_relations[:10]: 
                self.stdout.write(f'  - {plan.planname} (ID: {plan.id})')
        
        # Проверяем дубликаты (должно быть по одной записи на компетенцию в плане)
        from django.db.models import Count
        duplicates = CompetenceRelations.objects.values(
            'plan', 'competence_index'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        if duplicates.exists():
            self.stdout.write(self.style.ERROR(f'\nНайдено дубликатов: {duplicates.count()}'))
            for dup in duplicates[:5]:
                relations = CompetenceRelations.objects.filter(
                    plan_id=dup['plan'],
                    competence_index=dup['competence_index']
                )
                self.stdout.write(f'  План {dup["plan"]}, компетенция "{dup["competence_index"]}": {dup["count"]} записей')
                for rel in relations[:3]:
                    self.stdout.write(f'    ID: {rel.id}, создано: {rel.created_at}')
        else:
            self.stdout.write(self.style.SUCCESS('\nДубликатов не найдено'))