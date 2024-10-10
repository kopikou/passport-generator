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
        competences_grouped = {key: list(items) for key, items in groupby(competences_sorted, key=lambda  item: item['competence_index'])}

        competence = []
        for key, item in competences_grouped.items():
            competence.append({
                "index": key,
                "label": item[0]['competence'],
                "indicators": ", ".join([i['indicator_index'] for i in item]),
            })

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
        }

        doc.render(context)

        return doc
