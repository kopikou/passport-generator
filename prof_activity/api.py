from itertools import groupby

from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from django.http import JsonResponse, HttpRequest

from prof_activity.models import AreasProfActivity, TypeProfActivity, Areas2PlanProfActivity, Type2PlanProfActivity
from prof_activity.serializer import Areas2PlanProfActivitySerializer, Type2PlanProfActivitySerializer
from uplfile.service import UploadFileService


class ProfActivityViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = None
    serializer_class = None

    @action(methods=['GET'], url_path="get-admission-data", detail=False)
    def get_admission_data(self, request, *args, **kwargs):
        mira_id = self.request.user.userprofile.mira_id
        res = UploadFileService.get_admission_data(mira_id)

        mira_ids = [i['id'] for i in res]

        areas = Areas2PlanProfActivity.objects.filter(plan_mira_id__in=mira_ids).values()
        areas_sorted = sorted(areas, key=lambda x: x['plan_mira_id'])
        areas_grouped = {key: list(items) for key, items in groupby(areas_sorted, key=lambda x: x['plan_mira_id'])}
        types = Type2PlanProfActivity.objects.filter(plan_mira_id__in=mira_ids).values()
        types_sorted = sorted(types, key=lambda x: x['plan_mira_id'])
        types_grouped = {key: list(items) for key, items in groupby(types_sorted, key=lambda x: x['plan_mira_id'])}

        data = []

        for i in res:
            data.append({
                **i,
                "areas": areas_grouped.get(i['id'], []),
                "types": types_grouped.get(i['id'], [])
            })

        return Response(data)

    @action(methods=['GET'], url_path="get-areas-activity", detail=False)
    def get_areas_activity(self, request, *args, **kwargs):
        res = AreasProfActivity.objects.all().values()
        return Response(data=[i for i in res])

    @action(methods=['GET'], url_path="get-types-activity", detail=False)
    def get_types_activity(self, request, *args, **kwargs):
        res = TypeProfActivity.objects.all().values()
        return Response([i for i in res], status=status.HTTP_200_OK)


    @action(methods=['POST'], url_path="save-areas-data", detail=False)
    def save_areas_data(self, request, *args, **kwargs):
        data = {
            'area': self.request.data['area'],
            'plan_mira_id': self.request.data['plan_mira_id'],
            'user_mira_id': self.request.user.userprofile.mira_id,
        }

        data_serializer = Areas2PlanProfActivitySerializer(data=data)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.save()

        return Response(data_serializer.data)

    @action(methods=['POST'], url_path="save-types-data", detail=False)
    def save_types_data(self, request, *args, **kwargs):
        data = {
            'type': self.request.data['type'],
            'plan_mira_id': self.request.data['plan_mira_id'],
            'user_mira_id': self.request.user.userprofile.mira_id,
        }

        data_serializer = Type2PlanProfActivitySerializer(data=data)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.save()

        return Response(data_serializer.data)

    @action(methods=['POST'], url_path="remove-area-data", detail=True)
    def remove_area_data(self, request, *args, **kwargs):
        instance = Areas2PlanProfActivity.objects.get(id=self.kwargs['pk'])
        instance.delete()
        return Response(
            data={"success": "True"},
            status=status.HTTP_200_OK,
        )


    @action(methods=['POST'], url_path="remove-type-data", detail=True)
    def remove_type_data(self, request, *args, **kwargs):
        instance = Type2PlanProfActivity.objects.get(id=self.kwargs['pk'])
        instance.delete()
        return Response(
            data={"success": "True"},
            status=status.HTTP_200_OK,
        )
