from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from urllib3 import request

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from auths.models import Permissions
from rpd.models import RPDFile, PlanData, LinesData, PlanDocuments, DocumentsTypes
from rpd.serializer import RpdFileSerializer, PlanDataSerializer, LinesDataSerializer, PlanDocumentsSerializer, \
    BatchUpdateCafLinesSerializer
from rpd.services import PLXParser


class PlxUploadViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RPDFile.objects.all()
    serializer_class = RpdFileSerializer
    permission_classes = [UserProfileHasPermission(Permissions.can_upload_plx_files)]

    @action(methods=['POST'], url_path="insert-file", detail=False)
    def upload_plan_file(self, request, *args, **kwargs):
        for filename, file in request.FILES.items():
            data = {
                'user_id': request.user.id,
                'file': file,
                'title': filename,
                'status': 0,
            }

            if RPDFile.objects.filter(title=filename).exists():
                raise APIException({
                    "message": f"Файл {filename} уже существует"
                }, status.HTTP_400_BAD_REQUEST)

            data_serializer = RpdFileSerializer(data=data)

            data_serializer.is_valid(raise_exception=True)
            data_serializer.save()

        return Response(
            data={"success": "True"},
            status=status.HTTP_201_CREATED,
        )


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == RPDFile.StatusChoice.download:
            instance.status = RPDFile.StatusChoice.in_review
            instance.save()

        serializer_data = RpdFileSerializer(instance)

        parser = PLXParser(serializer_data.data['file'], serializer_data.data['id'])
        return Response({
            "items": serializer_data.data,
            "parser": parser.get_result_data(),
        }, status=status.HTTP_200_OK)


    @action(methods=['GET'], url_path='accept-file', detail=False)
    def accept_file(self, request, *args, **kwargs):
        id = request.GET['id']

        data = RPDFile.objects.filter(id=id)

        data.update(status=RPDFile.StatusChoice.accepted.value)

        return Response({
            "success": True,
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='update-plan-data', detail=False)
    def update_plan_data(self, request, *args, **kwargs):
        data = request.data

        instance = PlanData.objects.get(id=data['id'])

        serializer = PlanDataSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": "True",
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='update-lines-data', detail=False)
    def update_lines_data(self, request, *args, **kwargs):
        data = request.data['data']

        instance = LinesData.objects.get(id=data['id'])

        serializer = LinesDataSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": "True",
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='add-document-data', detail=False)
    def add_document_data(self, request, *args, **kwargs):
        data = request.data

        serializer = PlanDocumentsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": "True",
            "items": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], url_path='update-document-data', detail=False)
    def update_document_data(self, request, *args, **kwargs):
        data = request.data

        instance = PlanDocuments.objects.get(id=data['id'])

        serializer = PlanDocumentsSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "success": "True",
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], url_path='batch-update-caf-lines', detail=False)
    def batch_update_caf_lines(self, request, *args, **kwargs):

        serializer = BatchUpdateCafLinesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = LinesData.objects.filter(id__in=serializer.validated_data['ids']).update(
            caf=serializer.validated_data['caf'])

        return Response({
            "success": "True",
        }, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path='get-lines-data', detail=False)
    def get_lines_data(self, request, *args, **kwargs):

        id = request.GET['id']

        data = LinesData.objects.filter(plan__file_id=id).values()

        return Response({
            "items": [i for i in data],
        }, status=status.HTTP_200_OK)

    @action(methods=['GET'], url_path='get-document-types', detail=False)
    def get_document_types(self, request, *args, **kwargs):

        data = DocumentsTypes.objects.all().values()

        return Response([i for i in data], status=status.HTTP_200_OK)
