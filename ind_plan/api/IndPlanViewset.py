import datetime

from psycopg.errors import RaiseException
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from arim.services import AISServices
from auths.models import UserProfile
from ind_plan.models import Work, PlanWorkType, IndPlan, PlanWork
from ind_plan.serializers import WorkSerializer, IndPlanSerializer, IndPlanListSerializer, PlanWorkSerializer, \
    PlanWorkAddUpdateSerializer, IndPlanUpdateSerializer
from ind_plan.services.indPlan_service import IndPlanService


class IndPlanViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
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

    def list(self, request, *args, **kwargs):
        current_year = IndPlanService.get_current_uch_year()

        current_plan = self.get_queryset().filter(year=current_year,
                                                  user_created=self.request.user).first()

        if current_plan is None:
            zav = AISServices.get_zav_to_plan(self.request.user.userprofile.mira_id)
            IndPlan.objects.create(
                user_created=self.request.user,
                year=current_year,
                zav=UserProfile.objects.get(mira_id=zav[0]['czav']).user
            )

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        data = IndPlanService.get_indPlan(pk)
        serializer = IndPlanSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-works')
    def get_works(self, request, *args, **kwargs):
        works = Work.objects.all()

        data = []
        for work in works:
            data.append({
                'id': work.id,
                'name': work.name,
                'hours_count': work.hours_count,
                'type': PlanWorkType[work.type],
                'type_name': work.type,
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