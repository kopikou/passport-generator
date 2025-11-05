from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.disable_mira_dumps import DATA_KAFS_CODES
from arim.services import AISServices


class ArimViewSet(GenericViewSet):

    @action(methods=['GET'], url_path="kafs", detail=False)
    def get_caf_codes(self, request, *args, **kwargs):
        if settings.DISABLE_MIRA:
            data = DATA_KAFS_CODES
        else:
            data = AISServices.get_kaf_codes()

        return Response(data)
