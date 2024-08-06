from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from arim.services import AISServices


class ArimViewSet(GenericViewSet):

    @action(methods=['GET'], url_path="kafs", detail=False)
    def get_caf_codes(self, request, *args, **kwargs):
        data = AISServices.get_kaf_codes()

        return Response(data)
