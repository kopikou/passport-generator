from django.contrib.auth.models import User
from django.db import models

from generator.models import PlanLinesLink
from rpd.models import DocumentsTypes, PlanData
from app.utils import TimestampsModel

def get_upload_dir(instance, filename):
    plan_data = PlanData.objects.get(id=instance.rpd_id)
    fname = f'{instance.title}.{filename.split(".")[-1].lower()}'
    return f'files/{plan_data.abbrprofile}-{str(plan_data.startyear)[-2:]}/{fname}'

class UploadFiles(TimestampsModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.TextField()
    file = models.FileField(upload_to=get_upload_dir)
    type = models.ForeignKey(DocumentsTypes, on_delete=models.CASCADE)
    rpd = models.ForeignKey(PlanData, on_delete=models.CASCADE, related_name="uplfile")
    line = models.ForeignKey(PlanLinesLink, on_delete=models.CASCADE, null=True)



