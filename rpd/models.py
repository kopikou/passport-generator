from django.db import models
from rpd.utils import TimestampsModel


# Create your models here.
class RPDFiles(TimestampsModel):
    title = models.CharField(max_length=100, verbose_name="Наименование файла")
    file = models.FileField(upload_to="uploads/%Y-%m-%d/", verbose_name="Файл РПД")

    def delete(self):
        self.is_deleted = True
        self.save()


class Competence(models.Model):
    code = models.IntegerField()
    index = models.CharField(max_length=32)
    content = models.CharField(max_length=2048)

    class Meta:
        db_table = "mleha_competences"
        managed = False
