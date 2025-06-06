from django.db.models import Prefetch

from arim.services import AISServices
from rpd.models import PlanData, PlanDocuments
from uplfile.models import UploadFiles


class UploadFileService(object):

    @staticmethod
    def get_admission_data(mira_id):
        data = AISServices.get_admission_list_by_person(mira_id)

        abbrprofile_list = list(set([i['abbrprofile'] for i in data]))
        startyear_list = list(set([i['startyear'] for i in data]))

        filtered_data = PlanData.objects \
            .filter(abbrprofile__in=abbrprofile_list, startyear__in=startyear_list, file__status=4) \
            .prefetch_related(
            Prefetch("plan_documents", queryset=PlanDocuments.objects.select_related("new_type").all()),
            Prefetch("uplfile", queryset=UploadFiles.objects.all())
        ).select_related("file")
        filtered_data_sorted = {f"{i.abbrprofile}_{i.startyear}": i for i in filtered_data}

        result = []
        for item in data:
            res = filtered_data_sorted.get(f"{item['abbrprofile']}_{item['startyear']}")
            if res:
                result.append({
                    **item,
                    "plan_documents": [{
                        "id": i.id,
                        "name": i.name,
                        "type_id": i.new_type.id,
                        "type__name": i.new_type.name
                    } for i in res.plan_documents.all()],
                    "documents_files": [{
                        "user_id": i.user_id,
                        "title": i.title,
                        "url": i.file.url,
                        "type_id": i.type_id,
                        "id": i.id,
                    } for i in res.uplfile.all()],
                    "plan_id": res.id,
                    "plan_name": res.file.title,
                })

        return result