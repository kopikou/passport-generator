import os
from itertools import groupby
from pathlib import Path

import pendulum
from docxtpl import DocxTemplate

from app.settings import BASE_DIR
from arim.models import CatPerson


class ReportService(object):

    @staticmethod
    def get_rpd_docx(data):
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
                'know': item['discipline_indicator'][0]['know'] if item['discipline_indicator'][0]['know'] else '',
                'able': item['discipline_indicator'][0]['able'] if item['discipline_indicator'][0]['able'] else '',
                'own': item['discipline_indicator'][0]['own'] if item['discipline_indicator'][0]['own'] else '',
                'criteria': item['discipline_indicator'][0]['criteria'] if item['discipline_indicator'][0][
                    'criteria'] else '',
                'methods': item['discipline_indicator'][0]['methods'] if item['discipline_indicator'][0][
                    'methods'] else '',
            })

        precedence = []
        subsequent = []
        for item in data['additional_info']:
            if item['type'] == 'disciplinePlace':
                precedence = item['value']['precedence']
                subsequent = item['value']['subsequent']

        other_disciplines = {item['disid']: item['dis'] for item in data['other_discipline']}
        precedence_names = ", ".join([f"«{other_disciplines[item]}»" for item in precedence])
        subsequent_names = ", ".join([f"«{other_disciplines[item]}»" for item in subsequent])

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
        }

        doc.render(context)

        return doc
