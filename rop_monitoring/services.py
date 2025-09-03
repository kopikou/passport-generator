import os
from datetime import datetime
from io import BytesIO

import pandas as pd
import pendulum
from django.conf import settings
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from app.utils import Mira, SOP
from rop_monitoring.models import Indicators, MiraAdmissionKinds, AdmissionKinds, Indicator
from rop_monitoring.sql_queries import MARKS_QUERY, STUDENTS_QUERY, ORDERS_QUERY, ADMISSIONS_QUERY
from openpyxl import Workbook
from openpyxl.styles import Font


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_monitoring_scores(monitoring_id):
    monitor = RopMonitor()
    admissions = monitor.get_admissions()

    calculator = IndicatorsCalculator()

    rop_monitoring_scores = []
    for admission_id, admission in admissions.items():
        admission_kind = None
        is_new_admission = False

        if admission.get('admission_kind') in [MiraAdmissionKinds.BACH.value, MiraAdmissionKinds.SPEC.value]:
            if is_new_admission:
                admission_kind = AdmissionKinds.NEW_BACH_SPEC.value
            else:
                admission_kind = AdmissionKinds.BACH_SPEC.value
        elif admission.get('admission_kind') in [MiraAdmissionKinds.MAG.value]:
            if is_new_admission:
                admission_kind = AdmissionKinds.NEW_MAG.value
            else:
                admission_kind = AdmissionKinds.MAG.value

        if admission_kind is not None:
            indicators = list(Indicator.objects.filter(admission_kinds__overlap=[admission_kind]).values())

            for indicator in indicators:
                value, score = calculator.get_indicator_value_score(admission_id, indicator['id'])

                if value is not None and score is not None:
                    value_numeric = None
                    value_boolean = None

                    if isinstance(value, bool):
                        value_boolean = value
                    elif isinstance(value, (int, float)):
                        value_numeric = float(value)

                    rop_monitoring_scores.append({
                        "rop_monitoring": monitoring_id,
                        "admission": admission_id,
                        "admission_name": admission.get('admission_name'),
                        "admission_kind": admission.get('admission_kind'),
                        "person_id": admission.get('admission_rop_id'),
                        "person_name": admission.get('admission_rop'),
                        "indicator_id": indicator['id'],
                        "value": value,
                        "value_boolean": value_boolean,
                        "value_numeric": value_numeric,
                        "score": score,
                    })

    return rop_monitoring_scores


def export_answers_to_excel(admissions):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Результаты"

    headers = [
        "Название программы",
        "РОП",
        "Ср. балл ЕГЭ (ДВИ)",
        "Баллы за ср. балл ЕГЭ",
        "Доля завершивших/активных студентов",
        "Баллы за долю завершивших/активных студентов",
        "Доля завершивших/активных студентов целевиков",
        "Баллы за долю завершивших/активных студентов целевиков",
        "Доля НПР, принявших участие в опросах о кач-ве образ.",
        "Баллы за долю НПР, принявших участие в опросах о кач-ве образ.",
        "Доля обучающихся, принявших участие в опросах о кач-ве образ.",
        "Баллы за долю обучающихся, принявших участие в опросах о кач-ве образ."
    ]

    sheet.append(headers)

    bold_font = Font(bold=True)
    for cell in sheet["1:1"]:
        cell.font = bold_font

    for admission in admissions:
        row = [
            admission.get('admission_name', ''),
            admission.get('person_name', ''),
            admission.get('ege_value', 0.0),
            admission.get('ege_score', 0.0),
            admission.get('student_contingent_value', 0.0),
            admission.get('student_contingent_score', 0.0),
            admission.get('celev_student_contingent_value', 0.0),
            admission.get('celev_student_contingent_score', 0.0),
            admission.get('npr_value', 0.0),
            admission.get('npr_score', 0.0),
            admission.get('student_sop_value', 0.0),
            admission.get('student_sop_score', 0.0)
        ]
        sheet.append(row)

    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column_letter].width = adjusted_width

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    filename = escape_uri_path(pendulum.today().format("DD.MM.YYYY"))
    response = StreamingHttpResponse(
        streaming_content=buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    response["Content-Encoding"] = 'UTF-8'

    return response


class IndicatorsCalculator:
    def __init__(self):
        self.monitor = RopMonitor()
        self.admissions = None
        self.ege_indicator = None
        self.student_contingent_indicator = None
        self.celev_student_contingent_indicator = None
        self.npr_indicator = None
        self.stud_sop_indicator = None
        self.employer_indicator = None

    def get_indicator_value_score(self, admission_id, indicator_id):
        match indicator_id:
            case Indicators.EGE.value:
                indicator_data = self.get_ege_indicator(admission_id)
            case Indicators.STUD_CONTINGENT.value:
                indicator_data = self.get_student_contingent_indicator(admission_id)
            case Indicators.CELEV_STUD_CONTINGENT.value:
                indicator_data = self.get_celev_student_contingent_indicator(admission_id)
            case Indicators.NPR.value:
                indicator_data = self.get_npr_indicator(admission_id)
            case Indicators.STUD_SOP.value:
                indicator_data = self.get_stud_sop_indicator(admission_id)
            case _:
                indicator_data = {
                    'value': None,
                    'score': None,
                }

        return indicator_data.get('value'), indicator_data.get('score')

    def get_ege_indicator(self, admission_id):
        if not self.ege_indicator:
            self.ege_indicator = self.monitor.get_ege_indicator()
        indicator = self.ege_indicator.get(admission_id, {})

        return indicator

    def get_student_contingent_indicator(self, admission_id):
        if not self.student_contingent_indicator:
            self.student_contingent_indicator = self.monitor.get_student_contingent_indicator()
        indicator = self.student_contingent_indicator.get(admission_id, {})

        return indicator

    def get_celev_student_contingent_indicator(self, admission_id):
        if not self.celev_student_contingent_indicator:
            self.celev_student_contingent_indicator = self.monitor.get_celev_student_contingent_indicator()
        indicator = self.celev_student_contingent_indicator.get(admission_id, {})

        return indicator

    def get_npr_indicator(self, admission_id):
        if not self.npr_indicator:
            self.npr_indicator = self.monitor.get_npr_indicator()
        indicator = self.npr_indicator.get(admission_id, {})

        return indicator

    def get_stud_sop_indicator(self, admission_id):
        if not self.stud_sop_indicator:
            self.stud_sop_indicator = self.monitor.get_stud_sop_indicator()
        indicator = self.stud_sop_indicator.get(admission_id, {})

        return indicator


class RopMonitor:
    def __init__(self) -> None:
        super().__init__()
        self.admissions = {}
        self.admissions_with_dvi = ['07.03.01', '07.03.02', '07.03.03', '29.03.04', '38.05.02', '42.03.02', '54.03.01',
                                    '54.05.01']
        self.marks = self.get_marks()
        self.students = self.get_students()
        self.student_states = {
            'active': [1, 10, 21],
            'fired': [13, 16, 27, 32],
            'finished': [12, 31],
            'academ': [5, 34]
        }
        self.celev_set = 2

    def get_current_course(self, admission_year):
        current_year = datetime.now().year
        course = current_year - admission_year + 1
        if course < 1:
            course = 1
        return course

    def get_ratio_score(self, admission_period, course_year, actual_students_ratio, is_for_celev):
        if is_for_celev:
            table = {
                4: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.40, 0.60),
                },
                4.5: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.50, 0.65),
                    5: (0.40, 0.60),
                },
                5: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.50, 0.65),
                    5: (0.40, 0.60),
                },
                5.5: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.50, 0.65),
                    5: (0.40, 0.60),
                    6: (0.40, 0.60),
                },
                6: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.50, 0.65),
                    5: (0.40, 0.60),
                    6: (0.40, 0.60),
                },
                6.5: {
                    1: (0.85, 0.90),
                    2: (0.70, 0.80),
                    3: (0.60, 0.70),
                    4: (0.50, 0.65),
                    5: (0.40, 0.60),
                    6: (0.40, 0.60),
                    7: (0.40, 0.60),
                }
            }
        else:
            table = {
                4: {
                    1: (0.90, 0.95),
                    2: (0.80, 0.90),
                    3: (0.70, 0.85),
                    4: (0.55, 0.75),
                },
                4.5: {
                    1: (0.90, 0.95),
                    2: (0.80, 0.90),
                    3: (0.70, 0.85),
                    4: (0.60, 0.80),
                    5: (0.55, 0.75),
                },
                5.5: {
                    1: (0.90, 0.95),
                    2: (0.80, 0.90),
                    3: (0.70, 0.85),
                    4: (0.60, 0.80),
                    5: (0.55, 0.75),
                    6: (0.55, 0.75),
                },
                6.5: {
                    1: (0.90, 0.95),
                    2: (0.80, 0.90),
                    3: (0.70, 0.85),
                    4: (0.60, 0.80),
                    5: (0.55, 0.75),
                    6: (0.55, 0.75),
                    7: (0.55, 0.75),
                }
            }

        if admission_period not in table:
            return 0

        course_thresholds = table[admission_period]

        if course_year not in course_thresholds:
            return 0

        if is_for_celev:
            min_for_1, min_for_2 = course_thresholds[course_year]

            if actual_students_ratio >= min_for_2:
                return 2
            elif actual_students_ratio >= min_for_1:
                return 1
            else:
                return 0
        else:
            min_for_2, min_for_4 = course_thresholds[course_year]

            if actual_students_ratio >= min_for_4:
                return 4
            elif actual_students_ratio >= min_for_2:
                return 2
            else:
                return 0

    def get_marks(self):
        marks = Mira.fetch(MARKS_QUERY, [])

        marks_by_student_id = {}
        for mark in marks:
            student_id = mark["student_id"]
            if student_id not in marks_by_student_id:
                marks_by_student_id[student_id] = []
            marks_by_student_id[student_id].append(mark)

        return marks_by_student_id

    def get_students(self):
        students = Mira.fetch(STUDENTS_QUERY, [])

        orders = Mira.fetch(ORDERS_QUERY, [])

        admissions = Mira.fetch(ADMISSIONS_QUERY, [])

        admissions_by_id = {int(ca['admission_id']): ca for ca in admissions}
        self.admissions = admissions_by_id

        filtered_orders = [
            order for order in orders
            if safe_int(order['admission_id']) in admissions_by_id and order['order_date'] is not None
        ]
        orders_by_student_id = {}
        for order in filtered_orders:
            student_id = order["student_id"]
            if student_id not in orders_by_student_id:
                orders_by_student_id[student_id] = []
            orders_by_student_id[student_id].append(order)

        students_by_id = {}
        for student in students:
            student_id = student["student_id"]
            student["admissions_history"] = []

            student_orders = orders_by_student_id.get(student_id, [])

            for order in student_orders:
                if order['comment'].lower() == "набор":
                    admission_id = safe_int(order["admission_id"])
                    admission_info = admissions_by_id.get(admission_id)
                    if admission_info:
                        if (not any(admission['admission_id'] == admission_info['admission_id']
                                    for admission in student['admissions_history'])):
                            admission_info['order_date'] = order['order_date']
                            student["admissions_history"].append(admission_info)

            admissions = student.get('admissions_history', [])
            if admissions:
                first_admission = admissions[0]
            else:
                first_admission = student
            student['first_admission'] = {
                'admission_id': first_admission['admission_id'],
                'admission_name': first_admission['admission_name'],
                'admission_abbr': first_admission['admission_abbr'],
                'admission_year': first_admission['admission_year'],
                'admission_date_end': first_admission['admission_date_end'],
                'admission_rop': first_admission['admission_rop'],
                'admission_rop_id': first_admission['admission_rop_id'],
            }
            if student_id not in students_by_id:
                students_by_id[student_id] = student

        return students_by_id

    def filter_marks(self, students_with_marks: dict):
        dvi_direction_specifications = {
            '07.03.01': {'t': 2, 'f': 2},
            '07.03.02': {'t': 2, 'f': 2},
            '07.03.03': {'t': 2, 'f': 2},
            '29.03.04': {'t': 2, 'f': 1},
            '38.05.02': {'t': 2, 'f': 1},
            '42.03.02': {'t': 2, 'f': 1},
            '54.03.01': {'t': 2, 'f': 2},
            '54.05.01': {'t': 2, 'f': 2}
        }

        for student in students_with_marks.values():
            direction_code = student['direction_code']
            specifications = dvi_direction_specifications.get(direction_code, {'t': 3, 'f': 0})
            student['max_ege'] = specifications['t']
            student['max_dvi'] = specifications['f']

            student['marks'] = {
                'is_ege': sorted(
                    [mark for mark in student['marks'] if mark['is_ege'] == 't'],
                    key=lambda x: x['mark'],
                    reverse=True
                )[:specifications['t']],
                'is_dvi': sorted(
                    [mark for mark in student['marks'] if mark['is_ege'] == 'f'],
                    key=lambda x: x['mark'],
                    reverse=True
                )[:specifications['f']]
            }

            if (len(student['marks']['is_ege']) + len(student['marks']['is_dvi']) < student['max_ege'] +
                    student['max_dvi']):
                student['marks'] = {
                    'is_ege': [],
                    'is_dvi': []
                }

    def get_ege_indicator(self):
        students_with_marks = {}
        for student in self.students.values():
            student_id = student['student_id']
            if student_id not in students_with_marks and student_id in self.marks:
                students_with_marks[student_id] = student
                students_with_marks[student_id]['marks'] = self.marks[student_id]
                if (len(students_with_marks[student_id]['admissions_history']) > 0 and
                        students_with_marks[student_id]['admission_id'] !=
                        students_with_marks[student_id]['admissions_history'][0]['admission_id']):
                    students_with_marks[student_id]['admission_id'] = \
                        students_with_marks[student_id]['admissions_history'][0]['admission_id']

                    students_with_marks[student_id]['admission_name'] = \
                        students_with_marks[student_id]['admissions_history'][0]['admission_name']

                    students_with_marks[student_id]['admission_date_end'] = \
                        students_with_marks[student_id]['admissions_history'][0]['admission_date_end']

                    students_with_marks[student_id]['admission_year'] = \
                        students_with_marks[student_id]['admissions_history'][0]['admission_year']

                    students_with_marks[student_id]['that_year_student'] = 1 if students_with_marks[student_id][
                                                                                    'student_admission_year'] == \
                                                                                students_with_marks[student_id][
                                                                                    'admission_year'] else 0

        self.filter_marks(students_with_marks)

        students_with_marks = [student for student in students_with_marks.values()
                               if (len(student['marks']['is_ege']) > 0
                                   or len(student['marks']['is_dvi']) > 0)
                               and student['that_year_student'] == 1]

        admissions = {}
        for student in students_with_marks:
            admission_id = student['admission_id']
            if admission_id not in admissions:
                admissions[admission_id] = {
                    'admission_id': admission_id,
                    'admission_name': student['admission_name'],
                    'admission_rop': student['admission_rop'],
                    'admission_year': student['admission_year'],
                    'faculty_name': student['faculty_name'],
                    'direction_name': student['direction_name'],
                    'admission_date_end': student['admission_date_end'],
                    'count_all_students': 0,
                    'count_budget_students': 0,
                    'count_commercial_students': 0,
                    'count_ege_subjects': student['max_ege'],
                    'ege_marks_sum': 0,
                    'budget_ege_marks_sum': 0,
                    'commercial_ege_marks_sum': 0,
                    'count_dvi_subjects': student['max_dvi'],
                    'dvi_marks_sum': 0,
                    'budget_dvi_marks_sum': 0,
                    'commercial_dvi_marks_sum': 0,
                    'count_ege_students': 0,
                    'count_dvi_students': 0,
                }

            if student['marks']['is_ege'] or student['marks']['is_dvi']:
                admissions[admission_id]['count_all_students'] += 1
                if student['student_set_name'] == 'b':
                    admissions[admission_id]['count_budget_students'] += 1
                    budget = True
                elif student['student_set_name'] == 'c':
                    admissions[admission_id]['count_commercial_students'] += 1
                    budget = False
                else:
                    budget = None

                if student['marks']['is_ege']:
                    admissions[admission_id]['count_ege_students'] += 1
                    for mark in student['marks']['is_ege']:
                        admissions[admission_id]['ege_marks_sum'] += mark['mark']
                        if budget is True:
                            admissions[admission_id]['budget_ege_marks_sum'] += mark['mark']
                        elif budget is False:
                            admissions[admission_id]['commercial_ege_marks_sum'] += mark['mark']

                if student['marks']['is_dvi']:
                    admissions[admission_id]['count_dvi_students'] += 1
                    for mark in student['marks']['is_dvi']:
                        admissions[admission_id]['dvi_marks_sum'] += mark['mark']
                        if budget is True:
                            admissions[admission_id]['budget_dvi_marks_sum'] += mark['mark']
                        elif budget is False:
                            admissions[admission_id]['commercial_dvi_marks_sum'] += mark['mark']

        admission_rows_by_id = {}
        for admission in admissions.values():
            admission['avg_ege_marks'] = int(
                admission['ege_marks_sum'] /
                (admission['count_ege_students'] * admission['count_ege_subjects'])
            ) if (admission['count_ege_students'] * admission['count_ege_subjects']) > 0 else 0

            admission['avg_dvi_marks'] = int(
                admission['dvi_marks_sum'] /
                (admission['count_dvi_students'] * admission['count_dvi_subjects'])
            ) if (admission['count_dvi_students'] * admission['count_dvi_subjects']) > 0 else 0

            admission['avg_marks'] = 0
            if admission['avg_ege_marks'] > 0 and admission['avg_dvi_marks'] > 0:
                admission['avg_marks'] = int((admission['avg_ege_marks'] + admission['avg_dvi_marks']) / 2)
            elif admission['avg_ege_marks'] > 0 and admission['avg_dvi_marks'] == 0:
                admission['avg_marks'] = admission['avg_ege_marks']
            elif admission['avg_ege_marks'] == 0 and admission['avg_dvi_marks'] > 0:
                admission['avg_marks'] = admission['avg_dvi_marks']

            current_date = pendulum.now().timestamp()
            str_admission_date_end = str(admission['admission_date_end'])
            admission_date_end = pendulum.from_format(str_admission_date_end, 'DD.MM.YYYY').timestamp()
            admission['admission_finished'] = '+' if current_date > admission_date_end else '−'

            avg = admission['avg_marks']
            if avg <= 65:
                score = 0
            elif 66 <= avg <= 69:
                score = 1
            elif avg >= 70:
                score = 2
            else:
                score = 0

            admission_rows_by_id[admission['admission_id']] = {
                'admission_name': admission['admission_name'],
                'admission_rop': admission['admission_rop'],
                'value': admission['avg_marks'],
                'score': score,
            }

        return admission_rows_by_id

    def get_student_contingent_indicator(self):
        current_date = pendulum.now()
        admissions = {}
        for admission in self.admissions.values():
            admission_id = admission['admission_id']
            if admission_id not in admissions:
                date_end = pendulum.from_format(admission['admission_date_end'], "DD.MM.YYYY")
                admissions[admission_id] = {
                    'admission_id': admission_id,
                    'admission_name': admission['admission_name'],
                    'admission_rop': admission['admission_rop'],
                    'admission_abbr': admission['admission_abbr'],
                    'admission_year': admission['admission_year'],
                    'admission_period': admission['admission_period'],
                    'faculty_name': admission['faculty_name'],
                    'direction_name': admission['direction_name'],
                    'admission_date_end': admission['admission_date_end'],
                    'admission_finished': date_end <= current_date,
                    'admitted_students': [],
                    'went_to_academ_students': [],
                    'went_to_other_group_students': [],
                    'fired_students': [],
                    'came_from_academ_students': [],
                    'restored_or_new_students': [],
                    'active_students': [],
                    'finished_students': [],
                }

        for student in self.students.values():
            first_admission_id = student['first_admission']['admission_id']
            actual_admission_id = student['admission_id']
            student_state = student.get('student_state', -1)

            if first_admission_id in admissions:
                admissions[first_admission_id]['admitted_students'].append(student)

            if actual_admission_id in admissions:
                if student_state in self.student_states['active']:
                    admissions[actual_admission_id]['active_students'].append(student)
                elif student_state in self.student_states['finished']:
                    admissions[actual_admission_id]['finished_students'].append(student)
                elif student_state in self.student_states['academ']:
                    admissions[actual_admission_id]['went_to_academ_students'].append(student)
                elif student_state in self.student_states['fired']:
                    admissions[actual_admission_id]['fired_students'].append(student)

        for admission in admissions.values():
            for student in admission['admitted_students']:
                if student not in admission['active_students'] + admission['finished_students']:
                    if student['admission_id'] == admission['admission_id']:
                        if (student['student_state'] in self.student_states['academ']
                                and student not in admission['went_to_academ_students']):
                            admission['went_to_academ_students'].append(student)
                            continue
                        if (student['student_state'] in self.student_states['fired']
                                and student not in admission['fired_students']):
                            admission['fired_students'].append(student)
                            continue

                    if student['admission_id'] != admission['admission_id']:
                        if student['admission_abbr'] != admission['admission_abbr']:
                            admission['went_to_other_group_students'].append(student)
                            continue
                        if (student['admission_abbr'] == admission['admission_abbr']
                                and student['admission_year'] != admission['admission_year']):
                            admission['went_to_academ_students'].append(student)
                            continue

            for student in admission['active_students'] + admission['finished_students'] + admission['fired_students'] \
                           + admission['went_to_academ_students']:
                if student not in admission['admitted_students']:
                    if student['first_admission']['admission_abbr'] != admission['admission_abbr']:
                        admission['restored_or_new_students'].append(student)
                        continue
                    if (student['first_admission']['admission_abbr'] == admission['admission_abbr']
                            and student['first_admission']['admission_year'] != admission['admission_year']):
                        admission['came_from_academ_students'].append(student)
                        continue
        admission_rows_by_id = {}

        admissions = sorted(admissions.values(), key=lambda d: d['admission_name'])
        for admission in admissions:
            if len(admission['admitted_students']) > 0:
                denominator = (
                        len(admission['admitted_students']) -
                        (len(admission['went_to_other_group_students']) + len(admission['went_to_academ_students'])) +
                        (len(admission['came_from_academ_students']) + len(admission['restored_or_new_students']))
                )

                numerator = len(admission['active_students']) + len(admission['finished_students'])

                if denominator == 0:
                    contingent_students_ratio = 0
                else:
                    contingent_students_ratio = round(numerator / denominator, 2)

                course_year = self.get_current_course(admission["admission_year"])

                score = self.get_ratio_score(admission["admission_period"], course_year, contingent_students_ratio,
                                             False)

                admission_rows_by_id[admission['admission_id']] = {
                    'admission_name': admission['admission_name'],
                    'admission_rop': admission['admission_rop'],
                    'value': contingent_students_ratio,
                    'score': score,
                }
        return admission_rows_by_id

    def get_celev_student_contingent_indicator(self):
        current_date = pendulum.now()
        admissions = {}
        for admission in self.admissions.values():
            admission_id = admission['admission_id']
            if admission_id not in admissions:
                date_end = pendulum.from_format(admission['admission_date_end'], "DD.MM.YYYY")
                admissions[admission_id] = {
                    'admission_id': admission_id,
                    'admission_name': admission['admission_name'],
                    'admission_abbr': admission['admission_abbr'],
                    'admission_rop': admission['admission_rop'],
                    'admission_year': admission['admission_year'],
                    'admission_period': admission['admission_period'],
                    'faculty_name': admission['faculty_name'],
                    'direction_name': admission['direction_name'],
                    'admission_date_end': admission['admission_date_end'],
                    'admission_finished': date_end <= current_date,
                    'admitted_students': [],
                    'all_celev_students': [],
                    'admitted_celev_students': [],
                    'dogs_celev_students': [],
                    'all_disappeared_celev_students': [],
                    'went_to_academ_students': [],
                    'academ_celev_students': [],
                    'moved_celev_students': [],
                    'fired_students': [],
                    'fired_celev_students': [],
                    'closed_celev_dog_students': [],
                    'restored_or_new_students': [],
                    'restored_or_new_celev_students': [],
                    'went_to_other_group_students': [],
                    'came_from_academ_students': [],
                    'came_from_academ_celev_students': [],
                    'active_students': [],
                    'active_celev_students': [],
                    'finished_students': [],
                    'finished_celev_students': [],
                }

        for student in self.students.values():
            first_admission_id = student['first_admission']['admission_id']
            actual_admission_id = student['admission_id']
            student_state = student.get('student_state', -1)
            student_dog = student['student_dog_cel']
            student_dog_in_edu = student['student_dog_in_edu']
            student_dog_state = student['student_dog_state']
            active_student_dog = student_dog_state != 3
            inactive_student_dog = student_dog_state == 3

            if first_admission_id in admissions:
                admissions[first_admission_id]['admitted_students'].append(student)

                if student_dog:
                    if student_dog_in_edu == 'f':
                        admissions[first_admission_id]['admitted_celev_students'].append(student)
                    elif student_dog_in_edu == 't':
                        admissions[first_admission_id]['dogs_celev_students'].append(student)
                    if inactive_student_dog and student not in admissions[first_admission_id][
                        'closed_celev_dog_students']:
                        admissions[first_admission_id]['closed_celev_dog_students'].append(student)

            if actual_admission_id in admissions:
                if (student_dog and student not in admissions[actual_admission_id]['admitted_celev_students']
                        and student not in admissions[actual_admission_id]['dogs_celev_students']):
                    if student_dog_in_edu == 'f':
                        admissions[actual_admission_id]['admitted_celev_students'].append(student)
                    elif student_dog_in_edu == 't':
                        admissions[actual_admission_id]['dogs_celev_students'].append(student)

                    if inactive_student_dog and student not in admissions[actual_admission_id][
                        'closed_celev_dog_students']:
                        admissions[actual_admission_id]['closed_celev_dog_students'].append(student)

                if student_state in self.student_states['active']:
                    admissions[actual_admission_id]['active_students'].append(student)
                    if student_dog and active_student_dog:
                        admissions[actual_admission_id]['active_celev_students'].append(student)

                elif student_state in self.student_states['finished']:
                    admissions[actual_admission_id]['finished_students'].append(student)
                    if student_dog and active_student_dog:
                        admissions[actual_admission_id]['finished_celev_students'].append(student)

                elif student_state in self.student_states['academ']:
                    admissions[actual_admission_id]['went_to_academ_students'].append(student)
                    if student_dog and active_student_dog:
                        admissions[actual_admission_id]['academ_celev_students'].append(student)

                elif student_state in self.student_states['fired']:
                    if student_dog and active_student_dog:
                        admissions[actual_admission_id]['fired_celev_students'].append(student)
                    admissions[actual_admission_id]['fired_students'].append(student)

        for admission in admissions.values():
            admission['all_celev_students'] = admission['admitted_celev_students'] + admission['dogs_celev_students']

            for student in admission['admitted_students']:
                student_dog = student['student_dog_cel']
                student_dog_state = student['student_dog_state']
                active_student_dog = student_dog_state != 3
                inactive_student_dog = student_dog_state == 3

                if inactive_student_dog and student not in admission['closed_celev_dog_students']:
                    admission['closed_celev_dog_students'].append(student)

                if student not in admission['active_students'] + admission['finished_students']:
                    if student['admission_id'] == admission['admission_id']:
                        if student['student_state'] in self.student_states['academ']:
                            if student not in admission['went_to_academ_students']:
                                admission['went_to_academ_students'].append(student)
                            if student_dog and active_student_dog and student not in admission['academ_celev_students']:
                                admission['academ_celev_students'].append(student)
                            continue

                        if student['student_state'] in self.student_states['fired']:
                            if student not in admission['fired_students']:
                                admission['fired_students'].append(student)
                            if student_dog and active_student_dog and student not in admission['fired_celev_students']:
                                admission['fired_celev_students'].append(student)
                            continue
                    else:
                        if student['admission_abbr'] != admission['admission_abbr']:
                            if student not in admission['went_to_other_group_students']:
                                admission['went_to_other_group_students'].append(student)
                            if student_dog and active_student_dog and student not in admission['moved_celev_students']:
                                admission['moved_celev_students'].append(student)
                            continue

                        else:
                            if student['admission_year'] != admission['admission_year']:
                                if student not in admission['went_to_academ_students']:
                                    admission['went_to_academ_students'].append(student)
                                if student_dog and active_student_dog and student not in admission[
                                    'academ_celev_students']:
                                    admission['academ_celev_students'].append(student)
                                continue

            for student in admission['active_students'] + admission['finished_students'] + admission['fired_students'] \
                           + admission['went_to_academ_students']:

                student_dog = student['student_dog_cel']
                student_dog_state = student['student_dog_state']
                active_student_dog = student_dog_state != 3
                inactive_student_dog = student_dog_state == 3

                if inactive_student_dog and student not in admission['closed_celev_dog_students']:
                    admission['closed_celev_dog_students'].append(student)

                if student not in admission['admitted_students']:
                    if student['first_admission']['admission_abbr'] != admission['admission_abbr']:
                        admission['restored_or_new_students'].append(student)

                        if student_dog and active_student_dog and student not in admission[
                            'restored_or_new_celev_students']:
                            admission['restored_or_new_celev_students'].append(student)

                        continue
                    if (student['first_admission']['admission_abbr'] == admission['admission_abbr']
                            and student['first_admission']['admission_year'] != admission['admission_year']):
                        admission['came_from_academ_students'].append(student)

                        if student_dog and active_student_dog and student not in admission[
                            'came_from_academ_celev_students']:
                            admission['came_from_academ_celev_students'].append(student)

                        continue

            admission['all_disappeared_celev_students'] = (admission['academ_celev_students'] +
                                                           admission['moved_celev_students'] +
                                                           admission['fired_celev_students'] +
                                                           admission['closed_celev_dog_students'])

        admission_rows_by_id = {}

        admissions = sorted(admissions.values(), key=lambda d: d['admission_name'])
        for admission in admissions:
            if len(admission['admitted_students']) > 0:
                celev_students_ratio = round(
                    (len(admission['active_celev_students']) + len(admission['finished_celev_students'])) /
                    (len(admission['all_celev_students']))
                    , 2) if len(admission['all_celev_students']) > 0 else 0

                course_year = self.get_current_course(admission["admission_year"])
                score = self.get_ratio_score(admission["admission_period"], course_year, celev_students_ratio, True)

                admission_rows_by_id[admission['admission_id']] = {
                    'admission_name': admission['admission_name'],
                    'admission_rop': admission['admission_rop'],
                    'value': celev_students_ratio,
                    'score': score,
                }
        return admission_rows_by_id

    def get_npr_indicator(self):
        person_cadmission = self.get_person_uchnagr('09/10/2024', '09/10/2025')
        # person_cadmission = Mira.fetch(NPR_QUERY, [])
        csv_path = os.path.join("templates", "prepod_who_go_survey_in_bitrix.csv")
        df = pd.read_csv(csv_path)
        data_dict = df.to_dict('records')

        admissions = {}
        for admission in self.admissions.values():
            admission_id = admission['admission_id']
            if admission_id not in admissions:
                admissions[admission_id] = {
                    'admission_id': admission_id,
                    'admission_name': admission['admission_name'],
                    'admission_rop': admission['admission_rop'],
                    'total_persons': set(),
                    'responded_persons': set(),
                }

        person_admission_map = {}
        for person in person_cadmission:
            mira_id = person['cperson']
            admission_id = person['cadmission']

            if mira_id not in person_admission_map:
                person_admission_map[mira_id] = set()
            person_admission_map[mira_id].add(admission_id)

            if admission_id in admissions:
                admissions[admission_id]['total_persons'].add(mira_id)

        responded_mira_ids = {row['mira_id'] for row in data_dict}

        for mira_id in responded_mira_ids:
            if mira_id in person_admission_map:
                for admission_id in person_admission_map[mira_id]:
                    if admission_id in admissions:
                        admissions[admission_id]['responded_persons'].add(mira_id)

        admission_rows_by_id = {}
        for admission in sorted(admissions.values(), key=lambda d: d['admission_name']):
            total = len(admission['total_persons'])
            responded = len(admission['responded_persons'])
            ratio = round(responded / total,2) if total > 0 else 0
            score = 1 if ratio >= 0.6 else 0
            admission_rows_by_id[admission['admission_id']] = {
                'admission_name': admission['admission_name'],
                'admission_rop': admission['admission_rop'],
                'value': ratio,
                'score': score,
            }

        return admission_rows_by_id

    def get_stud_sop_indicator(self):
        student_count_data = self.get_cadmission_student_count('01/01/2025', '07/01/2025')
        student_results_data = self.get_student_results_count(2025)
        student_count = {item['cnewgrup']: item['summa'] for item in student_count_data}
        student_result = {item['client_group']: item['summa'] for item in student_results_data}
        admissions_rows_by_id = {}
        for admission in self.admissions.values():
            admission_name = admission['admission_name']
            count = student_count.get(admission_name, 0)
            res = student_result.get(admission_name, 0)
            ratio = round(res / count, 2) if count > 0 else 0
            ratio = min(ratio, 1.0)
            score = 1 if ratio >= 0.6 else 0
            admissions_rows_by_id[admission['admission_id']] = {
                'admission_name': admission['admission_name'],
                'admission_rop': admission['admission_rop'],
                'value': ratio,
                'score': score,
            }
        return admissions_rows_by_id

    @classmethod
    def get_cadmission_student_count(cls, start_date, start_end):
        query = (f"""SELECT LEFT(lg1.cnewgrup, LEN(lg1.cnewgrup) - 2) AS cnewgrup,
    COUNT(DISTINCT CASE WHEN %s BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) +
    COUNT(DISTINCT CASE WHEN %s BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) AS summa
FROM dbo.[log$studgrup] lg1
LEFT JOIN dbo.[log$studgrup] lg2 ON lg1.cnewgrup = lg2.coldgrup AND lg1.cstud = lg2.cstud
LEFT JOIN dbo.catstud cs ON cs.id = lg1.cstud
WHERE lg1.cnewgrup IS NOT NULL AND lg1.cnewgrup <> ''
AND cs.cstudstate IN (1,5,6,10,11,12,13,15,20,24,31,32,33,34)
GROUP BY LEFT(lg1.cnewgrup, LEN(lg1.cnewgrup) - 2)
HAVING COUNT(DISTINCT CASE WHEN %s BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) +
    COUNT(DISTINCT CASE WHEN %s BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) > 0
            """)
        r = Mira.fetch(query, [start_date, start_end,start_date, start_end])
        return r

    @classmethod
    def get_student_results_count(cls, year):
        query = (f"""select cadmission, LEFT(client_group, LENGTH(client_group) - 2) AS client_group,
        (COUNT(DISTINCT CASE WHEN s.year = %s AND s.semestr = 2 THEN mira_id END)  +
        COUNT(DISTINCT CASE WHEN s.year = %s - 1 AND s.semestr = 1 THEN mira_id END)) as summa
 from sop_surveyresult
left join sop_surveydisciplineresult on sop_surveyresult.id = sop_surveydisciplineresult.survey_result_id
 left join sop_survey s on sop_surveyresult.survey_id = s.id
where survey_id in (select id from sop_survey where (year=%s and semestr=2) or (year=(select %s - 1) and semestr=1))
group by cadmission, LEFT(client_group, LENGTH(client_group) - 2)
                """)
        r = SOP.fetch(query, [year, year, year, year])
        return r

    @classmethod
    def get_person_uchnagr(cls, start_date, start_end):
        query = (f"""SELECT cadmission,cperson FROM dbo.person2uchnagr
    WHERE ddat BETWEEN %s AND %s
                """)
        r = Mira.fetch(query, [start_date, start_end])
        return r

    def get_admissions(self):
        return self.admissions
