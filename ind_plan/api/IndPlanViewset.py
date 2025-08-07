from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from arim.models import UchNagr
from ind_plan.services.nagr_service import NagrService


class IndPlanViewSet(
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = UchNagr.objects.all()

    @action(detail=False, methods=['get'], url_path='self')
    def get_uch_nagr(self, request, *args, **kwargs):
        data = NagrService.get_nagr(self.request.user.userprofile.mira_id)
        return Response(data)