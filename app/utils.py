from django import forms
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.forms import SimpleArrayField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, MultipleChoiceField
from rest_framework.permissions import BasePermission

from auths.models import Permissions


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

