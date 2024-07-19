from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from urllib3 import request

from rpd.models import RPDFile, PlanData, LinesData, PlanDocuments
from rpd.serializer import RpdFileSerializer, PlanDataSerializer, LinesDataSerializer, PlanDocumentsSerializer
from rpd.services import PLXParser, AISServices

from app.dictionaries import FILE_STATUS

class PlxUploadViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RPDFile.objects.all()
    serializer_class = RpdFileSerializer

    @action(methods=['POST'], url_path="insert-file", detail=False)
    def upload_plan_file(self, request, *args, **kwargs):
        if request.method == 'POST':
            for filename, file in request.FILES.items():
                data = {
                    'user_id': request.user.id,
                    'file': file,
                    'title': filename,
                    'status': 0,
                }

                data_serializer = RpdFileSerializer(data=data)

                data_serializer.is_valid(raise_exception=True)
                data_serializer.save()

            return JsonResponse(
                data={"success": "True"},
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(
            data={"success": "False"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=['GET'], url_path="get-files", detail=False)
    def get_files(self, request, *args, **kwargs):
        user = request.user

        data = RPDFile.objects.filter(user=user)
        serializer = RpdFileSerializer(data, many=True)

        for items in serializer.data:
            items['status'] = FILE_STATUS[items['status']][1]

        return JsonResponse({
            "items": [i for i in serializer.data],
        })

    @action(methods=['DELETE'], url_path="remove-files", detail=False)
    def remove_file(self, request, *args, **kwargs):
        id = request.data['id']

        RPDFile.objects.filter(id=id).delete()

        return JsonResponse({
            "success": "True",
        })

    @action(methods=['GET'], url_path="get-file-by-id", detail=False)
    def get_file_by_id(self, request, *args, **kwargs):

        id = request.GET['id']

        data = RPDFile.objects.filter(id=id)

        data.update(status=FILE_STATUS[2][0])

        serializer_data = RpdFileSerializer(data, many=True)

        parser = PLXParser(serializer_data.data[0]['file'], serializer_data.data[0]['id'])
        return JsonResponse({
            "items": [i for i in serializer_data.data],
            "parser": parser.get_result_data(),
        })

    @action(methods=['GET'], url_path="get-caf-codes", detail=False)
    def get_caf_codes(self, request, *args, **kwargs):
        data = AISServices.get_kaf_codes()

        return JsonResponse({
            "items": [i for i in data],
        })

    @action(methods=['POST'], url_path='update-plan-data', detail=False)
    def update_plan_data(self, request, *args, **kwargs):
        data = request.data

        instance = PlanData.objects.get(id=data['id'])

        serializer = PlanDataSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({
            "success": "True",
        })

    @action(methods=['POST'], url_path='update-lines-data', detail=False)
    def update_lines_data(self, request, *args, **kwargs):
        data = request.data

        instance = LinesData.objects.get(id=data['id'])

        serializer = LinesDataSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({
            "success": "True",
        })

    @action(methods=['POST'], url_path='add-document-data', detail=False)
    def add_document_data(self, request, *args, **kwargs):
        data = request.data

        serializer = PlanDocumentsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({
            "success": "True",
            "items": serializer.data
        })

    @action(methods=['POST'], url_path='update-document-data', detail=False)
    def update_document_data(self, request, *args, **kwargs):
        data = request.data

        instance = PlanDocuments.objects.get(id=data['id'])

        serializer = PlanDocumentsSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({
            "success": "True",
        })

