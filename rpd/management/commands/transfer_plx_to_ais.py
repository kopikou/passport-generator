from django.core.management import BaseCommand

from rpd.models import RPDFile, LinesData, PlanData


class Command(BaseCommand):
    help = "Перенос данных о планах (план, дисциплины, семестры) из системы в АИС"

    def handle(self, *args, **options):
        data = RPDFile.objects.filter(status=RPDFile.StatusChoice.accepted)
        print(data)

        data = data.update(status=RPDFile.StatusChoice.on_synchronize)

        print(data)
        for i in data:
            plan_data = PlanData.objects.filter(file_id=i.id)
            line_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id)
            semester_data = LinesData.objects.filter(synchronize=True, plan__file_id=i.id)

            print(i)