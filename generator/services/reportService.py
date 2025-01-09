import os
from itertools import groupby
from pathlib import Path

import pendulum
from docxtpl import DocxTemplate

from app.settings import BASE_DIR
from arim.models import CatPerson


def get_tic_name(data):
    result = []

    if data['zach']:
        result.append('Зачет')
    if data['ekz']:
        result.append('Экзамен')
    if data['zacho']:
        result.append('Зачет с оценкой')
    if data['kp']:
        result.append('Курсовой проект')
    if data['kr']:
        result.append('Курсовая работа')

    return result


def get_work_hours(data, type):
    result = []

    for item in data:
        if item['type'] == type:
            result.append({
                "num": item['num'],
                "number": item['number'],
                "hours": int(item['hours']),
                "content": item['content'],
                "type": item['type'],
            })

    return result


class ReportService(object):

    @staticmethod
    def get_rpd_annotation(data):
        path = f"{BASE_DIR}{Path("/templates/docxRPD/annotation.docx")}"
        doc = DocxTemplate(path)

        competences_sorted = sorted(data['planlines']['indicators'], key=lambda item: item['competence_index'])
        competences_grouped = {key: list(items) for key, items in
                               groupby(competences_sorted, key=lambda item: item['competence_index'])}
        competence = []
        for key, item in competences_grouped.items():
            competence.append({
                "index": key,
                "content": item[0]['competence'],
            })

        discipline_themes = {key: item for key, item in enumerate(data['discipline_themes'], start=1)}

        discipline_goal = ''
        main_library = []
        for item in data['additional_info']:
            if item['type'] == 'disciplineGoal':
                discipline_goal = item['value']

            if item['type'] == 'library':
                for k, i in enumerate(item['value']['mainBook'], start=1):
                    main_library.append({
                        "number": k,
                        "bib_disc": i['bib_disc'],
                    })

        tic_all = []
        for item in data['planlines']['semesters']:
            tic_all.append(", ".join(get_tic_name(item)))

        context = {
            "disciplGoal": discipline_goal,
            "discpl": data['planlines']['dis'],
            "competences": competence,
            "discipline_themes": discipline_themes,
            "tic_all": ", ".join(tic_all),
            "main_library": main_library,
        }

        doc.render(context)
        return doc

    @staticmethod
    def get_rpd_report(data):
        path = f"{BASE_DIR}{Path("/templates/docxRPD/rpd.docx")}"
        doc = DocxTemplate(path)

        competences_sorted = sorted(data['planlines']['indicators'], key=lambda item: item['competence_index'])
        competences_grouped = {key: list(items) for key, items in
                               groupby(competences_sorted, key=lambda item: item['competence_index'])}
        competence = []
        for key, item in competences_grouped.items():
            competence.append({
                "index": key,
                "content": item[0]['competence'],
                "indicators": ", ".join([i['indicator_index'] for i in item]),
            })

        indicators = []
        for item in data['planlines']['indicators']:
            indicators.append({
                'index': item['indicator_index'],
                'content': item['indicator'],
                'know': item['discipline_indicator'][0]['know'] if item['discipline_indicator'] else '',
                'able': item['discipline_indicator'][0]['able'] if item['discipline_indicator'] else '',
                'own': item['discipline_indicator'][0]['own'] if item['discipline_indicator'] else '',
                'criteria': item['discipline_indicator'][0]['criteria'] if item['discipline_indicator'] else '',
                'methods': item['discipline_indicator'][0]['methods'] if item['discipline_indicator'] else '',
            })

        guidelines_titles = {
            'laboratory': 'Методические указания для обучающихся по лабораторным работам:',
            'practice': 'Методические указания для обучающихся по практическим занятиям',
            'independent': 'Методические указания для обучающихся по самостоятельной работе:',
            'course': 'Методические указания для обучающихся по курсовому проектированию/работе:',
        }

        tat_titles = {
            'ekz': 'Типовые оценочные средства для проведения экзамена по дисциплине',
            'zacho': 'Типовые оценочные средства для проведения дифференцированного зачета по дисциплине',
            'zach': 'Типовые оценочные средства для проведения зачета по дисциплине',
            'krkp': 'Типовые оценочные средства для курсовой работы/курсового проектирования по дисциплине',
        }

        additional_library = []
        main_library = []
        resources = []
        software = []
        logistics = []
        tat = []
        fos = []
        guidelines = []
        precedence = []
        subsequent = []
        interactive_methods = None
        for item in data['additional_info']:
            if item['type'] == 'interactiveMethods':
                interactive_methods = item['value']['interactiveMethods']

            if item['type'] == 'disciplinePlace':
                precedence = item['value']['precedence']
                subsequent = item['value']['subsequent']

            if item['type'] == 'guidelines':
                q = 0
                for k, i in item['value'][0].items():
                    q += 1
                    guidelines.append({
                        'number': q,
                        'type': k,
                        'title': guidelines_titles[k],
                        'content': i,
                    })

            if item['type'] == 'fos':
                q = 0
                for k, i in item['value'][0].items():
                    q += 1
                    fos.append({
                        'number': q,
                        'type': k,
                        'title': i['title'],
                        'about': i['about'] if 'about' in i else '',
                        'criteria': i['criteria'] if 'criteria' in i else '',
                    })

            if item['type'] == 'resources':
                resources = item['value']

            if item['type'] == 'library':
                for k, i in enumerate(item['value']['dopBook'], start=1):
                    additional_library.append({
                        "number": k,
                        "bib_disc": i['bib_disc'],
                    })

                for k, i in enumerate(item['value']['mainBook'], start=1):
                    main_library.append({
                        "number": k,
                        "bib_disc": i['bib_disc'],
                    })

            if item['type'] == 'software':
                for k, i in enumerate(item['value'], start=1):
                    if i['clicense__type']:
                        software.append({
                            'number': k,
                            'content': 'Свободно распространяемое программное обеспечение ' + i['clicense__name']
                            if i['clicense__type'] == 'Свободное'
                            else 'Лицензионное программное обеспечение ' + i['clicense__name'],
                        })
                    else:
                        software.append({
                            'number': k,
                            'content': i['clicense__name'],
                        })

            if item['type'] == 'logistics':
                for k, i in enumerate(item['value'], start=1):
                    logistics.append({
                        'number': k,
                        'name': i['name'],
                    })

            if item['type'] == 'tat':
                q = 0
                for k, i in item['value'][0].items():
                    q += 1
                    if k == 'zach':
                        tat.append({
                            'number': q,
                            'type': k,
                            'title': tat_titles[k],
                            'main': i['main'],
                            'about': i['about'],
                            'example': i['example'],
                            'passed': i['passed'],
                            'unpassed': i['unpassed'],
                        })
                    else:
                        tat.append({
                            'number': q,
                            'type': k,
                            'title': tat_titles[k],
                            'main': i['main'],
                            'about': i['about'],
                            'example': i['example'],
                            'great': i['great'],
                            'good': i['good'],
                            'satisfactorily': i['satisfactorily'],
                            'unsatisfactory': i['unsatisfactory'],
                        })

        other_disciplines = {item['disid']: item['dis'] for item in data['other_discipline']}
        precedence_names = ", ".join([f"«{other_disciplines[item]}»" for item in precedence])
        subsequent_names = ", ".join([f"«{other_disciplines[item]}»" for item in subsequent])

        tic_all = {}
        semester_hours = []
        semesters = []
        for item in data['planlines']['semesters']:
            tic_all[item['num']] = ", ".join(get_tic_name(item))
            semesters.append(item['num'])
            semester_hours.append({
                "num": item['num'],
                "aud_hours": sum([
                    item['lekc'] or 0,
                    item['lab'] or 0,
                    item['pr'] or 0,
                ]),
                "contact_hours": sum([
                    item['lekc'] or 0,
                    item['lab'] or 0,
                    item['pr'] or 0,
                    item['eios'] or 0,
                ]),
                "lekc_hours": item['lekc'] or 0,
                "lab_hours": item['lab'] or 0,
                "pr_hours": item['pr'] or 0,
                "srs_hours": item['srs'] or 0,
                "ekz_hours": item['ekzhour'] or 0,
                "eios_hours": item['eios'] or 0,
                "tic": tic_all[item['num']],
            })

        semester_hours_all = {
            "lekc_hours_all": sum([i['lekc'] for i in data['planlines']['semesters'] if i['lekc'] is not None]),
            "lab_hours_all": sum([i['lab'] for i in data['planlines']['semesters'] if i['lab'] is not None]),
            "pr_hours_all": sum([i['pr'] for i in data['planlines']['semesters'] if i['pr'] is not None]),
            "srs_hours_all": sum([i['srs'] for i in data['planlines']['semesters'] if i['srs'] is not None]),
            "ekz_hours_all": sum([i['ekzhour'] for i in data['planlines']['semesters'] if i['ekzhour'] is not None]),
            "eios_hours_all": sum([i['eios'] for i in data['planlines']['semesters'] if i['eios'] is not None]),
        }
        semester_hours_all.update({
            "aud_hours_all": sum([
                semester_hours_all['lekc_hours_all'] or 0,
                semester_hours_all['lab_hours_all'] or 0,
                semester_hours_all['pr_hours_all'] or 0,
            ]),
        })
        semester_hours_all.update({
            "contact_hours_all": sum([
                semester_hours_all['aud_hours_all'] or 0,
                semester_hours_all['eios_hours_all'] or 0,
            ]),
        })
        semester_hours_all.update({
            "tic_all": ", ".join(set([item for key, item in tic_all.items()])),
        })

        discipline_themes = {item['id']: item for item in data['discipline_themes']}
        discipline_sorted = sorted(data['discipline_themes'], key=lambda item: (item['semester'], item['num']))
        discipline_grouped = {key: list(item) for key, item in
                              groupby(discipline_sorted, key=lambda item: item['semester'])}

        work_hour = []
        for e, item in enumerate(data['discipline_work_hour']):
            work_hour.append({
                "num": item['semester'],
                "theme": discipline_themes[item['theme_id']]['name'],
                "formcontrol": discipline_themes[item['theme_id']]['formcontrol_verbose'],
                "type": item['type'],
                "content": item['name'],
                "hours": item['hours'],
                "number": item['num'],
                "tic": [s['ekz_hours'] for s in semester_hours if s['num'] == item['semester']],
                "tic_all": [s['tic'] for s in semester_hours if s['num'] == item['semester']]
            })
        work_hour_sorted = sorted(work_hour, key=lambda item: item['num'])
        wk = {key: list(items) for key, items in
              groupby(work_hour_sorted, key=lambda item: item['num'])}

        lab_work = get_work_hours(work_hour, 3)
        lab_work_sorted = sorted(lab_work, key=lambda item: (item['num'], item['number']))
        lab_work_grouped = {key: list(item) for key, item in groupby(lab_work_sorted, key=lambda item: item['num'])}

        pr_work = get_work_hours(work_hour, 1)
        pr_work_sorted = sorted(pr_work, key=lambda item: (item['num'], item['number']))
        pr_work_grouped = {key: list(item) for key, item in groupby(pr_work_sorted, key=lambda item: item['num'])}

        srs_work = get_work_hours(work_hour, 2)
        srs_work_sorted = sorted(srs_work, key=lambda item: (item['num'], item['content']))
        srs_work_grouped = {key: list(item) for key, item in groupby(srs_work_sorted, key=lambda item: item['num'])}

        srs_work_res = {}
        for key, items in srs_work_grouped.items():
            res_sorted = sorted(items, key=lambda i: i['content'])
            res_grouped = {k: list(i) for k, i in groupby(res_sorted, key=lambda item: item['content'])}

            tmp = []
            v = 1
            for k, i in res_grouped.items():
                tmp.append({
                    "content": k,
                    "number": v,
                    "hours": sum([q['hours'] for q in i]),
                })
                v += 1

            srs_work_res[key] = tmp

        for key, items in wk.items():
            items_sorted = sorted(items, key=lambda q: q['theme'])
            items_grouped = {k: list(i) for k, i in groupby(items_sorted, key=lambda q: q['theme'])}
            q = 0
            tmp_arr = []
            for k, i in items_grouped.items():
                q += 1
                i_sorted = sorted(i, key=lambda val: val['type'])
                i_grouped = {v: list(val) for v, val in groupby(i_sorted, key=lambda val: val['type'])},
                tmp_arr.append({
                    "index": (k, q),
                    "lec": int(sum([s['hours'] for s in i if s['type'] == 0])) or '',
                    "lec_nums": ", ".join([str(s['number']) for s in i if s['type'] == 0]),
                    "labs": int(sum([s['hours'] for s in i if s['type'] == 3])) or '',
                    "labs_nums": ", ".join([str(s['number']) for s in i if s['type'] == 3]),
                    "pr": int(sum([s['hours'] for s in i if s['type'] == 1])) or '',
                    "pr_nums": ", ".join([str(s['number']) for s in i if s['type'] == 1]),
                    "srs": int(sum([s['hours'] for s in i if s['type'] == 2])) or '',
                    "srs_nums": ", ".join([str(s['number']) for s in i if s['type'] == 2]),
                    "formcontrol": i[0]['formcontrol'],
                    "tic": i[0]['tic'][0] or '',
                    "tic_all": ", ".join(i[0]['tic_all']),
                })
            tmp_arr.append({
                "index": ("Промежуточная аттестация", ''),
                "lec": '',
                "lec_nums": '',
                "labs": '',
                "labs_nums": '',
                "pr": '',
                "pr_nums": '',
                "srs": i[0]['tic'][0] or '',
                "srs_nums": '',
                "formcontrol": ", ".join(i[0]['tic_all']),
            })
            tmp_arr.append({
                "index": ("Всего", ''),
                "lec": sum([int(i['lec']) for i in tmp_arr if i['lec']]) or '',
                "lec_nums": '',
                "labs": sum([int(i['labs']) for i in tmp_arr if i['labs']]) or '',
                "labs_nums": '',
                "pr": sum([int(i['pr']) for i in tmp_arr if i['pr']]) or '',
                "pr_nums": '',
                "srs": sum([int(i['srs']) for i in tmp_arr if i['srs']]) or '',
                "srs_nums": '',
                "formcontrol": '',
            })
            wk[key] = {i['index']: i for i in tmp_arr}

        context = {
            "now": pendulum.now().start_of("day"),
            "current_year": pendulum.now().year,
            "kaf_name": data['admission']['ckaf__name'],
            "discipline": data['planlines']['dis'],
            "kvalif": data['admission']['kvalif_name'],
            "spec_name": data['admission']['spec_name'],
            "kind": data['admission']['cadmkind__name_prof'],
            "kind_direct": 'Специальность' if data['admission']['cadmkind'] == 1 else 'Направление',
            "direction": data['admission']['cdirection__name'],
            "direction_code": data['admission']['cdirection__cod'],
            "fob": data['admission']['cfob__name'],
            "year_post": data['admission']['yr'],
            "person": data['person'],
            "person_name": CatPerson.objects.get(id=data['person']).name,
            "competence": competence,
            "indicators": indicators,
            "precedence": precedence_names,
            "subsequent": subsequent_names,
            "sum_zet": int(sum([i['zet'] for i in data['planlines']['semesters']])),
            "semesters": semesters,
            "sh": semester_hours,
            "sha": semester_hours_all,
            "wk": wk,
            "dg": discipline_grouped,
            "labw": lab_work_grouped,
            "prw": pr_work_grouped,
            "srsw": srs_work_res,
            "interactive_methods": interactive_methods,
            "guidelines": guidelines,
            "fos": fos,
            "tat": tat,
            'additional_library': additional_library,
            'main_library': main_library,
            "resources": resources,
            "software": software,
            "logistics": logistics,
        }

        doc.render(context)

        return doc
