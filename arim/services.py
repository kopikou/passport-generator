from json import JSONDecodeError

import pendulum
import requests
from django.conf import settings

from app.utils import cache_function


class AISServices(object):
    @staticmethod
    @cache_function(timeout=60 * 1)
    def get_kaf_codes():
        q = """
            SELECT ckaf2rpgen as value, name2rpgen as label FROM dbo.uchplan_kaf ORDER BY name2rpgen
            """

        r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
            "q": q
        }, proxies={
            "http": "",
            "https": "",
        })

        data = r.json()['RecordSet']

        return data

    @staticmethod
    def get_ap1(param):
        return {
            "param": param
        }