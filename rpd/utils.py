from django.db import models

class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)

class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(model=self.model, using=self._db, hints=self._hints).filter(is_deleted=False)


class TimestampsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()
    default_objects = models.Manager()


    class Meta:
        abstract = True

    def restore(self):
        self.is_deleted = False
        self.save()


