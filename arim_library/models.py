from django.db import models

# Create your models here.
class IrbisData(models.Model):
    class Meta:
        db_table = "irbisdata"
        managed = False

    idd = models.IntegerField()
    irbisid = models.CharField(max_length=64, null=True, blank=True)
    bib_disc = models.CharField(max_length=500, null=True, blank=True)
    rubrica = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    avtors = models.CharField(max_length=200, null=True, blank=True)
    cnt = models.IntegerField(null=True, blank=True)
    year_izd = models.IntegerField(null=True, blank=True)
    http_link = models.CharField(max_length=200, null=True, blank=True)
    izd_type = models.CharField(max_length=16, null=True, blank=True)
    place = models.CharField(max_length=20, null=True, blank=True)
