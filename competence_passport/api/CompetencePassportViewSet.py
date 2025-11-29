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
    
    @action(methods=['GET'], detail=True, url_path='competences')
    def get_plan_competences(self, request, pk=None):
        """
        Получение всех компетенций для учебного плана
        """
        try:
            
            # Используем DUMP данные если MIRA отключена
            if settings.DISABLE_MIRA:
                plan_data = DATA_GROUPS_PROGRAM
            else:
                plan_data = GeneratorService.get_group_program(pk, self.request.user.userprofile.mira_id)
            
            if not plan_data:
                return Response(
                    {'error': 'Учебный план не найден или нет доступа'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем первый элемент (основной план)
            main_plan = plan_data[0] if plan_data else None
            
            if not main_plan:
                return Response(
                    {'error': 'Данные плана не найдены'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем ID плана из данных
            plan_id = main_plan.get('plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан в данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Теперь получаем компетенции через существующие модели
            return self._get_competences_by_plan_id(plan_id)
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_competences_by_plan_id(self, plan_id):
        """Вспомогательный метод для получения компетенций по ID плана"""
        try:
            plan = PlanData.objects.get(mira_id=plan_id)
            
            # Получаем все линии плана с индикаторами компетенций
            lines_with_indicators = LinesData.objects.filter(
                plan=plan
            ).prefetch_related(
                Prefetch(
                    'indicators',
                    queryset=LinesIndicators.objects.all().order_by('competence_index', 'indicator_index')
                )
            ).select_related('disid')
            
            lines_count = lines_with_indicators.count()
            
            # Формируем структуру данных
            competences_data = []
            
            for line in lines_with_indicators:
                line_data = {
                    'discipline_id': line.id,
                    'discipline_name': line.dis,
                    'discipline_code': line.newdisid,
                    'competences': []
                }
                
                # Группируем индикаторы по компетенциям
                competence_groups = {}
                indicators_count = line.indicators.count()
                
                for indicator in line.indicators.all():
                    if indicator.competence and indicator.competence_index:
                        comp_key = f"{indicator.competence_index}_{indicator.competence}"
                        if comp_key not in competence_groups:
                            competence_groups[comp_key] = {
                                'competence_index': indicator.competence_index,
                                'competence_name': indicator.competence,
                                'indicators': []
                            }
                        
                        competence_groups[comp_key]['indicators'].append({
                            'indicator_index': indicator.indicator_index,
                            'indicator_name': indicator.indicator
                        })
                
                # Преобразуем в список
                line_data['competences'] = list(competence_groups.values())
                competences_data.append(line_data)
            
            return Response({
                'plan_id': plan.id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'startyear': plan.startyear,
                'competences': competences_data
            })
            
        except PlanData.DoesNotExist:
            return Response(
                {'error': 'Учебный план не найден в базе данных'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении компетенций из базы: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # @action(methods=['POST'], detail=True, url_path='upload-plan')
    # def upload_plan_file(self, request, pk=None):
    #     """
    #     Загрузка нового файла учебного плана
    #     """
    #     plan_file = request.FILES.get('plan_file')
    #     if not plan_file:
    #         return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        

        
    #     return Response({
    #         'message': 'Файл успешно загружен',
    #         'file_url': 'url_to_saved_file'  
    #     })

    # @action(methods=['POST'], detail=True, url_path='select-plan')
    # def select_plan_file(self, request, pk=None):
    #     """
    #     Выбор существующего файла учебного плана
    #     """
    #     file_id = request.data.get('file_id')
    #     if not file_id:
    #         return Response({'error': 'ID файла не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        

    #     return Response({'message': 'Учебный план успешно выбран'})

    # @action(methods=['GET'], detail=True, url_path='available-plans')
    # def get_available_plans(self, request, pk=None):
    #     """
    #     Получение списка доступных учебных планов
    #     """

    #     available_plans = [
    #         {
    #             'id': 1,
    #             'name': 'Учебный план 2025',
    #             'url': '/uploads/plans/plan_2025.plx',
    #             'date': '2025-04-07'
    #         }
    #     ]
        
    #     return Response(available_plans)