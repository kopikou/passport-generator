from collections import defaultdict
from datetime import datetime

import pendulum

from app.utils import Mira
from rop_monitoring.sql_queries import MARKS_QUERY, STUDENTS_QUERY, ORDERS_QUERY, ADMISSIONS_QUERY


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


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
            if avg < 65:
                score = 0
            elif 66 <= avg <= 69:
                score = 1
            elif avg > 70:
                score = 2
            else:
                score = 0

            admission_rows_by_id[admission['admission_id']] = {
                'admission_name': admission['admission_name'],
                'admission_rop': admission['admission_rop'],
                'avg_marks': admission['avg_marks'],
                'avg_marks_score': score,
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
                contingent_students_ratio = round((len(admission['active_students']) + len(admission['finished_students'])) /
                                         (len(admission['admitted_students']) -
                                          (len(admission['went_to_other_group_students']) +
                                           len(admission['went_to_academ_students'])) +
                                          (len(admission['came_from_academ_students']) +
                                           len(admission['restored_or_new_students']))
                                          )
                                         , 2)

                course_year = self.get_current_course(admission["admission_year"])

                score = self.get_ratio_score(admission["admission_period"], course_year, contingent_students_ratio,False)

                admission_rows_by_id[admission['admission_id']] = {
                    'admission_name': admission['admission_name'],
                    'admission_rop': admission['admission_rop'],
                    'contingent_students_ratio': contingent_students_ratio,
                    'contingent_students_ratio_score': score,
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
                    'celev_students_ratio': celev_students_ratio,
                    'celev_students_ratio_score': score,
                }
        return admission_rows_by_id

    def get_admissions(self):
        return self.admissions
