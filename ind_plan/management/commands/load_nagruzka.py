import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from tqdm import tqdm

from arim.models import Person2Uchnagr, CatPerson, Catadmission
from datetime import datetime


class Command(BaseCommand):
    help = 'Import data from CSV to Person2Uchnagr model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r', encoding='cp1251') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            academic_year = datetime.now().year - (1 if datetime.now().month < 9 else 0)

            snaptime = timezone.now()

            for row in tqdm(list(csv_reader)):
                # Создаем или получаем связанные объекты
                # Предполагаем, что у вас есть логика для получения этих объектов
                cperson_obj = CatPerson.objects.filter(id1c=row['IDПреподавателя']).first()
                cadmission_obj = Catadmission.objects.filter(name=row['Группа'][:-2]).first()

                # Преобразуем данные
                c1pers =row['IDПреподавателя']
                hour = float(row['Часы']) if row['Часы'] else None
                studcount = int(row['КолСтудентов']) if row['КолСтудентов'] else 0
                kurs = int(row['Курс']) if row['Курс'] else None
                sem = int(row['Семестр']) if row['Семестр'] else None

                # Создаем запись
                person2uchnagr = Person2Uchnagr(
                    c1pers=c1pers,
                    name=row['ФИОПреподавателя'],
                    cperson=cperson_obj,
                    discpl=row['Дисциплина'],
                    grup=row['Группа'],
                    hour=hour,
                    formcontr=row['ВидРабот'],
                    sem=sem,
                    metka=row.get('IDПотока', ''),
                    kurs=kurs,
                    direction=row['УровеньОбучения'],
                    doljnost=row['ТипСтавки'],
                    studcount=studcount,
                    ddat=snaptime,
                    cadmission=cadmission_obj,
                    snapshot_time=snaptime,
                    year=academic_year
                )

                person2uchnagr.save()

