import os
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
        }

        doc.render(context)

        return doc
