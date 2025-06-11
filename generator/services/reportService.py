import datetime
import os
import platform
import re
import shutil
from itertools import groupby
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from time import sleep

import pendulum
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.encoding import escape_uri_path
from docxtpl import DocxTemplate

from app.settings import BASE_DIR
from arim.models import CatPerson
from arim.services import AISServices
from generator.models import PlanLinesLink, ScientificData, FormControl
from rpd.models import LinesIndicators, PlanData

def flatten(xss):
    return [x for xs in xss for x in xs]

def get_tic_name(data, plan_data=None):
    result = []

    if plan_data:
        if plan_data['admission']['cadmkind'] == 5:
            if plan_data['planlines']['dis'] == 'Иностранный язык':
                result.append('Кандидатский экзамен по иностранному языку')
            if plan_data['planlines']['dis'] == 'История и философия науки':
                result.append('Кандидатский экзамен по истории и философии науки')

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

    if not result and plan_data['admission']['cadmkind'] == 5:
        result.append('Кандидатский экзамен по спец. дисциплине')


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
                "theme": item['theme'],
                "theme_id": item['theme_id'],
            })

    return result


class ReportService(object):

    @classmethod
    def generate_rpd_report(cls, instance: PlanLinesLink):
        from generator.services.generator_service import GeneratorService
        pk = instance.id
        rpd_data = GeneratorService.get_rpd_data(pk)

        path = f'templates/outputs/'

        if not os.path.exists(path):
            os.makedirs(path)

        with TemporaryDirectory() as dr:
            path_doc_file = os.path.join(dr, f"{pk}.docx")
            path_pdf_file = os.path.join(dr, f"{pk}.pdf")

            if rpd_data['planlines']['viewpract']:
                tpl = ReportService.get_practice_report(rpd_data)
            else:
                tpl = ReportService.get_rpd_report(rpd_data)
            # tpl.save(response)

            tpl.save(path_doc_file)

            if platform.system() == 'Linux':
                run([
                    'libreoffice', '--headless', '--invisible', '--convert-to',
                    'pdf', path_doc_file, '--outdir', os.path.dirname(path_pdf_file),
                ])
            elif platform.system() == 'Windows':
                from win32com.client import Dispatch

                word = Dispatch('Word.Application')
                doc = word.Documents.Open(path_doc_file)
                doc.SaveAs(path_pdf_file, FileFormat=17)
                word.Quit()

            success = False
            for i in range(10):
                try:
                    with open(path_pdf_file, 'rb') as file:
                        name = f"{rpd_data['admission']['abbr']}_{rpd_data['admission']['yr']}_{rpd_data['planlines']['dis']}_{pk}"
                        if instance.status == PlanLinesLink.StatusChoices.accepted:
                            name = f"{name}_accepted"

                        uploaded_file = UploadedFile(file, f"{name}.pdf")
                        uploaded_file.seek(0)

                        if instance.file \
                                and (not instance.last_accepted_file or instance.file.name != instance.last_accepted_file.name):
                            instance.file.delete()

                        instance.file = uploaded_file
                        instance.file_updated_at = datetime.datetime.now()

                        if  instance.status == PlanLinesLink.StatusChoices.accepted:
                            if instance.last_accepted_file:
                                instance.last_accepted_file.delete()
                            instance.last_accepted_file = instance.file
                        instance.save(update_fields=['file', 'last_accepted_file', 'file_updated_at'])
                        success = True
                except FileNotFoundError:
                    sleep(0.5)

                if success:
                    break

        return instance


    @staticmethod
    def get_rpd_annotation(data):
        path = f'{BASE_DIR}{Path("/templates/docxRPD/annotation.docx")}'
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
            tic_all.append(", ".join(get_tic_name(item, data)))

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
    def get_practice_report(data):

        if data['admission']['cadmkind'] == 3 and data['planlines']['viewpract'] == 8:
            path = f'{BASE_DIR}{Path("/templates/docxRPD/practice_nis.docx")}'
        else:
            path = f'{BASE_DIR}{Path("/templates/docxRPD/practice.docx")}'

        doc = DocxTemplate(path)

        competences_sorted = sorted(data['planlines']['indicators'], key=lambda item: item['competence_index'])
        competences_grouped = {key: list(items) for key, items in
                               groupby(competences_sorted, key=lambda item: item['competence_index'])}
        competence = []
        for sem, item in competences_grouped.items():
            competence.append({
                "index": sem,
                "content": item[0]['competence'],
                "indicators": ", ".join([i['indicator_index'] for i in item]),
                "ind_content": ", ".join([i['indicator'] for i in item]),
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

        if data['admission']['ckaf_id'] == 105:
            podrazdelene = data['admission']['cfac__name'].strip()
        else:
            podrazdelene = data['admission']['ckaf__ccatdep__nameshort'].strip()

        discipline = data['planlines']['dis'].split(': ')

        sems = [i['num'] for i in data['planlines']['semesters']]

        additional_library = []
        main_library = []
        tat = []
        fos = []
        resources = []
        software = []
        logistics = []
        practice_way = []
        practice_form = []
        practice_content_text = ''
        practice_content = []
        practice_report = []
        practice_report_req = ''
        for item in data['additional_info']:
            if item['type'] == 'practiceWay':
                practice_way = item['value']['practiceWay']
                practice_form = item['value'].get('practiceForm', [])

            if item['type'] == 'fos':
                q = 0

                # fos_choiced = set(flatten([i['formcontrol_list'] for i in data['discipline_themes']]))

                fos_sorted = sorted(data['discipline_themes'], key=lambda x: x['semester'])
                fos_grouped = {key: set(flatten([q['formcontrol_list'] for q in list(i)])) for key, i in groupby(fos_sorted, key=lambda x: x['semester'])}

                for i in item['value']:
                    if i['type'] in fos_grouped.get(int(i['num']), []):
                        q += 1
                        fos.append({
                            'num': i['num'],
                            'number': q,
                            'type': i['type'],
                            'title': i['title'],
                            'about': i['about'] if 'about' in i else '',
                            'criteria': i['criteria'] if 'criteria' in i else '',
                        })

            if item['type'] == 'practiceContent':
                practice_content = item['value']

            if item['type'] == 'practiceContentText':
                practice_content_text = item['value']['content']

            if item['type'] == 'practiceReport':
                practice_report_req = item['value']['requirements']
                practice_report = [i.strip() for i in item['value']['documents'].split('\n') if i.strip()]

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
                    if 'clicense__type' in i:
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
                for i in item['value']:
                    if i['num'] not in sems:
                        continue
                    q += 1
                    if i['type'] == 'zach':
                        tat.append({
                            'number': q,
                            'type': i['type'],
                            'title': i['title'].lower(),
                            'form': i.get('form', ''),
                            'formabout': i.get('formabout', ''),
                            "tat": i.get('tat', ''),
                            'passed': i['passed'],
                            'unpassed': i['unpassed'],
                        })
                    else:
                        tat.append({
                            'number': q,
                            'type': i['type'],
                            'title': i['title'].lower(),
                            'form': i.get('form', ''),
                            'formabout': i.get('formabout', ''),
                            "tat": i.get('tat', ''),
                            'great': i['great'],
                            'good': i['good'],
                            'satisfactorily': i['satisfactorily'],
                            'unsatisfactory': i['unsatisfactory'],
                        })



        semesters = []
        semester_hours = []
        tic_all = {}
        for item in data['planlines']['semesters']:
            tic_all[item['num']] = ", ".join(get_tic_name(item, data))
            semesters.append({
                "num": item['num'],
                "kurs": (item['num'] + 1) // 2,
                "srs_hours": item['srs'] or 0,
                "weeks": int(item['srs'] / 54),
                "zet": int(item['zet']) or 0,
                "tic": ', '.join(get_tic_name(item)),
            })

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


        semester_hours_sorted = sorted(semester_hours, key=lambda x: x['num'])
        semester_hours_grouped = {key: list(item) for key, item in
                                  groupby(semester_hours_sorted, key=lambda x: x['num'])}

        discipline_themes = {item['id']: item for item in data['discipline_themes']}
        discipline_sorted = sorted(data['discipline_themes'], key=lambda item: (item['semester'], item['num']))
        discipline_grouped = {sem: list(item) for sem, item in
                              groupby(discipline_sorted, key=lambda item: item['semester']) if sem in semester_hours_grouped}

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


        formcontrols = FormControl.objects.all()
        formcontrol_by_id = {i.id: i.name for i in formcontrols}

        work_hour = []
        for e, item in enumerate(data['discipline_work_hour']):
            work_hour.append({
                "num": item['semester'],
                "theme": discipline_themes[item['theme_id']]['name'],
                "theme_id": item['theme_id'],
                "formcontrol": ', '.join(
                    [formcontrol_by_id[i] for i in discipline_themes[item['theme_id']]['formcontrol_list']]),
                "type": item['type'],
                "content": item['name'],
                "hours": item['hours'],
                "number": item['num'],
                "tic": [s['ekz_hours'] for s in semester_hours if s['num'] == item['semester']],
                "tic_all": [s['tic'] for s in semester_hours if s['num'] == item['semester']]
            })


        srs_work = get_work_hours(work_hour, 2)
        srs_work_sorted = sorted(srs_work, key=lambda item: (item['num'], item['content']))
        srs_work_grouped = {key: list(item) for key, item in groupby(srs_work_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        lekc_work = get_work_hours(work_hour, 0)
        lekc_work_sorted = sorted(lekc_work, key=lambda item: (item['num'], item['number']))
        lekc_work_grouped = {key: list(item) for key, item in groupby(lekc_work_sorted, key=lambda item: item['num']) if
                             key in semester_hours_grouped}

        lab_work = get_work_hours(work_hour, 3)
        lab_work_sorted = sorted(lab_work, key=lambda item: (item['num'], item['number']))
        lab_work_grouped = {key: list(item) for key, item in groupby(lab_work_sorted, key=lambda item: item['num']) if
                            key in semester_hours_grouped}

        pr_work = get_work_hours(work_hour, 1)
        pr_work_sorted = sorted(pr_work, key=lambda item: (item['num'], item['number']))
        pr_work_grouped = {key: list(item) for key, item in groupby(pr_work_sorted, key=lambda item: item['num']) if
                           key in semester_hours_grouped}

        srs_work_res = {}
        for sem, items in srs_work_grouped.items():
            res_sorted = sorted(items, key=lambda i: i['content'])
            res_grouped = {k: list(i) for k, i in groupby(res_sorted, key=lambda item: item['content'])}

            tmp = []
            v = 1
            for k, i in res_grouped.items():
                tmp.append({
                    "content": k,
                    "number": v,
                    "hours": sum([q['hours'] for q in i]),
                    "theme": i[0]['theme'],
                    "theme_id": i[0]['theme_id'],
                })
                v += 1

            srs_work_res[sem] = tmp

        wk_data = {}
        for sem, items in discipline_grouped.items():

            if sem not in semester_hours_grouped:
                continue

            res = []
            for item in items:
                tmp_srs = []
                tmp_lab = []
                tmp_pr = []
                tmp_lekc = []
                if srs_work_grouped.get(sem):
                    for q in srs_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_srs.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                            })

                if lab_work_grouped.get(sem):
                    for q in lab_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_lab.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                if pr_work_grouped.get(sem):
                    for q in pr_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_pr.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                if lekc_work_grouped.get(sem):
                    for q in lekc_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_lekc.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                res.append({
                    **item,
                    "srs": tmp_srs,
                    "lab": tmp_lab,
                    "pr": tmp_pr,
                    "lekc": tmp_lekc,
                })

            wk_data[sem] = res


        for sem, items in wk_data.items():
            if sem not in semester_hours_grouped:
                continue

            tmp = []
            for item in items:
                res = []
                if srs_work_grouped:
                    for q in srs_work_grouped[sem]:
                        if q['theme'] == item['name']:
                            r = list(filter(
                                lambda x: x['content'] == q['content'], srs_work_res[sem]
                            ))
                            res.append(str(r[0]['number']))

                tmp.append({
                    "name": item['name'],
                    "tic": ', '.join([formcontrol_by_id[i] for i in item['formcontrol_list']]),
                    "num": item['num'],
                    "lekc": item['num'],
                    "lekc_hours": sum([i['hours'] for i in item['lekc']]) if sum(
                        [i['hours'] for i in item['lekc']]) != 0 else '',
                    "lab": ', '.join([str(i['number']) for i in item['lab']]),
                    "lab_hours": sum([i['hours'] for i in item['lab']]) if sum(
                        [i['hours'] for i in item['lab']]) != 0 else '',
                    "pr": ', '.join([str(i['number']) for i in item['pr']]),
                    "pr_hours": sum([i['hours'] for i in item['pr']]) if sum(
                        [i['hours'] for i in item['pr']]) != 0 else '',
                    "srs": ', '.join(res),
                    "srs_hours": sum([i['hours'] for i in item['srs']]) if sum(
                        [i['hours'] for i in item['srs']]) != 0 else '',
                })

            wk_data[sem] = tmp

            wk_data[sem].append({
                "name": 'Промежуточная аттестация',
                "tic": semester_hours_grouped[sem][0]['tic'],
                "num": '',
                "lekc": '',
                "lekc_hours": '',
                "lab": '',
                "lab_hours": '',
                "pr": '',
                "pr_hours": '',
                "srs": '',
                "srs_hours": semester_hours_grouped[sem][0]['ekz_hours'] if semester_hours_grouped[sem][0][
                                                                                'ekz_hours'] != 0 else '',
            })

            wk_data[sem].append({
                "name": 'Всего',
                "tic": '',
                "num": '',
                "lekc": '',
                "lekc_hours": sum([i['lekc_hours'] for i in tmp if i['lekc_hours'] != '']) if sum(
                    [i['lekc_hours'] for i in tmp if i['lekc_hours'] != '']) != 0 else '',
                "lab": '',
                "lab_hours": sum([i['lab_hours'] for i in tmp if i['lab_hours'] != '']) if sum(
                    [i['lab_hours'] for i in tmp if i['lab_hours'] != '']) != 0 else '',
                "pr": '',
                "pr_hours": sum([i['pr_hours'] for i in tmp if i['pr_hours'] != '']) if sum(
                    [i['pr_hours'] for i in tmp if i['pr_hours'] != '']) != 0 else '',
                "srs": '',
                "srs_hours": sum([i['srs_hours'] for i in tmp if i['srs_hours'] != '']) if sum(
                    [i['srs_hours'] for i in tmp if i['srs_hours'] != '']) != 0 else '',
            })

        contex = {
            "now": pendulum.now().start_of("day"),
            "current_year": pendulum.now().year,
            "kaf_name": data['admission']['ckaf__name'],
            "fac_name": data['admission']['cfac__name'],
            "podrazdelene": podrazdelene,
            "view_pract": discipline[0],
            "discipline": data['planlines']['dis'],
            "kvalif": data['admission']['kvalif_name'],
            "spec_name": data['admission']['spec_name'],
            "kind": data['admission']['cadmkind__name_prof'],
            "kind_direct": 'Специальность' if data['admission']['cadmkind'] == 1 else 'Направление',
            "direction": data['admission']['cdirection__name'],
            "direction_code": data['admission']['cdirection__cod'],
            "year_post": data['admission']['yr'],
            "protocol_number": data['protocol_number'] if data['protocol_number'] else '',
            "meeting": data['meeting'] if data['meeting'] else '',
            "accept_date": data['accept_date'] if data['accept_date'] else '',
            "review_date": data['review_date'] if data['review_date'] else '',
            "fob": data['admission']['cfob__name'],
            "semesters": semesters,
            "status": data['status'],
            "practice_way": ', '.join(practice_way),
            "practice_form": ', '.join(practice_form),
            "competence": competence,
            "indicators": indicators,
            "practice_content_text": practice_content_text,
            "practice_content": practice_content,
            "practice_report_req": practice_report_req,
            "practice_report": practice_report,
            "additional_library": additional_library,
            "main_library": main_library,
            "resources": resources,
            "software": software,
            "logistics": logistics,
            "tat": tat,
            "srsw": srs_work_res,
            "prw": pr_work_grouped,
            "dg": discipline_grouped,
            "wk": wk_data,
            "fos": fos,
        }

        doc.render(contex)

        return doc

    @staticmethod
    def get_rpd_report(data):
        path = f'{BASE_DIR}{Path("/templates/docxRPD/rpd.docx")}'

        if data['admission']['cadmkind'] == 5:
            path = f'{BASE_DIR}{Path("/templates/docxRPD/rpd_asp.docx")}'

        doc = DocxTemplate(path)

        formcontrols = FormControl.objects.all()
        formcontrol_by_id = {i.id: i.name for i in formcontrols}

        competences_sorted = sorted(data['planlines']['indicators'], key=lambda item: item['competence_index'])
        competences_grouped = {key: list(items) for key, items in
                               groupby(competences_sorted, key=lambda item: item['competence_index'])}
        competence = []
        for sem, item in competences_grouped.items():
            competence.append({
                "index": sem,
                "content": item[0]['competence'],
                "indicators": ", ".join([i['indicator_index'] for i in item]) if data['admission']['cadmkind'] != 5 else "\n".join([f"{i['indicator_index']} {i['indicator']}" for i in item]),
                "ind_content": ", ".join([i['indicator'] for i in item]),
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
            'foreign': 'Типовые оценочные средства для кандидатского экзамена по иностранному языку',
            'philosophy': 'Типовые оценочные средства для кандидатского экзамена по истории и философии науки',
            'base': 'Типовые оценочные средства для кандидатского экзамена по спец. дисциплине',
        }

        asp_spec = ''
        asp_napr = None
        asp_code = ''

        if data['admission']['cadmkind'] == 5:
            tat_titles.update({'ekz': 'Типовые оценочные средства для проведения кандидатского экзамена по дисциплине',})

            if data['admission']['spec_name'].find(', направленность') != -1:
                napr = data['admission']['spec_name'].split(', направленность -')

                asp_spec = napr[0]
                asp_napr = napr[1]
                asp_code = data['admission']['cspec__code']
            else:
                asp_spec = data['admission']['spec_name']
                asp_code = data['admission']['cspec__code']

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

        sems = [i['num'] for i in data['planlines']['semesters']]

        has_labs = sum(i['lab'] for i in data['planlines']['semesters'] if i['lab']) > 0
        has_pr = sum(i['pr'] for i in data['planlines']['semesters'] if i['pr']) > 0
        has_lekc = sum(i['lekc'] for i in data['planlines']['semesters'] if i['lekc']) > 0
        has_kp = sum(i['kp_hour'] for i in data['planlines']['semesters'] if i['kp_hour']) > 0
        has_kr = sum(i['kr_hour'] for i in data['planlines']['semesters'] if i['kr_hour']) > 0
        has_kp_kr = has_kp or has_kr

        for item in data['additional_info']:
            if item['type'] == 'interactiveMethods':
                interactive_methods = item['value']['interactiveMethods']

            if item['type'] == 'disciplinePlace':
                precedence = item['value']['precedence']
                subsequent = item['value']['subsequent']

            if item['type'] == 'guidelines':
                q = 0
                for k, i in item['value'][0].items():
                    if k == 'course' and not has_kp_kr:
                        continue
                    if k == 'practice' and not has_pr:
                        continue
                    if k == 'laboratory' and not has_labs:
                        continue

                    q += 1
                    guidelines.append({
                        'number': q,
                        'type': k,
                        'title': guidelines_titles[k],
                        'content': i,
                    })

            if item['type'] == 'fos':
                q = 0

                # fos_choiced = set(flatten([i['formcontrol_list'] for i in data['discipline_themes']]))

                fos_sorted = sorted(data['discipline_themes'], key=lambda x: x['semester'])
                fos_grouped = {key: set(flatten([q['formcontrol_list'] for q in list(i)])) for key, i in groupby(fos_sorted, key=lambda x: x['semester'])}

                for i in item['value']:
                    if i['type'] in fos_grouped.get(int(i['num']), []):
                        q += 1
                        fos.append({
                            'num': i['num'],
                            'number': q,
                            'type': i['type'],
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
                    if 'clicense__type' in i:
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
                for i in sorted(item['value'], key=lambda x: x['num']):
                    if i['num'] not in sems:
                        continue
                    q += 1
                    if i['type'] == 'zach':
                        tat.append({
                            'number': q,
                            'type': i['type'],
                            'title': f"Семестр {i['num']}, {tat_titles[i['type']]}",
                            # 'main': i['main'],
                            'num': i['num'],
                            'about': i['about'],
                            'example': i['example'],
                            'passed': i['passed'],
                            'unpassed': i['unpassed'],
                        })
                    else:
                        tat.append({
                            'number': q,
                            'type': i['type'],
                            'title': f"Семестр {i['num']}, {tat_titles[i['type']]}",
#                             'main': i['main'],
                            'num': i['num'],
                            'about': i['about'],
                            'example': i['example'],
                            'great': i['great'],
                            'good': i['good'],
                            'satisfactorily': i['satisfactorily'],
                            'unsatisfactory': i['unsatisfactory'],
                        })

        other_disciplines = {item['disid']: f"«{item['dis']}»" for item in data['other_discipline']}
        other_disciplines.update({0: 'Нет'})

        precedence_names = ''
        subsequent_names = ''
        if precedence:
            precedence_names = ", ".join([f"{other_disciplines[item]}" for item in precedence if item in other_disciplines])
        if subsequent:
            subsequent_names = ", ".join([f"{other_disciplines[item]}" for item in subsequent if item in other_disciplines])

        tic_all = {}
        semester_hours = []
        semesters = []
        for item in data['planlines']['semesters']:
            tic_all[item['num']] = ", ".join(get_tic_name(item, data))
            semesters.append(item['num'])
            semester_hours.append({
                "num": item['num'],
                "aud_hours": sum([
                    item['lekc'] or 0,
                    item['lab'] or 0,
                    item['pr'] or 0,
                ]),
                "contact_hours": sum([
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

        semester_hours_sorted = sorted(semester_hours, key=lambda x: x['num'])
        semester_hours_grouped = {key: list(item) for key, item in
                                  groupby(semester_hours_sorted, key=lambda x: x['num'])}

        semester_hours_all = {
            "lekc_hours_all": sum([i['lekc'] or 0 for i in data['planlines']['semesters']]),
            "lab_hours_all": sum([i['lab'] or 0 for i in data['planlines']['semesters']]),
            "pr_hours_all": sum([i['pr'] or 0 for i in data['planlines']['semesters']]),
            "srs_hours_all": sum([i['srs'] or 0 for i in data['planlines']['semesters']]),
            "ekz_hours_all": sum([i['ekzhour'] or 0 for i in data['planlines']['semesters']]),
            "eios_hours_all": sum([i['eios'] or 0 for i in data['planlines']['semesters']]),
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
                semester_hours_all['eios_hours_all'] or 0,
            ]),
        })
        semester_hours_all.update({
            "tic_all": ", ".join(set([item for key, item in tic_all.items()])),
        })

        discipline_themes = {item['id']: item for item in data['discipline_themes']}
        discipline_sorted = sorted(data['discipline_themes'], key=lambda item: (item['semester'], item['num']))
        discipline_grouped = {sem: list(item) for sem, item in
                              groupby(discipline_sorted, key=lambda item: item['semester']) if sem in semester_hours_grouped}

        work_hour = []
        for e, item in enumerate(data['discipline_work_hour']):
            work_hour.append({
                "num": item['semester'],
                "theme": discipline_themes[item['theme_id']]['name'],
                "theme_id": item['theme_id'],
                "formcontrol": ', '.join([formcontrol_by_id[i] for i in discipline_themes[item['theme_id']]['formcontrol_list']]),
                "type": item['type'],
                "content": item['name'],
                "hours": item['hours'],
                "number": item['num'],
                "tic": [s['ekz_hours'] for s in semester_hours if s['num'] == item['semester']],
                "tic_all": [s['tic'] for s in semester_hours if s['num'] == item['semester']]
            })
        work_hour_sorted = sorted([i for i in work_hour if i['num'] in semester_hours_grouped], key=lambda item: item['num'])
        wk = {key: list(items) for key, items in
              groupby(work_hour_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        lekc_work = get_work_hours(work_hour, 0)
        lekc_work_sorted = sorted(lekc_work, key=lambda item: (item['num'], item['number']))
        lekc_work_grouped = {key: list(item) for key, item in groupby(lekc_work_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        lab_work = get_work_hours(work_hour, 3)
        lab_work_sorted = sorted(lab_work, key=lambda item: (item['num'], item['number']))
        lab_work_grouped = {key: list(item) for key, item in groupby(lab_work_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        pr_work = get_work_hours(work_hour, 1)
        pr_work_sorted = sorted(pr_work, key=lambda item: (item['num'], item['number']))
        pr_work_grouped = {key: list(item) for key, item in groupby(pr_work_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        srs_work = get_work_hours(work_hour, 2)
        srs_work_sorted = sorted(srs_work, key=lambda item: (item['num'], item['content']))
        srs_work_grouped = {key: list(item) for key, item in groupby(srs_work_sorted, key=lambda item: item['num']) if key in semester_hours_grouped}

        srs_work_res = {}
        for sem, items in srs_work_grouped.items():
            res_sorted = sorted(items, key=lambda i: i['content'])
            res_grouped = {k: list(i) for k, i in groupby(res_sorted, key=lambda item: item['content'])}

            tmp = []
            v = 1
            for k, i in res_grouped.items():
                tmp.append({
                    "content": k,
                    "number": v,
                    "hours": sum([q['hours'] for q in i]),
                    "theme": i[0]['theme'],
                    "theme_id": i[0]['theme_id'],
                })
                v += 1

            srs_work_res[sem] = tmp

        wk_data = {}
        for sem, items in discipline_grouped.items():

            if sem not in semester_hours_grouped:
                continue

            res = []
            for item in items:
                tmp_srs = []
                tmp_lab = []
                tmp_pr = []
                tmp_lekc = []
                if srs_work_grouped.get(sem):
                    for q in srs_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_srs.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                            })

                if lab_work_grouped.get(sem):
                    for q in lab_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_lab.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                if pr_work_grouped.get(sem):
                    for q in pr_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_pr.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                if lekc_work_grouped.get(sem):
                    for q in lekc_work_grouped[sem]:
                        if item['id'] == q['theme_id']:
                            tmp_lekc.append({
                                "hours": q['hours'],
                                "theme": q['theme'],
                                "theme_id": q['theme_id'],
                                "name": q['content'],
                                "number": q['number'],
                            })

                res.append({
                    **item,
                    "srs": tmp_srs,
                    "lab": tmp_lab,
                    "pr": tmp_pr,
                    "lekc": tmp_lekc,
                })

            wk_data[sem] = res

        for sem, items in wk_data.items():
            if sem not in semester_hours_grouped:
                continue

            tmp = []
            for item in items:
                res = []
                if srs_work_grouped:
                    for q in srs_work_grouped[sem]:
                        if q['theme'] == item['name']:
                            r = list(filter(
                                lambda x: x['content'] == q['content'], srs_work_res[sem]
                            ))
                            res.append(str(r[0]['number']))

                tmp.append({
                    "name": item['name'],
                    "tic": ', '.join([formcontrol_by_id[i] for i in item['formcontrol_list']]),
                    "num": item['num'],
                    "lekc": ', '.join([str(i['number']) for i in item['lekc']]),
                    "lekc_hours": sum([i['hours'] for i in item['lekc']]) if sum(
                        [i['hours'] for i in item['lekc']]) != 0 else '',
                    "lab": ', '.join([str(i['number']) for i in item['lab']]),
                    "lab_hours": sum([i['hours'] for i in item['lab']]) if sum(
                        [i['hours'] for i in item['lab']]) != 0 else '',
                    "pr": ', '.join([str(i['number']) for i in item['pr']]),
                    "pr_hours": sum([i['hours'] for i in item['pr']]) if sum(
                        [i['hours'] for i in item['pr']]) != 0 else '',
                    "srs": ', '.join(res),
                    "srs_hours": sum([i['hours'] for i in item['srs']]) if sum(
                        [i['hours'] for i in item['srs']]) != 0 else '',
                })

            wk_data[sem] = tmp

            wk_data[sem].append({
                "name": 'Промежуточная аттестация',
                "tic": semester_hours_grouped[sem][0]['tic'],
                "num": '',
                "lekc": '',
                "lekc_hours": '',
                "lab": '',
                "lab_hours": '',
                "pr": '',
                "pr_hours": '',
                "srs": '',
                "srs_hours": semester_hours_grouped[sem][0]['ekz_hours'] if semester_hours_grouped[sem][0][
                                                                                'ekz_hours'] != 0 else '',
            })

            wk_data[sem].append({
                "name": 'Всего',
                "tic": '',
                "num": '',
                "lekc": '',
                "lekc_hours": sum([i['lekc_hours'] for i in tmp if i['lekc_hours'] != '']) if sum(
                    [i['lekc_hours'] for i in tmp if i['lekc_hours'] != '']) != 0 else '',
                "lab": '',
                "lab_hours": sum([i['lab_hours'] for i in tmp if i['lab_hours'] != '']) if sum(
                    [i['lab_hours'] for i in tmp if i['lab_hours'] != '']) != 0 else '',
                "pr": '',
                "pr_hours": sum([i['pr_hours'] for i in tmp if i['pr_hours'] != '']) if sum(
                    [i['pr_hours'] for i in tmp if i['pr_hours'] != '']) != 0 else '',
                "srs": '',
                "srs_hours": sum([i['srs_hours'] for i in tmp if i['srs_hours'] != '']) if sum(
                    [i['srs_hours'] for i in tmp if i['srs_hours'] != '']) != 0 else '',
            })

        ckafs = AISServices.get_kaf_codes()
        ckafs_by_id = {i['value']: i['label'] for i in ckafs}

        if data['planlines']['caf']:
            podrazdelene = ckafs_by_id.get(data['planlines']['caf'], '')
        else:
            if data['admission']['ckaf_id'] == 105:
                podrazdelene = data['admission']['cfac__name'].strip()
            else:
                podrazdelene = data['admission']['ckaf__ccatdep__nameshort'].strip()
        context = {
            "now": pendulum.now().start_of("day"),
            "current_year": pendulum.now().year,
            "kaf_name": data['admission']['ckaf__name'],
            "fac_name": data['admission']['cfac__name'],
            "podrazdelene": podrazdelene,
            "discipline": data['planlines']['dis'],
            "kvalif": data['admission']['kvalif_name'],
            "spec_name": data['admission']['spec_name'],
            "kind": data['admission']['cadmkind__name_prof'],
            "kind_direct": 'Специальность' if data['admission']['cadmkind'] == 1 else 'Направление',
            "direction": data['admission']['cdirection__name'],
            "direction_code": data['admission']['cdirection__cod'],
            "asp_spec": asp_spec,
            "asp_napr": asp_napr,
            "asp_code": asp_code,
            "fob": data['admission']['cfob__name'],
            "year_post": data['admission']['yr'],
            "person": data['person'],
            "person_name": CatPerson.objects.get(id=data['person']).name,
            "competence": competence,
            "indicators": indicators,
            "precedence": precedence_names,
            "subsequent": subsequent_names,
            "sum_zet": int(sum([i['zet'] or 0 for i in data['planlines']['semesters']])),
            "semesters": semesters,
            "sh": semester_hours,
            "sha": semester_hours_all,
            "wk": wk_data,
            "dg": discipline_grouped,
            "labw": lab_work_grouped,
            "prw": pr_work_grouped,
            "srsw": srs_work_res,
            "interactive_methods": interactive_methods,
            "guidelines": guidelines,
            "fos": [{**i, "number": index} for index, i in enumerate(sorted(fos, key=lambda x: int(x['num'])), start=1)],
            "tat": [{**i, "number": index} for index, i in enumerate(sorted(tat, key=lambda x: int(x['num'])), start=1)],
            'additional_library': additional_library,
            'main_library': main_library,
            "resources": resources,
            "software": software,
            "logistics": logistics,
            "protocol_number": data['protocol_number'] if data['protocol_number'] else '',
            "meeting": data['meeting'] if data['meeting'] else '',
            "accept_date": pendulum.from_format(data['accept_date'], "YYYY-MM-DD").format("DD.MM.YYYY") if data['accept_date'] else '',
            "review_date": pendulum.from_format(data['review_date'], "YYYY-MM-DD").format("DD.MM.YYYY") if data['review_date'] else '',
            "status": data['status'],
        }

        if data['status'] == PlanLinesLink.StatusChoices.accepted:
            protocol_date = pendulum.from_format(data['protocol_date'], "YYYY-MM-DD")
            confirm_date = pendulum.from_format(data['confirm_date'], "YYYY-MM-DD") if data['confirm_date'] else ""
            user_accepted = User.objects.filter(id=data['user_accepted_id']).first()
            user_confirmed = User.objects.filter(id=data['user_confirmed_id']).first()

            is_only_accepted = user_confirmed is None

            user_confirmed = (user_confirmed.last_name + " " + user_confirmed.first_name + " " + user_confirmed.userprofile.middle_name) if user_confirmed is not None else ""

            context.update({
                "protocol_date": protocol_date.format("DD MMMM YYYY"),
                "protocol_year": protocol_date.format("YYYY"),
                "user_accepted": f"{user_accepted.last_name} {user_accepted.first_name} {user_accepted.userprofile.middle_name}",
                "user_confirmed": user_confirmed,
                "confirm_date": f'{confirm_date.format("DD.MM.YYYY") if confirm_date else ""}',
                "user_accepted_is_confirmed": user_confirmed != "" and user_confirmed == f"{user_accepted.last_name} {user_accepted.first_name} {user_accepted.userprofile.middle_name}",
                "is_only_accepted": is_only_accepted,
            })

            if context["user_accepted_is_confirmed"]:
                context["confirm_date"] = max(context["accept_date"], context["confirm_date"])


        doc.render(context)

        return doc

    @staticmethod
    def get_scientific_report(data):
        path = ''
        if int(data.rng) == 4:
            path = f'{BASE_DIR}{Path("/templates/docxRPD/scientific_four.docx")}'
        elif int(data.rng) == 3:
            path = f'{BASE_DIR}{Path("/templates/docxRPD/scientific_third.docx")}'

        doc = DocxTemplate(path)

        scientific_data = ScientificData.objects.filter(plan_id=data.id).values()
        rpd_data = PlanData.objects.get(mira_id=data.mira_id)

        p2_indicator = LinesIndicators.objects.filter(planlineid__plan_id=rpd_data.id, competence_index='Р-2').last()
        p2_1_indicator = LinesIndicators.objects.filter(planlineid__plan_id=rpd_data.id, indicator_index='Р-2.1').last()
        p2_2_indicator = LinesIndicators.objects.filter(planlineid__plan_id=rpd_data.id, indicator_index='Р-2.2').last()

        table_colums = [
            {'title': 'Подготовительный этап выполнения научного исследования', 'semesters': [1, 2]},
            {'title': 'Основной этап выполнения научного исследования',
             'semesters': [3, 4] if int(data.rng) == 3 else [3, 4, 5, 6]},
            {'title': 'Завершающий этап выполнения научного исследования',
             'semesters': [5, 6] if int(data.rng) == 3 else [7, 8]},
        ]

        table_data = []
        for column in table_colums:
            tmp = {}
            for s in column['semesters']:
                tmp[s] = sorted(
                    [i for i in scientific_data if
                     i['parameters']['part'] == 0 and int(i['parameters']['semester']) == s],
                    key=lambda x: x['parameters']['order'])

            table_data.append({
                'title': column['title'],
                'semesters': tmp,
            })

        name = data.name
        if name.find('Направленность') != -1:
            parts = data.name.split('Направленность')
            name = f"{parts[0]}\nНаправленность {parts[1]}"

        contex = {
            'name': name,
            'ckaf': data.ckaf,
            'cfac': data.cfac,
            'cfob': data.cfob,
            'rng': data.rng,
            'startyear': data.startyear,
            'fgt': data.fgt,
            'viceRector': re.sub(r'(?<= \w)\w+', '.', data.viceRector),
            'director': re.sub(r'(?<= \w)\w+', '.', data.director),
            'zavkaf': re.sub(r'(?<= \w)\w+', '.', data.zavkaf),
            'rop': re.sub(r'(?<= \w)\w+', '.', data.rop),
            'year': data.year,
            'p2': p2_indicator.competence,
            'p21': p2_1_indicator.indicator,
            'p22': p2_2_indicator.indicator,
            'scientific_research': table_data,
            'scientific_dissert': sorted([i for i in scientific_data if i['parameters']['part'] == 1],
                                         key=lambda x: x['parameters']['order']),
            'scientific_publish': sorted([i for i in scientific_data if i['parameters']['part'] == 2],
                                         key=lambda x: x['parameters']['order']),
        }

        doc.render(contex)

        return doc
