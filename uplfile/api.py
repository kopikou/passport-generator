import os
from itertools import groupby

from django.db.models import Prefetch
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from auths.models import Permissions
from generator.models import PlanLinesLink
from generator.permissions import CanEditRPDProgram, CanUploadFiles, CanViewFileList
from rpd.models import PlanData, PlanDocuments, BaseDocuments
from uplfile.models import UploadFiles
from uplfile.serializer import UploadFilesSerializer
from uplfile.service import UploadFileService


class UploadFileViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = UploadFiles
    serializer_class = UploadFilesSerializer
    permission_classes = [CanViewFileList | UserProfileHasPermission(Permissions.can_upload_files)]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        os.remove(instance.file.path)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], url_path="get-admission-data", detail=False)
    def get_admission_data(self, request, *args, **kwargs):

        mira_id = self.request.user.userprofile.mira_id

        res = UploadFileService.get_admission_data(mira_id)

        return Response(res)

    @action(methods=['POST'], url_path="save-file", detail=True, permission_classes=[CanUploadFiles | UserProfileHasPermission(Permissions.can_upload_files)])
    def save_file(self, request, *args, **kwargs):
        data = {}
        for filename, file in request.FILES.items():
            if self.request.POST['type'] == 'document':
                doc_data = PlanDocuments.objects.get(id=self.request.POST['fileId'])
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


    @action(methods=['GET'], url_path="get-base-documents", detail=False)
    def get_base_documents(self, request, *args, **kwargs):

        res = BaseDocuments.objects.all().values()

        return Response([i for i in res], status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path="get-programs", detail=True)
    def get_programs(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')

        data = PlanLinesLink.objects.filter(planlines__plan_id=pk).select_related('planlines')
        res = []

        for i in data:
            res.append({
                'id': i.id,
                'status': i.status,
                'status_verbose': i.status_verbose,
                'dis': i.planlines.dis,
                'type': i.planlines.type,
            })

        return Response(data=res, status=status.HTTP_200_OK)