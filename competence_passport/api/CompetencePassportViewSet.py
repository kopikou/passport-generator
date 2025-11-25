from django.conf import settings
from app.disable_mira_dumps import DATA_GROUP_LIST, DATA_GROUPS_PROGRAM

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework import status
from generator.services.generator_service import GeneratorService
from app.utils import UserProfileHasPermission
from auths.models import Permissions
from generator.permissions import CanViewRPDProgram

class CompetencePassportViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]

    @action(methods=['GET'], detail=False, url_path='group-list')
    def get_group_list(self, request, *args, **kwargs):
        txt_filter = self.request.query_params.get('text')
        group_txt_filter = self.request.query_params.get('groupText')
        status_filter = self.request.query_params.get('status')
        my_filter = self.request.query_params.get('my')
        year_filter = self.request.query_params.get('year')

        if settings.DISABLE_MIRA:
           res = DATA_GROUP_LIST
        else:
            res = GeneratorService.get_group_list(
                self.request.user.userprofile.mira_id, 
                year_filter, 
                txt_filter,
                group_txt_filter, 
                status_filter, 
                my_filter
            )

        return Response(data=res)

    @action(methods=['POST'], detail=True, url_path='upload-plan')
    def upload_plan_file(self, request, pk=None):
        """
        Загрузка нового файла учебного плана
        """
        plan_file = request.FILES.get('plan_file')
        if not plan_file:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        

        
        return Response({
            'message': 'Файл успешно загружен',
            'file_url': 'url_to_saved_file'  
        })

    @action(methods=['POST'], detail=True, url_path='select-plan')
    def select_plan_file(self, request, pk=None):
        """
        Выбор существующего файла учебного плана
        """
        file_id = request.data.get('file_id')
        if not file_id:
            return Response({'error': 'ID файла не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        

        return Response({'message': 'Учебный план успешно выбран'})

    @action(methods=['GET'], detail=True, url_path='available-plans')
    def get_available_plans(self, request, pk=None):
        """
        Получение списка доступных учебных планов
        """

        available_plans = [
            {
                'id': 1,
                'name': 'Учебный план 2025',
                'url': '/uploads/plans/plan_2025.plx',
                'date': '2025-04-07'
            }
        ]
        
        return Response(available_plans)