from django.db.backends.postgresql.base import DatabaseWrapper
from django.db.backends.postgresql.features import DatabaseFeatures


class DatabaseFeatures(DatabaseFeatures):
    minimum_database_version = (9, )


class DatabaseWrapper(DatabaseWrapper):
    features_class = DatabaseFeatures
