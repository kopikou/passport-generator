from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from arim.services import AISServices


class AccreditationInfoViewSet(GenericViewSet):
    @action(methods=['GET'], url_path="ap1", detail=False)
    def get_ap1(self, requests, *args, **kwargs):
        data = AISServices.get_ap1(123)

        return Response(data)

    @action(methods=['GET'], url_path="ap2", detail=False)
    def get_ap2(self, requests, *args, **kwargs):
        data = AISServices.get_ap1(4335)

        return Response(data)