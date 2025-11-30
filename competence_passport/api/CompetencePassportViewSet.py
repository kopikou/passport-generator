from django.conf import settings
from app.disable_mira_dumps import DATA_GROUP_LIST, DATA_GROUPS_PROGRAM
from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework import status
from generator.services.generator_service import GeneratorService
from app.utils import UserProfileHasPermission
from auths.models import Permissions
from generator.permissions import CanViewRPDProgram
from rpd.models.rpd_models import PlanData, LinesData, LinesIndicators
import logging
logger = logging.getLogger(__name__)


class CompetencePassportViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]

    def get_queryset(self):
        return PlanData.objects.none()

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
        
    @action(methods=['GET'], detail=False, url_path='all-competences')
    def get_all_competences(self, request):
        """Получение всех компетенций для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем план по mira_id
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем ВСЕ линии (дисциплины) данного плана
            plan_lines = LinesData.objects.filter(plan=plan)
            
            # Получаем уникальные компетенции через индикаторы линий данного плана
            competences = LinesIndicators.objects.filter(
                planlineid__in=plan_lines,  # Фильтруем по линиям, принадлежащим плану
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence'
            ).distinct().order_by('competence_index')
            
            # Преобразуем в список словарей
            competences_list = [
                {
                    'id': f"{comp['competence_index']}_{hash(comp['competence'])}",
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                }
                for comp in competences
            ]
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'competences': competences_list
            })
            
        except Exception as e:
            logger.error(f"Error fetching competences for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['GET'], detail=False, url_path='all-disciplines')
    def get_all_disciplines(self, request):
        """Получение всех дисциплин для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем план по mira_id
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплины для данного плана
            disciplines = LinesData.objects.filter(
                plan=plan,  # Фильтруем по плану
                synchronize=True
            ).values(
                'id',
                'newdisid',
                'dis'
            ).order_by('newdisid')
            
            disciplines_list = [
                {
                    'id': disc['id'],
                    'newdisid': disc['newdisid'],
                    'dis': disc['dis']
                }
                for disc in disciplines
            ]
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'disciplines': disciplines_list
            })
            
        except Exception as e:
            logger.error(f"Error fetching disciplines for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении дисциплин: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )