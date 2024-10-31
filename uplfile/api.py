from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from auths.models import Permissions
from rpd.models import PlanData, PlanDocuments
from uplfile.models import UploadFiles
from uplfile.serializer import UploadFileSerializer


class UploadFileViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = None
    serializer_class = None
    permission_classes = [UserProfileHasPermission(Permissions.can_upload_files)]

    @action(methods=['GET'], url_path="get-admission-data", detail=False)
    def get_admission_data(self, request, *args, **kwargs):

        mira_id = self.request.user.userprofile.mira_id
        mira_id = 16236
        data = AISServices.get_admission_list_by_person(mira_id)

        abbrprofile_list = list(set([i['abbrprofile'] for i in data]))
        startyear_list = list(set([i['startyear'] for i in data]))

        filtered_data = PlanData.objects.filter(abbrprofile__in=abbrprofile_list, startyear__in=startyear_list, file__status=4)
        filtered_data_sorted = {f"{i.abbrprofile}_{i.startyear}": i for i in filtered_data}

        result = []
        for item in data:
            res = filtered_data_sorted.get(f"{item['abbrprofile']}_{item['startyear']}")
            if res:
                plan_documents = [i for i in res.plan_documents.values("id", "name", "new_type", "new_type__name")]
                result.append({
                    **item,
                    "plan_documents": plan_documents,
                    "plan_id": res.id,
                    "plan_name": res.file.title,
                })

        return Response(result)

    @action(methods=['POST'], url_path="save-file", detail=True)
    def save_file(self, request, *args, **kwargs):
        result = []

        for filename, file in request.FILES.items():
            data = {}
            if self.request.POST['type'] == 'document':
                doc_data = PlanDocuments.objects.get(id=kwargs['pk'])
                data = {
                    'user_id': request.user.id,
                    'file': file,
                    'title': filename,
                    'rpd_id': doc_data.plan_id,
                    'type_id': doc_data.new_type_id,
                    'lines_id': None,
                }

            data_serializer = UploadFileSerializer(data=data)
            data_serializer.is_valid(raise_exception=True)
            data_serializer.save()

        return Response(data_serializer.data)
