from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.forms import CheckboxSelectMultiple, MultipleChoiceField
from rest_framework.permissions import BasePermission


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


def cache_function(timeout=60 * 15):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if settings.ENABLE_CACHE_FUNCTION_DECORATOR:
                key = f'{func.__name__}-{args}-{kwargs}'
                result = cache.get(key)
                if not result:
                    result = func(*args, **kwargs)
                    cache.set(key, result, timeout)
            else:
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


class CheckboxSelectMultipleEx(CheckboxSelectMultiple):
    def format_value(self, value):
        return value.split(",")


class UserProfileHasPermission(BasePermission):
    message = "У вас не достаточно прав"

    def __init__(self, permission):
        super().__init__()
        self.permission = permission

    def __call__(self):
        return self

    def has_permission(self, request, view):
        return self.permission in request.user.userprofile.permissions
