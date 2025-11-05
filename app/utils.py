import os
import pathlib

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.core.files.utils import validate_file_name
from django.db import models, connections
from django.conf import settings
from django.core.cache import cache
from django.forms import CheckboxSelectMultiple, MultipleChoiceField
from rest_framework.permissions import BasePermission, IsAuthenticated
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session


class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(model=self.model, using=self._db, hints=self._hints).filter(is_deleted=False)


class TimestampsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    is_deleted = models.BooleanField(default=False, null=True)

    objects = models.Manager()
    # objects = BaseModelManager()
    # default_objects = models.Manager()

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


class UserProfileHasPermission(IsAuthenticated):
    message = "У вас не достаточно прав"

    def __init__(self, permission):
        super().__init__()
        self.permission = permission

    def __call__(self):
        return self

    def has_permission(self, request, view):
        return self.permission in request.user.userprofile.permissions


def dictfetchall(cursor):
    data = list(cursor.fetchall())
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in data
    ]


class DB:
    key = 'default'

    @classmethod
    def exec(cls, query, params, as_dict=False):
        data = None
        with connections[cls.key].cursor() as cursor:
            d = cursor.execute(query, params)
            while True:
                if cursor.description:
                    if as_dict:
                        data = dictfetchall(d)
                    else:
                        data = d.fetchall()
                if not cursor.nextset():
                    break
            connections[cls.key].commit()
        return data

    @classmethod
    def fetch(cls, query, params=None):
        if not params:
            params = []
        with connections[cls.key].cursor() as cursor:
            cursor.execute(query, params)
            data = dictfetchall(cursor)
        return data

    @classmethod
    def fetch_one_or_none(cls, query, params=None):
        data = cls.fetch(query, params)
        if not data:
            return None
        return data[0]

class RPGEN:
    key = 'rpgen'

    @classmethod
    def exec(cls, query, params, as_dict=False):
        db = DBRepository()

        data = None
        with db.cursor() as cursor:
            d = cursor.execute(query, params)
            while True:
                if cursor.description:
                    if as_dict:
                        data = dictfetchall(d)
                    else:
                        data = d.fetchall()
                if not cursor.nextset():
                    break
            connections[cls.key].commit()
        return data

    @classmethod
    def fetch(cls, query, params=None):

        if not params:
            params = []

        db = DBRepository()

        if not params:
            params = []
        with db.cursor() as cursor:
            cursor.execute(query, params)
            data = dictfetchall(cursor)
        return data


class Mira(DB):
    key = 'mira'


class SOP(DB):
    key = 'sop'


class DBRepository(object):
    db_conf_key = ""
    db_driver = ""

    def __init__(self) -> None:
        self.engine = create_engine(settings.RPGEN_CONNECTION_STRING)

    def session(self):
        return Session(self.engine)

    def cursor(self):
        connection = self.engine.raw_connection()
        return connection.cursor()


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        name = str(name).replace("\\", "/")
        dir_name, file_name = os.path.split(name)
        if ".." in pathlib.PurePath(dir_name).parts:
            raise SuspiciousFileOperation(
                "Detected path traversal attempt in '%s'" % dir_name
            )
        validate_file_name(file_name)

        return name

def shortify_name(name):
    parts = name.split(' ')
    return f"{parts[0]} {parts[1][0]}.{parts[2][0]}."