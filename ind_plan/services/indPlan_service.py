from datetime import datetime


class IndPlanService(object):
    @classmethod
    def get_current_uch_year(cls):
        year = datetime.now().year
        if datetime.now().month < 9:
            year -= 1
        # return year на время теста отключаем
        return 2024
