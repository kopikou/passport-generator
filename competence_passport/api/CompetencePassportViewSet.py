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
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплины
            plan_lines = LinesData.objects.filter(plan=plan)
            
            # Получаем уникальные компетенции 
            competences = LinesIndicators.objects.filter(
                planlineid__in=plan_lines, 
                competence__isnull=False,
                competence_index__isnull=False
            ).values(
                'competence_index',
                'competence'
            ).distinct().order_by('competence_index')
            
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
            
            # Получаем план
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем дисциплины БЕЗ фильтрации по synchronize
            disciplines = LinesData.objects.filter(
                plan=plan
            ).values(
                'id',
                'newdisid',
                'dis',
                'synchronize'
            ).order_by('newdisid')
            
            disciplines_list = [
                {
                    'id': disc['id'],
                    'newdisid': disc['newdisid'],
                    'dis': disc['dis'],
                    'synchronize': disc['synchronize']
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
        
    @action(methods=['GET'], detail=False, url_path='competence-matrix')
    def get_competence_matrix(self, request):
        """Получение матрицы компетенций для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            if not plan_id:
                return Response(
                    {'error': 'ID плана не указан'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                plan = PlanData.objects.get(mira_id=plan_id)
            except PlanData.DoesNotExist:
                return Response(
                    {'error': 'Учебный план не найден в базе данных'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Получаем все дисциплины плана
            disciplines = LinesData.objects.filter(
                plan=plan
            ).prefetch_related(
                Prefetch(
                    'indicators',
                    queryset=LinesIndicators.objects.filter(
                        competence__isnull=False,
                        competence_index__isnull=False
                    ).only('competence_index', 'competence')
                )
            ).order_by('newdisid')
            
            # Создаем словарь для группировки дисциплин по префиксам
            groups = {}
            
            # Определяем названия для основных групп
            group_names = {
                'Б1': 'Дисциплины (модули)',
                'Б1.Б': 'Обязательная часть',
                'Б1.Б.01': 'Общеобразовательный модуль',
                'Б1.Б.02': 'Фундаментальный модуль',
                'Б1.Б.03': 'Базовый модуль направления',
                'Б1.Б.04': 'Модуль проектной деятельности',
                'Б1.Б.05': 'Модуль по физической культуре и спорту',
                'Б1.В': 'Вариативная часть',
                'Б1.В.01': 'Модуль проектной деятельности',
                'Б1.В.02': 'Модуль профильной подготовки',
                'Б1.В.03': 'Модуль дополнительного профиля',
                'Б2': 'Практика',
                'Б2.Б': 'Обязательная часть',
                'Б2.В': 'Вариативная часть',
                'Б3': 'Государственная итоговая аттестация',
                'ФТД': 'Факультативы'
            }
            
            for discipline in disciplines:
                if not discipline.newdisid:
                    continue
                
                # Получаем компетенции для этой дисциплины
                discipline_competences = set()
                for indicator in discipline.indicators.all():
                    if indicator.competence_index:
                        discipline_competences.add(indicator.competence_index)
                
                # Добавляем дисциплину в матрицу
                disc_key = discipline.newdisid
                if disc_key not in groups:
                    groups[disc_key] = {
                        'type': 'discipline',
                        'index': disc_key,
                        'name': discipline.dis,
                        'competences': discipline_competences,
                        'level': disc_key.count('.') + 1 if '.' in disc_key else 1
                    }
                
                # Добавляем компетенции ко всем родительским группам
                parts = disc_key.split('.')
                for i in range(len(parts)):
                    group_key = '.'.join(parts[:i+1])
                    
                    # Определяем базовую группу для ключа
                    base_group_key = group_key
                    if base_group_key.startswith('Б1.Б.05.02'):
                        base_group_key = 'Б1.Б.05'
                    elif base_group_key.startswith('Б1.В.02.ДВ'):
                        base_group_key = 'Б1.В.02'
                    elif base_group_key.startswith('Б1.В.ДВ'):
                        base_group_key = 'Б1.В'
                    
                    if base_group_key not in groups:
                        groups[base_group_key] = {
                            'type': 'group',
                            'index': base_group_key,
                            'name': group_names.get(base_group_key, base_group_key),
                            'competences': set(),
                            'level': base_group_key.count('.') + 1 if '.' in base_group_key else 1
                        }
                    
                    # Добавляем компетенции к группе
                    groups[base_group_key]['competences'].update(discipline_competences)
            
            matrix_data = []
            for item in groups.values():
                sorted_competences = sorted(list(item['competences']))
                indices_str = ", ".join(sorted_competences)
                
                matrix_data.append({
                    'type': item['type'], 
                    'level': item['level'],  
                    'index': item['index'],
                    'name': item['name'],
                    'competence_indices': indices_str,
                    'competence_indices_list': sorted_competences
                })
            
            def sort_key(x):
                type_order = 0 if x['type'] == 'group' else 1
                return (type_order, x['index'])
            
            matrix_data.sort(key=sort_key)
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'matrix': matrix_data
            })
            
        except Exception as e:
            logger.error(f"Error fetching competence matrix for plan {plan_id}: {str(e)}")
            return Response(
                {'error': f'Ошибка при получении матрицы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )