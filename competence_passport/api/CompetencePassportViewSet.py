from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework import status
from competence_passport.services import CompetencePassportService
from app.utils import UserProfileHasPermission
from auths.models import Permissions
from generator.permissions import CanViewRPDProgram
from rpd.models.rpd_models import PlanData
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
        
        user_mira_id = self.request.user.userprofile.mira_id if hasattr(self.request.user, 'userprofile') else None
        res = CompetencePassportService.get_group_list(
            user_mira_id, 
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
            
            error_response = CompetencePassportService.validate_plan_id(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan, error_response = CompetencePassportService.get_plan_or_error_response(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            competences = CompetencePassportService.get_all_competences_for_plan(plan)
            sorted_competences = CompetencePassportService.sort_competences(competences)
            
            competences_list = [
                {
                    'id': f"{comp['competence_index']}_{hash(comp['competence'])}",
                    'competence_index': comp['competence_index'],
                    'competence': comp['competence']
                }
                for comp in sorted_competences
            ]
            
            return Response(CompetencePassportService.get_plan_response_data(plan, {
                'competences': competences_list
            }))
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['GET'], detail=False, url_path='all-disciplines')
    def get_all_disciplines(self, request):
        """Получение всех дисциплин для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            plan, disciplines_list, error_response = CompetencePassportService.get_all_disciplines_for_plan(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            return Response(CompetencePassportService.get_plan_response_data(plan, {
                'disciplines': disciplines_list
            }))
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении дисциплин: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-matrix')
    def get_competence_matrix(self, request):
        """Получение матрицы компетенций для конкретного учебного плана"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            plan, matrix_data, error_response = CompetencePassportService.get_competence_matrix(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            return Response(CompetencePassportService.get_plan_response_data(plan, {
                'matrix': matrix_data
            }))
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении матрицы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='discipline-competences-detailed')
    def get_discipline_competences_detailed(self, request):
        """Детальная информация о компетенциях дисциплины с индикаторами"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            discipline_id = self.request.query_params.get('discipline_id')
            
            result, error_response = CompetencePassportService.get_discipline_competences_detailed(plan_id, discipline_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            discipline = result['discipline']
            competences_list = result['competences_list']
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'discipline_id': discipline.id,
                'discipline_index': discipline.newdisid,
                'discipline_name': discipline.dis,
                'competences': competences_list,
                'current_kompetences': discipline.kompetences or ""
            })
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении детальной информации: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['POST'], detail=False, url_path='update-discipline-competences')
    def update_discipline_competences(self, request):
        """Обновление компетенций для дисциплины с выбранными компетенциями"""
        try:
            plan_id = request.data.get('plan_id')
            discipline_id = request.data.get('discipline_id')
            selected_competences = request.data.get('selected_competences', [])
            
            result, error_response = CompetencePassportService.update_discipline_competences(
                plan_id, discipline_id, selected_competences
            )
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            discipline = result['discipline']
            
            return Response({
                'success': True,
                'competences_deleted': result['comp_to_delete_sorted'],
                'competences_added': result['comp_to_add_sorted'],
                'competences_kept': result['comp_to_keep_sorted'],
                'discipline': {
                    'id': discipline.id,
                    'index': discipline.newdisid,
                    'name': discipline.dis
                }
            })
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['POST'], detail=False, url_path='update-semester-scheme')
    def update_semester_scheme(self, request):
        """Обновление схемы формы аттестации для компетенции в семестре"""
        try:
            plan_id = request.data.get('plan_id')
            discipline_id = request.data.get('discipline_id')
            competence_index = request.data.get('competence_index')
            semester = request.data.get('semester')
            forms = request.data.get('forms', {})
            
            result, error_response = CompetencePassportService.update_semester_scheme(
                plan_id, discipline_id, competence_index, semester, forms
            )
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            return Response({
                'success': True,
                'scheme_id': result['scheme_id'],
                'created': result['created'],
                'forms_display': result['forms_display'],
                'has_forms': result['has_forms'],
                'message': 'Схема успешно обновлена'
            })
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении схемы: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(methods=['GET'], detail=False, url_path='competence-schema-data')
    def get_competence_schema_data(self, request):
        """Получение данных для схемы компетенций с формами аттестации"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            plan, schema_data, error_response = CompetencePassportService.get_competence_schema_data(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            return Response(CompetencePassportService.get_plan_response_data(plan, schema_data))
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении данных схемы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='plan-details')
    def get_plan_details(self, request):
        """Получение детальной информации о плане для титульного листа"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            user_mira_id = self.request.user.userprofile.mira_id if hasattr(self.request.user, 'userprofile') else None
            result, error_response = CompetencePassportService.get_plan_details(plan_id, user_mira_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            plan_data = result['plan_data']
            
            response_data = {
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'abbrprofile': plan.abbrprofile,
                'admission': plan_data['admission'],
                'planlines': plan_data['planlines'],
                'caf_name': plan_data['caf_name'],
                'plx_file': plan_data['plx_file'],
            }
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении данных плана: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-relations')
    def get_competence_relations(self, request):
        """Получение связей компетенции с другими компетенциями"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            result, error_response = CompetencePassportService.get_competence_relations(plan_id, competence_index)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': result['competence_index'],
                'competence': result['competence'],
                'relations': result['relations'],
                'created': result['created']
            })
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении связей компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='update-competence-relations')
    def update_competence_relations(self, request):
        """Обновление связей компетенции с другими компетенциями"""
        try:
            plan_id = request.data.get('plan_id')
            competence_index = request.data.get('competence_index')
            relations_text = request.data.get('relations_text', '')
            
            result, error_response = CompetencePassportService.update_competence_relations(
                plan_id, competence_index, relations_text
            )
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            return Response({
                'success': True,
                'message': 'Связи компетенции успешно обновлены',
                'competence_index': result['competence_index'],
                'relations': result['relations'],
                'created': result['created'],
                'updated_at': result['updated_at']
            })
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении связей компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['GET'], detail=False, url_path='competence-final-indicators')
    def get_competence_final_indicators(self, request):
        """Получение итоговых индикаторов достижения компетенции"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            result, error_response = CompetencePassportService.get_competence_final_indicators(plan_id, competence_index)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': result['competence_index'],
                'competence': result['competence'],
                'primary_indicator': result['primary_indicator'],
                'all_indicators': result['all_indicators'],
                'final_indicators_count': result['final_indicators_count'],
                'total_indicators_count': result['total_indicators_count']
            })
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении итоговых индикаторов компетенции: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='update-competence-final-indicators')
    def update_competence_final_indicators(self, request):
        """Обновление итоговых индикаторов компетенции"""
        try:
            plan_id = request.data.get('plan_id')
            competence_index = request.data.get('competence_index')
            final_indicator_text = request.data.get('final_indicator_text', '')
            indicator_id = request.data.get('indicator_id') 
            
            result, error_response = CompetencePassportService.update_competence_final_indicators(
                plan_id, competence_index, final_indicator_text, indicator_id
            )
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            indicator = result['indicator']
            
            if result['updated']:
                message = f'Итоговый индикатор "{indicator.indicator_index}" успешно обновлен'
            else:
                message = f'Создан новый итоговый индикатор "{indicator.indicator_index}"'
            
            return Response({
                'success': True,
                'message': message,
                'indicator_id': indicator.id,
                'indicator_index': indicator.indicator_index,
                'updated': result['updated'],
                'created': result.get('created', False)
            })
                    
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении итоговых индикаторов: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='competence-indicator-disciplines')
    def get_competence_indicator_disciplines(self, request):
        """Получение индикаторов компетенции с привязкой к дисциплинами"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            competence_index = self.request.query_params.get('competence_index')
            
            result, error_response = CompetencePassportService.get_competence_indicator_disciplines(plan_id, competence_index)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            
            return Response({
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname,
                'competence_index': result['competence_index'],
                'competence': result['competence'],
                'table_data': result['table_data'],
            })
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении индикаторов с дисциплинами: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['POST'], detail=False, url_path='update-indicator-content')
    def update_indicator_content(self, request):
        """Обновление содержания индикатора"""
        try:
            indicator_id = request.data.get('indicator_id')
            new_content = request.data.get('indicator_content', '').strip()
            
            result, error_response = CompetencePassportService.update_indicator_content(indicator_id, new_content)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            indicator = result['indicator']
            plan = result['plan']
            
            return Response({
                'success': True,
                'message': 'Содержание индикатора успешно обновлено',
                'indicator': {
                    'id': indicator.id,
                    'indicator_index': indicator.indicator_index,
                    'indicator_content': indicator.indicator,
                    'competence_index': indicator.competence_index,
                    'discipline_id': indicator.planlineid.id,
                    'discipline_name': indicator.planlineid.dis,
                    'discipline_index': indicator.planlineid.newdisid,
                },
                'plan_id': plan.id,
                'plan_mira_id': plan.mira_id,
                'plan_name': plan.planname
            })
                    
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении содержания индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='indicator-details')
    def get_indicator_details(self, request):
        """Получение деталей индикатора (знать/уметь/владеть)"""
        try:
            indicator_id = self.request.query_params.get('indicator_id')
            
            result, error_response = CompetencePassportService.get_indicator_details(indicator_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            indicator = result['indicator']
            
            response_data = {
                'know': result['know'],
                'able': result['able'],
                'own': result['own'],
                'criteria': result['criteria'],
                'methods': result['methods'],
            }

            response_data.update({
                'indicator_id': indicator.id,
                'indicator_index': indicator.indicator_index,
                'indicator_content': indicator.indicator,
                'competence_index': indicator.competence_index,
                'discipline_id': indicator.planlineid.id,
                'discipline_name': indicator.planlineid.dis,
                'discipline_index': indicator.planlineid.newdisid,
            })
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при получении деталей индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(methods=['POST'], detail=False, url_path='save-indicator-details')
    def save_indicator_details(self, request):
        """Сохранение деталей индикатора (знать/уметь/владеть)"""
        try:
            indicator_id = request.data.get('indicator_id')
            know = request.data.get('know', '')
            able = request.data.get('able', '')
            own = request.data.get('own', '')
            criteria = request.data.get('criteria', '')
            methods = request.data.get('methods', '')
            
            result, error_response = CompetencePassportService.save_indicator_details(
                indicator_id, know, able, own, criteria, methods
            )
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            discipline_indicator = result['discipline_indicator']
            indicator = result['indicator']
            
            return Response({
                'success': True,
                'message': 'Данные индикатора успешно сохранены',
                'created': result['created'],
                'indicator': {
                    'id': indicator.id,
                    'indicator_index': indicator.indicator_index,
                    'indicator_content': indicator.indicator,
                    'competence_index': indicator.competence_index,
                    'know': discipline_indicator.know,
                    'able': discipline_indicator.able,
                    'own': discipline_indicator.own,
                    'criteria': discipline_indicator.criteria,
                    'methods': discipline_indicator.methods,
                    'updated_at': discipline_indicator.updated_at
                }
            })
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка при сохранении данных индикатора: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(methods=['GET'], detail=False, url_path='validate-scheme-indicators')
    def validate_scheme_indicators(self, request):
        """Проверка соответствия промежуточных аттестаций и индикаторов"""
        try:
            plan_id = self.request.query_params.get('plan_id')
            
            result, error_response = CompetencePassportService.validate_scheme_indicators(plan_id)
            if error_response:
                return Response(
                    {'error': error_response['error']}, 
                    status=error_response['status']
                )
            
            plan = result['plan']
            
            return Response(CompetencePassportService.get_plan_response_data(plan, {
                'validation_errors': result['validation_errors'],
                'has_errors': result['has_errors'],
                'errors_count': result['errors_count'],
                'checked_at': result['checked_at']
            }))
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка при проверке схемы компетенций: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )