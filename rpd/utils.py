from django.db import models


class TimestampsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
