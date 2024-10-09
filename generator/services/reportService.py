import os
from pathlib import Path

from docxtpl import DocxTemplate

from app.settings import BASE_DIR


class ReportService(object):

    @staticmethod
    def get_rpd_docx(data):

        path = f"{BASE_DIR}{Path("/templates/docxRPD/rpd.docx")}"
        doc = DocxTemplate(path)

        context = {
            'name': "SkyFall",
        }

        doc.render(context)

        return doc