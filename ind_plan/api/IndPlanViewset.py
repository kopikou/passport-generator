from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

import ind_plan
from arim.models import UchNagr
from ind_plan.models import Work, PlanWorkType
from ind_plan.serializers import WorkSerializer
from ind_plan.services.indPlan_service import IndPlanService


class IndPlanViewSet(
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = UchNagr.objects.all()
    serializer_class = WorkSerializer

    @action(detail=False, methods=['get'], url_path='self')
    def get_indPlan(self, request, *args, **kwargs):
        data = IndPlanService.get_indPlan(self.request.user)
        return Response(data)

    @action(detail=False, methods=['get'], url_path='preparing_coefficients')
    def get_preparing_coefficients(self, request, *args, **kwargs):
        coefficients_for_new = {
            'labs_and_practices': 2,
            'lectures': 3,
        }

        coefficients_for_old = {
            'labs_and_practices': 0.5,
            'lectures': 1,
        }

        general_coefficients = {
            'check_labs': 0.2,
        }

        return Response(data = {
            'coefficients_for_new': coefficients_for_new,
            'coefficients_for_old': coefficients_for_old,
            'general_coefficients': general_coefficients,
        })

    @action(detail=False, methods=['get'], url_path='get-works')
    def get_works(self, request, *args, **kwargs):
        work_type = self.request.GET.get('type')
        works = Work.objects.all().filter(type=work_type)

        data = []
        for work in works:
            data.append({
                'id': work.id,
                'name': work.name,
                'hours_count': work.hours_count,
                'type': PlanWorkType[work.type],
            })

        return Response(data = data)