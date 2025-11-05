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
from ind_plan.models import Work, PlanWorkType, IndPlan, PlanWork, IndPlanTemplate
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
        elif self.action in ["update"]:
            return IndPlanUpdateSerializer
        else:
            return IndPlanListSerializer

    def _get_active_template(self):
        return IndPlanTemplate.objects.filter(is_active=True).order_by("-id").first()

    def list(self, request, *args, **kwargs):
        current_year = IndPlanService.get_current_uch_year()
        active_template = self._get_active_template()

        current_plan = IndPlan.objects.filter(
            year=current_year,
            template_id=active_template.id,
            user_created=self.request.user
        ).first()

        if not current_plan:
            zav = AISServices.get_zav_to_plan(self.request.user.userprofile.mira_id)
            IndPlan.objects.create(
                user_created=self.request.user,
                year=current_year,
                template_id=active_template.id,
                zav=UserProfile.objects.get(mira_id=zav[0]['czav']).user
            )

        query = IndPlan.objects.filter(
            Q(user_created=self.request.user)
            | Q(zav=self.request.user)
        ).all()
        serializer = self.get_serializer(query, many=True)
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

    @action(detail=True, methods=['get'], url_path='works')
    def get_works(self, request, *args, **kwargs):
        ind_plan = self.get_object()
        works = Work.objects.filter(
            template_id=ind_plan.template_id,
        ).order_by("order")

        serializer = WorkSerializer(works, many=True)

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