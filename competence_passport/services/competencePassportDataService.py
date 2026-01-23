from django.conf import settings
from competence_passport.services.matrixService import MatrixService
from competence_passport.services.schemaService import SchemaService
from competence_passport.services.passportService import PassportService
from competence_passport.services.ruleService import RuleService
from competence_passport.serializer import PlanSerializer
from generator.models import PlanLinesLink
from rpd.models.rpd_models import PlanData, LinesData
from arim.services import AISServices
import datetime

class CompetencePassportDataService:
    """Главный сервис для получения матрицы, схемы и паспорта компетенций"""
    @staticmethod
    def get_competence_passport_data(plan_id):
        """Все данные матрицы, схемы и паспорта компетенций"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)
        plan_serializer = PlanSerializer(plan)
        plan_data = plan_serializer.data


        plan_line_link = PlanLinesLink.objects.filter(planlines__plan=plan).first()
        cadmission = plan_line_link.cadmission
        admission_info = AISServices.get_admissionn_info(cadmission) if not settings.DISABLE_MIRA else {
            "id": 25064,
            "yr": 2025,
            "abbr": "ИСТб",
            "cuchplan_id": 10179,
            "spec_name": "Информационные системы и технологии в административном управлении",
            "direct_name": "Информационные системы и технологии",
            "kvalif_name": "Бакалавр",
            "ckaf_id": 1988626,
            "cfac_id": 46,
            "ckaf__name": "Информационных технологий и анализа данных",
            "ckaf__ccatdep__nameshort": "Институт информационных технологий и анализа данных ",
            "cfac__name": "Институт информационных технологий и анализа данных",
            "cadmkind": 2,
            "cadmkind__name": "бакалавры",
            "cadmkind__name_prof": "профиль",
            "cdirection": 812733,
            "cdirection__name": "Информационные системы и технологии",
            "cdirection__cod": "09.03.02",
            "cspec": None,
            "cspec__name": None,
            "cspec__code": None,
            "cfob": 1,
            "cfob__name": "очная"
        }

        raw_disciplines = RuleService.get_all_disciplines(
            plan_id=plan,
            filter=True,
            exclude_children=False
        )
        disciplines = []
        for disc in raw_disciplines:
            disciplines.append({
                "discipline_id": disc['id'],
                "discipline_index": disc['newdisid'],
                "discipline_name": disc['dis'] or "",
                "type": RuleService.get_discipline_types(disc['newdisid'])
            })

        discipline_ids = [d['id'] for d in raw_disciplines]
        raw_competences = RuleService.get_all_competences(
            planlineid__in=discipline_ids
        )
        competences = []
        for comp in raw_competences:
            competences.append({
                "competence_index": comp['competence_index'],
                "competence": comp['competence'],
                "type": RuleService.get_competence_type(comp['competence_index'])
            })

        matrix = MatrixService.get_competence_matrix(plan_id)
        schema = SchemaService.get_competence_schema(plan_id)
        passport = PassportService.get_competence_passport(plan_id)

        
        data = {
            'admission_info': admission_info,
            'plan': plan_data,
            'competences': competences,
            'disciplines': disciplines,
            'matrix': matrix,
            'schema': schema,
            'passport': passport 
        }
        return data

    @staticmethod
    def get_group_list(user_mira_id, year=datetime.datetime.now().year, group_txt_filter=''):
        data = AISServices.get_groups_by_person(id = user_mira_id, year = year, group_txt_filter = group_txt_filter)

        abbr_to_info = {}
        for item in data:
            abbr = item['abbr']
            if abbr not in abbr_to_info:
                abbr_to_info[abbr] = {
                    'abbr': abbr,
                    'plan_id': item['plan_id'],
                    'yr': year,
                    'planlin_list': []
                }
            abbr_to_info[abbr]['planlin_list'].append(item['planlin'])

        all_planlin_ids = [pid for info in abbr_to_info.values() for pid in info['planlin_list']]

        raw_lines = LinesData.objects.filter(
            mira_id__in=all_planlin_ids,
            plan__file__status=4,
            synchronize=True
        ).select_related('plan__file')

        planlin_to_file_url = {}
        for ld in raw_lines:
            if ld.plan.file:
                url = settings.SITE_URL + ld.plan.file.file.url
                planlin_to_file_url[str(ld.mira_id)] = url

        data = []
        for abbr, info in abbr_to_info.items():
            plx_file = ''
            for planlin in info['planlin_list']:
                plx_file = planlin_to_file_url.get(str(planlin), '')
                if plx_file:
                    break 

            data.append({
                'abbr': abbr,
                'plan_id': info['plan_id'],
                'yr': info['yr'],
                'plx_file': plx_file,
            })

        data.sort(key=lambda x: x['abbr'].lower())
        return data

    