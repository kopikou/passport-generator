from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from rpd.models import RPDFile
from rpd.serializer import RpdFileSerializer

class UploadViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = RPDFile.objects.all()
    serializer_class = RpdFileSerializer

    @action(methods=['POST'], url_path="insert_file", detail=False)
    def upload_plan_file(self, request, *args, **kwargs):
        if request.method == 'POST':
            for filename, file in request.FILES.items():
                data = {
                    'user_id': request.user.id,
                    'file': file,
                    'title': filename,
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

    @action(methods=['GET'], url_path="get_files", detail=False)
    def get_files(self, request, *args, **kwargs):
        user = request.user

        data = RPDFile.objects.filter(user=user, is_deleted=False)
        serializer = RpdFileSerializer(data, many=True)

        return JsonResponse({
            "items": [i for i in serializer.data],
        })

    @action(methods=['DELETE'], url_path="remove_files", detail=False)
    def remove_file(self, request, *args, **kwargs):
        id = request.data['id']

        RPDFile.objects.filter(id=id, is_deleted=False)[0].soft_delete()

        return JsonResponse({
            "success": "True",
        })