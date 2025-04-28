from django.core.management import BaseCommand

from generator.services.generator_service import GeneratorService


class Command(BaseCommand):
    def handle(self, *args, **options):
        GeneratorService.copy_rpd_program(3636, 3637)