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
            SELECT ckaf2rpgen as value, name2rpgen as label, ckaf2istu FROM dbo.uchplan_kaf ORDER BY name2rpgen
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
    @cache_function(timeout=10 * 1)
    def get_disciplines_by_person(id):

        q = f"""exec rpd_list_for_person {int(id)}"""

        r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
            "q": q
        }, proxies={
            "http": "",
            "https": "",
        })

        data = r.json()['RecordSet']

        return data

    @staticmethod
    def get_plan_in_mira():

        q = f"""exec rpd_list_for_person {int(id)}"""

        r = requests.get(f"{settings.ARIM_URL}/wizard.sql", {
            "q": q
        }, proxies={
            "http": "",
            "https": "",
        })

        data = r.json()['RecordSet']

        return data
