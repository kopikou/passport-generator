import os
from itertools import groupby

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
from uplfile.serializer import UploadFilesSerializer


class UploadFileViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = UploadFiles
    serializer_class = UploadFilesSerializer
    permission_classes = [UserProfileHasPermission(Permissions.can_upload_files)]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        os.remove(instance.file.path)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], url_path="get-admission-data", detail=False)
    def get_admission_data(self, request, *args, **kwargs):

        mira_id = self.request.user.userprofile.mira_id

        data = AISServices.get_admission_list_by_person(mira_id)

        abbrprofile_list = list(set([i['abbrprofile'] for i in data]))
        startyear_list = list(set([i['startyear'] for i in data]))

        filtered_data = PlanData.objects.filter(abbrprofile__in=abbrprofile_list, startyear__in=startyear_list, file__status=4)
        filtered_data_sorted = {f"{i.abbrprofile}_{i.startyear}": i for i in filtered_data}

        result = []
        for item in data:
            res = filtered_data_sorted.get(f"{item['abbrprofile']}_{item['startyear']}")
            if res:
                result.append({
                    **item,
                    "plan_documents": [i for i in res.plan_documents.values("id", "name", "new_type", "new_type__name")],
                    "documents_files": [i for i in res.uplfile.values()],
                    "plan_id": res.id,
                    "plan_name": res.file.title,
                })
        return Response(result)

    @action(methods=['POST'], url_path="save-file", detail=True)
    def save_file(self, request, *args, **kwargs):
        data = {}
        for filename, file in request.FILES.items():
            if self.request.POST['type'] == 'document':
                doc_data = PlanDocuments.objects.get(id=kwargs['pk'])
                data = {
                    'user_id': request.user.id,
                    'file': file,
                    'title': f"{doc_data.name}_{doc_data.plan.abbrprofile}-{str(doc_data.plan.startyear)[-2:]}",
                    'rpd_id': doc_data.plan_id,
                    'type_id': doc_data.new_type_id,
                    'lines_id': None,
                }

        data_serializer = UploadFilesSerializer(data=data)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.save()

        return Response(data_serializer.data)

