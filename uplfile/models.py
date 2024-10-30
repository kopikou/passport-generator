from django.contrib.auth.models import User
from django.db import models

from generator.models import PlanLinesLink
from rpd.models import DocumentsTypes, PlanData
from rpd.utils import TimestampsModel


class UploadFiles(TimestampsModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.TextField()
    file = models.FileField(upload_to="uploads/files/%Y-%m-%d/")
    type = models.ForeignKey(DocumentsTypes, on_delete=models.CASCADE)
    rpd = models.ForeignKey(PlanData, on_delete=models.CASCADE)
    line = models.ForeignKey(PlanLinesLink, on_delete=models.CASCADE, null=True)
