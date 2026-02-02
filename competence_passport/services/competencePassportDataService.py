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
import re
from docxtpl import DocxTemplate
from io import BytesIO
from pathlib import Path
from app.settings import BASE_DIR


class CompetencePassportDataService:
    """Главный сервис для получения матрицы, схемы и паспорта компетенций"""
    # @staticmethod
    # def get_competence_passport_data(plan_id):
    #     """Все данные матрицы, схемы и паспорта компетенций"""
    #     plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)
    #     plan_serializer = PlanSerializer(plan)
    #     plan_data = plan_serializer.data


    #     plan_line_link = PlanLinesLink.objects.filter(planlines__plan=plan).first()
    #     cadmission = plan_line_link.cadmission
    #     admission_info = AISServices.get_admissionn_info(cadmission) if not settings.DISABLE_MIRA else {
    #         "id": 25064,
    #         "yr": 2025,
    #         "abbr": "ИСТб",
    #         "cuchplan_id": 10179,
    #         "spec_name": "Информационные системы и технологии в административном управлении",
    #         "direct_name": "Информационные системы и технологии",
    #         "kvalif_name": "Бакалавр",
    #         "ckaf_id": 1988626,
    #         "cfac_id": 46,
    #         "ckaf__name": "Информационных технологий и анализа данных",
    #         "ckaf__ccatdep__nameshort": "Институт информационных технологий и анализа данных ",
    #         "cfac__name": "Институт информационных технологий и анализа данных",
    #         "cadmkind": 2,
    #         "cadmkind__name": "бакалавры",
    #         "cadmkind__name_prof": "профиль",
    #         "cdirection": 812733,
    #         "cdirection__name": "Информационные системы и технологии",
    #         "cdirection__cod": "09.03.02",
    #         "cspec": None,
    #         "cspec__name": None,
    #         "cspec__code": None,
    #         "cfob": 1,
    #         "cfob__name": "очная"
    #     }

    #     raw_disciplines = RuleService.get_all_disciplines(
    #         plan_id=plan,
    #         filter=True,
    #         exclude_children=False
    #     )
    #     disciplines = []
    #     for disc in raw_disciplines:
    #         disciplines.append({
    #             "discipline_id": disc['id'],
    #             "discipline_index": disc['newdisid'],
    #             "discipline_name": disc['dis'] or "",
    #             "type": RuleService.get_discipline_types(disc['newdisid'])
    #         })

    #     discipline_ids = [d['id'] for d in raw_disciplines]
    #     raw_competences = RuleService.get_all_competences(
    #         planlineid__in=discipline_ids
    #     )
    #     competences = []
    #     for comp in raw_competences:
    #         competences.append({
    #             "competence_index": comp['competence_index'],
    #             "competence": comp['competence'],
    #             "type": RuleService.get_competence_type(comp['competence_index'])
    #         })

    #     matrix = MatrixService.get_competence_matrix(plan_id)
    #     schema = SchemaService.get_competence_schema(plan_id)
    #     passport = PassportService.get_competence_passport(plan_id)

        
    #     data = {
    #         'admission_info': admission_info,
    #         'plan': plan_data,
    #         'competences': competences,
    #         'disciplines': disciplines,
    #         'matrix': matrix,
    #         'schema': schema,
    #         'passport': passport 
    #     }
    #     return data
    
    @staticmethod
    def get_plan_admission_data(plan_id):
        """Данные плана и группы"""
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
        
        data = {
            'admission_info': admission_info,
            'plan': plan_data,
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
    
    @staticmethod
    def get_reference_data(plan_id):
        """Данные справочников"""
        plan = plan_id if isinstance(plan_id, PlanData) else PlanData.objects.get(mira_id=plan_id)
    
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
        
        data = {
            'competences': competences,
            'disciplines': disciplines,
        }
        return data
    
    @staticmethod
    def get_matrix_data(plan_id):
        """Все данные матрицы компетенций"""
        matrix = MatrixService.get_competence_matrix(plan_id)

        data = {
            'matrix': matrix,
        }
        return data
    
    @staticmethod
    def get_schema_data(plan_id):
        """Все данные схемы компетенций"""
        schema = SchemaService.get_competence_schema(plan_id)
        
        data = {
            'schema': schema,
        }
        return data

    
    @staticmethod
    def get_passport_data(plan_id):
        """Все данные паспорта компетенций"""
        passport = PassportService.get_competence_passport(plan_id) 
        data = {
            'passport': passport 
        }
        return data

    @classmethod
    def get_matrix_report(cls, plan_id):
        """Экспорт матрицы компетенций в Word"""
        data = cls.get_competence_passport_data(plan_id)
        admission_info = data['admission_info']
        
        # Агрегируем данные по иерархии
        matrix_hierarchy = cls.build_matrix_hierarchy(data['matrix'])
        
        context = {
            'matrix': matrix_hierarchy,
            'direction_code': admission_info.get('cdirection__cod', ''),
            'direction': admission_info.get('cdirection__name', ''),
            'spec_name': admission_info.get('spec_name', ''),
            'kvalif': admission_info.get('kvalif_name', ''),
            'fob': admission_info.get('cfob__name', ''),
            'year_post': str(admission_info.get('yr', '')),
            'protocol_year': str(admission_info.get('yr', ''))
        }
        
        template_path = f'{BASE_DIR}{Path("/templates/docxRPD/matrix.docx")}'
        doc = DocxTemplate(template_path)
        doc.render(context)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @staticmethod
    def build_matrix_hierarchy(matrix_data):
        """Иерархия дисциплин"""
        # Разделяем на группы и дисциплины
        groups = {}
        disciplines = []
        
        for item in matrix_data:
            if item['type'] == 'group':
                groups[item['discipline_index']] = {
                    'discipline_index': item['discipline_index'],
                    'discipline_name': item['discipline_name'],
                    'competence_list': item['competence_list'],
                    'disciplines': [] 
                }
            else:
                disciplines.append(item)
        
        # Назначаем дисциплины своим группам
        for disc in disciplines:
            # Находим родительскую группу 
            disc_parts = disc['discipline_index'].split('.')
            
            # Ищем самую глубокую подходящую группу
            for i in range(len(disc_parts) - 1, 0, -1):
                parent_index = '.'.join(disc_parts[:i])
                if parent_index in groups:
                    groups[parent_index]['disciplines'].append(disc)
                    break
        
        result = []
        for group_index in sorted(groups.keys()):
            group = groups[group_index]
            # Сортируем дисциплины внутри группы
            group['disciplines'].sort(key=lambda x: x['discipline_index'])
            result.append(group)
        
        return result
    
    @classmethod
    def get_schema_report(cls, plan_id):
        """Экспорт схемы компетенций в Word"""
        data = cls.get_competence_passport_data(plan_id)

        admission_info = data['admission_info']
        
        processed_schema = cls.process_schema_for_report(data['schema'])
        
        context = {
            'schema': processed_schema,
            'direction_code': admission_info.get('cdirection__cod', ''),
            'direction': admission_info.get('cdirection__name', ''),
            'spec_name': admission_info.get('spec_name', ''),
            'kvalif': admission_info.get('kvalif_name', ''),
            'fob': admission_info.get('cfob__name', ''),
            'year_post': str(admission_info.get('yr', '')),
            'protocol_year': str(admission_info.get('yr', ''))
        }
        
        template_path = f'{BASE_DIR}{Path("/templates/docxRPD/schema.docx")}'
        doc = DocxTemplate(template_path)
        
        doc.render(context)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @classmethod
    def process_schema_for_report(cls, schema_data):
        """
        Обработка схемы компетенций для использования в Word-отчётах.
        """
        processed_schema = []
        for competence in schema_data:
            processed_disciplines = []
            
            for disc in competence.get('discipline_list', []):
                # Создаём словарь для 8 семестров
                semester_data = {f'semester_{i}': '' for i in range(1, 9)}

                for sd in disc.get('semester_data', []):
                    semester_num = sd.get('semester')
                    if 1 <= semester_num <= 8:
                        form_control = sd.get('form_control', [])
                        semester_data[f'semester_{semester_num}'] = cls.format_form_control(form_control)
                
                processed_disciplines.append({
                    'discipline_index': disc.get('discipline_index', ''),
                    'discipline_name': disc.get('discipline_name', ''),
                    **semester_data
                })
            
            processed_schema.append({
                'competence_index': competence.get('competence_index', ''),
                'competence': competence.get('competence', ''),
                'discipline_list': processed_disciplines
            })
        
        return processed_schema
    
    @staticmethod
    def format_form_control(form_control_list):
        """Преобразует список форм аттестации в строку для Word"""
        form_mapping = {
            'zach': '*(З)',
            'ekz': '*(Э)',
            'kp': '*(КП)',
            'zacho': '*(Зо)'
        }
        
        return '\n'.join(form_mapping.get(fc, '') for fc in form_control_list)
    
    @classmethod
    def get_passport_report(cls, plan_id):
        """Экспорт паспорта компетенций в Word"""
        data = cls.get_competence_passport_data(plan_id)
        admission_info = data['admission_info']
        
        processed_schema = cls.process_schema_for_report(data['schema'])

        schema_map = {
            item['competence_index']: item['discipline_list']
            for item in processed_schema
        }

        processed_passport = []
        for item in data['passport']:
            # Фрагмент схемы
            schema_fragment = schema_map.get(item['competence_index'], [])
            
            # Распределение индикаторов
            indicator_distribution = cls.prepare_indicator_distribution(
                item.get('indicator_list', [])
            )
            
            processed_passport.append({
                'competence_index': item['competence_index'],
                'competence': item['competence'],
                'competence_relations': item.get('competence_relations', ''),
                'competence_final_indicator': item.get('competence_final_indicator', ''),
                'indicator_list': item.get('indicator_list', []),
                'schema_fragment': schema_fragment,
                'indicator_distribution': indicator_distribution
            })
        
        context = {
            'passport': processed_passport,
            'direction_code': admission_info.get('cdirection__cod', ''),
            'direction': admission_info.get('cdirection__name', ''),
            'spec_name': admission_info.get('spec_name', ''),
            'kvalif': admission_info.get('kvalif_name', ''),
            'fob': admission_info.get('cfob__name', ''),
            'year_post': str(admission_info.get('yr', '')),
            'protocol_year': str(admission_info.get('yr', ''))
        }
        
        template_path = f'{BASE_DIR}{Path("/templates/docxRPD/passport.docx")}'
        doc = DocxTemplate(template_path)
        doc.render(context)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer.getvalue()

    @staticmethod
    def prepare_indicator_distribution(indicator_list):
        """Подготовка данных для таблицы распределения индикаторов"""
        def extract_numeric_part(indicator_index):
            match = re.search(r'[\d]+(?:\.[\d]+)*$', indicator_index.strip())
            return match.group(0) if match else indicator_index

        # Собираем все уникальные числовые части индексов
        numeric_parts = set()
        for ind in indicator_list:
            numeric_parts.add(extract_numeric_part(ind['indicator_index']))
        
        # Сортируем
        def sort_key(x):
            nums = [int(n) for n in x.split('.') if n.isdigit()]
            return tuple(nums)
        
        sorted_headers = sorted(numeric_parts, key=sort_key)

        # Группируем индикаторы по дисциплинам
        discipline_map = {}
        for ind in indicator_list:
            disc_key = f"{ind['discipline_index']} {ind['discipline_name']}"
            if disc_key not in discipline_map:
                discipline_map[disc_key] = set()
            discipline_map[disc_key].add(extract_numeric_part(ind['indicator_index']))

        # Формируем список дисциплин с готовыми строками X/пусто
        disciplines = []
        for disc_key in sorted(discipline_map.keys()):
            parts = disc_key.split(' ', 1)
            discipline_index = parts[0]
            discipline_name = parts[1] if len(parts) > 1 else ''
            
            # Создаём список значений для каждого заголовка
            row_values = []
            for header in sorted_headers:
                row_values.append("X" if header in discipline_map[disc_key] else "")
            
            disciplines.append({
                'discipline_index': discipline_index,
                'discipline_name': discipline_name,
                'indicator_row': row_values 
            })

        return {
            'disciplines': disciplines,
            'indicator_headers': sorted_headers
        }