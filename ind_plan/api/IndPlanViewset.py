import datetime

from django.core.serializers import serialize
from django.db.models import Q
from psycopg.errors import RaiseException
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.decorators import action

from arim.services import AISServices
from auths.models import UserProfile
from ind_plan.models import Work, PlanWorkType, IndPlan, PlanWork
from ind_plan.serializers import WorkSerializer, IndPlanListSerializer, PlanWorkSerializer, \
    PlanWorkAddUpdateSerializer, IndPlanUpdateSerializer, IndPlanSerializer
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

        serializer = self.get_serializer(IndPlan.objects.filter(Q(user_created=self.request.user) | Q(zav=self.request.user)).all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        ind_plan = self.get_queryset().get(pk=pk)
        data = []
        if ind_plan is not None:
            data = PlanWork.objects.filter(plan=ind_plan.id).all()

        serializer = self.get_serializer({
            "plan": ind_plan,
            "works": data
        })
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-works')
    def get_works(self, request, *args, **kwargs):
        works = Work.objects.all()

        serializer = self.get_serializer(works, many=True)
        return Response(serializer.data)

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