from django.apps import AppConfig
from mssql.base import DatabaseWrapper

DatabaseWrapper._sql_server_versions[8] = 2000
class ArimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arim'
