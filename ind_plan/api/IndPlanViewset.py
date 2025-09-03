from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from ind_plan.models import Work, PlanWorkType, IndPlan, PlanWork
from ind_plan.serializers import WorkSerializer, IndPlanSerializer, IndPlanListSerializer, PlanWorkSerializer, \
    PlanWorkAddUpdateSerializer, IndPlanUpdateSerializer
from ind_plan.services.indPlan_service import IndPlanService


class IndPlanViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = IndPlan.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return IndPlanSerializer
        elif self.action == "get_works":
            return WorkSerializer
        elif self.action in ["update"]:
            return IndPlanUpdateSerializer
        else:
            return IndPlanListSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        data = IndPlanService.get_indPlan(pk)
        serializer = IndPlanSerializer(data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        ind_plan = IndPlan.objects.create(
            user_created=self.request.user
        )

        serializer = IndPlanListSerializer(ind_plan)

        return Response(serializer.data)

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

class PlanWorkViewSet(
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = PlanWork.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return PlanWorkAddUpdateSerializer
        else:
            return PlanWorkSerializer