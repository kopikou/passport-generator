from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rpd.models import RPDFiles


class UploadViewSet(
    CreateModelMixin
):
    queryset = RPDFiles.object.all()
    