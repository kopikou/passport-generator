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
from rpd.models import RPDFile, PlanData, LinesData, PlanDocuments, DocumentsTypes, LinesIndicators, SemesterData, \
    BaseDocuments
from rpd.serializer import RpdFileSerializer, PlanDataSerializer, LinesDataSerializer, PlanDocumentsSerializer, \
    BatchUpdateCafLinesSerializer, LinesIndicatorsSerializer, SemesterDataSerializer
from rpd.services import PLXParser
from rpgen.models import PlanIndikator


class PlxUploadViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RPDFile.objects.select_related('plandata').all()
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

            # сохраняем файл в БД
            old_file = RPDFile.objects.filter(title=filename).first()
            data_serializer = RpdFileSerializer(instance=old_file, data=data)
            data_serializer.is_valid(raise_exception=True)
            rpd_file_instance = data_serializer.save()

            # удвляем старый файл привязанный к плану
            file.seek(0)
            parser = PLXParser(file, rpd_file_instance.id)
            plan_data = parser.get_plan_data()
            plan_data_instance = PlanData.objects.filter(
                abbrprofile=plan_data['abbrprofile'],
                startyear=plan_data['startyear'],
            ).first()
            if plan_data_instance:
                RPDFile.objects.filter(id=plan_data_instance.file_id).delete()
                rpd_file_instance.plandata = plan_data_instance
                rpd_file_instance.save()

            # обновляем план по новому файлу
            parser.update_db()

        return Response(
            data={"success": "True"},
            status=status.HTTP_201_CREATED,
        )


    def retrieve(self, request, *args, **kwargs):
        instance: RPDFile = self.get_object()

        if instance.status == RPDFile.StatusChoice.download:
            instance.status = RPDFile.StatusChoice.in_review
            instance.save()

        serializer_data = RpdFileSerializer(instance)

        plan_data = PlanData.objects.filter(file=instance).first()

        lines_data = LinesData.objects.filter(plan=plan_data)
        indikators = LinesIndicators.objects.filter(planlineid__in=lines_data)
        semesters = SemesterData.objects.filter(planlineid__in=lines_data)

        return Response({
            "items": serializer_data.data,
            "parser": {
                'documents': PlanDocumentsSerializer(plan_data.plan_documents.all(), many=True).data,
                'indicators': LinesIndicatorsSerializer(indikators, many=True).data,
                'lines': LinesDataSerializer(lines_data, many=True).data,
                'plan': PlanDataSerializer(plan_data).data,
                'semester': SemesterDataSerializer(semesters, many=True).data,
            },
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

