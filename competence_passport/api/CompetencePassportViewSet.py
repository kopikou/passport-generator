from django.conf import settings
from app.disable_mira_dumps import DATA_GROUPS_PROGRAM, DATA_GROUP_LIST
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from app.utils import UserProfileHasPermission
from auths.models import Permissions
from generator.permissions import CanViewRPDProgram
from competence_passport.permissions import CanViewCompetencePassport, CanEditCompetencePassport
from rpd.models.rpd_models import PlanData, LinesIndicators, SemesterData
from generator.models import DisciplineIndicators
from competence_passport.services.matrixService import MatrixService
from competence_passport.services.schemaService import SchemaService
from competence_passport.services.passportService import PassportService
from competence_passport.services.ruleService import RuleService
from competence_passport.services.competencePassportDataService import CompetencePassportDataService
from competence_passport.serializer import CompetencePassportDataSerializer, IndicatorsSerializer,\
    UpdateDisciplineCompetencesSerializer, SchemeUpdateSerializer, CompetenceRelationsSerializer,\
    FinalIndicatorUpdateSerializer, IndicatorDetailsSerializer, IndicatorSerializer, FixSchemaSerializer, \
    PlanAdmissionInfoSerializer, ReferenceDataSerializer, MatrixDataSerializer, SchemaDataSerializer, PassportDataSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from collections import defaultdict

class CompetencePassportViewSet(GenericViewSet):
    """
    ViewSet для матрицы, схемы и паспорта компетенций
    """
    queryset = PlanData.objects.none()
    serializer_class = CompetencePassportDataSerializer
    #permission_classes = [UserProfileHasPermission(Permissions.can_use_generator) and CanViewRPDProgram]
    permission_classes = [UserProfileHasPermission(Permissions.can_use_competence_passport_generator) and CanViewCompetencePassport]

    # def retrieve(self, request, *args, **kwargs):
    #     plan_id = self.kwargs['pk']

    #     result = CompetencePassportDataService.get_competence_passport_data(plan_id)
            
    #     serializer = self.get_serializer(data=result)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.validated_data)

    @action(methods=['GET'], detail=True, url_path="get-plan-admission", permission_classes=[IsAuthenticated])
    def get_plan_admission_info(self, request, *args, **kwargs):
        """Получение данных о плане"""
        plan_id = self.kwargs['pk']

        result = CompetencePassportDataService.get_plan_admission_data(plan_id)

        serializer = PlanAdmissionInfoSerializer(data=result)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data)

    @action(methods=['GET'], url_path="get-group-list", detail=False, permission_classes=[IsAuthenticated])
    def get_group_list(self, request, *args, **kwargs):
        """Получение данных о группе"""
        group_txt_filter = self.request.query_params.get('groupText')
        year_filter = self.request.query_params.get('year')

        if settings.DISABLE_MIRA:
            res = DATA_GROUP_LIST
        else:
            res = CompetencePassportDataService.get_group_list(self.request.user.userprofile.mira_id, year_filter, group_txt_filter)

        return Response(
            data=res,
        )
    
    @action(methods=['GET'], detail=True, url_path="get-reference-data", permission_classes=[IsAuthenticated])
    def get_reference_data(self, request, *args, **kwargs):
        """Получение данных справочников"""
        plan_id = self.kwargs['pk']

        result = CompetencePassportDataService.get_reference_data(plan_id)

        serializer = ReferenceDataSerializer(data=result)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data)
    
    @action(methods=['GET'], detail=True, url_path="get-matrix-data", permission_classes=[IsAuthenticated])
    def get_matrix_data(self, request, *args, **kwargs):
        """Получение данных матрицы компетенций"""
        plan_id = self.kwargs['pk']

        result = CompetencePassportDataService.get_matrix_data(plan_id)

        serializer = MatrixDataSerializer(data=result)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data)
    
    @action(methods=['GET'], detail=True, url_path="get-schema-data", permission_classes=[IsAuthenticated])
    def get_schema_data(self, request, *args, **kwargs):
        """Получение данных схемы компетенций"""
        plan_id = self.kwargs['pk']

        result = CompetencePassportDataService.get_schema_data(plan_id)

        serializer = SchemaDataSerializer(data=result)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data)
    
    @action(methods=['GET'], detail=True, url_path="get-passport-data", permission_classes=[IsAuthenticated])
    def get_passport_data(self, request, *args, **kwargs):
        """Получение данных паспорта компетенций"""
        plan_id = self.kwargs['pk']

        result = CompetencePassportDataService.get_passport_data(plan_id)

        serializer = PassportDataSerializer(data=result)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.validated_data)
    
    @action(methods=['POST'], detail=False, url_path='update-discipline-competences', permission_classes=[CanEditCompetencePassport])
    def update_discipline_competences(self, request, *args, **kwargs):
        """Обновление связей между дисуиплинами и компетенцями"""
        serializer = UpdateDisciplineCompetencesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = MatrixService.update_discipline_competences(
            plan_id=serializer.validated_data['plan_id'],
            discipline_id=serializer.validated_data['discipline_id'],
            selected_competences=serializer.validated_data['selected_competences']
        )
        discipline = result['discipline']
        return Response({
            'success': True,
            'competences_deleted': result['deleted'],
            'competences_added': result['added'],
            'competences_kept': result['kept'],
            'discipline': {
                'id': discipline.id,
                'index': discipline.newdisid,
                'name': discipline.dis
            }
        })
    
    @action(methods=['GET'], detail=True, url_path='validate-matrix', permission_classes=[IsAuthenticated])
    def validate_matrix(self, request, *args, **kwargs):
        """Валидация матрицы"""
        plan_id = self.kwargs['pk']
        result = MatrixService.validate_competence_matrix(plan_id=plan_id)
        
        return Response(result)

    
    @action(methods=['POST'], detail=False, url_path='update-semester-scheme', permission_classes=[CanEditCompetencePassport])
    def update_semester_scheme(self, request, *args, **kwargs):
        """Обновление схемы формирования"""
        serializer = SchemeUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = SchemaService.update_semester_scheme(
            plan_id=serializer.validated_data['plan_id'],
            discipline_id=serializer.validated_data['discipline_id'],
            competence_index=serializer.validated_data['competence_index'],
            competence=serializer.validated_data['competence'],
            semester=serializer.validated_data['semester'],
            forms=serializer.validated_data['forms']
        )

        return Response({
            'success': True,
            'scheme_id': result['scheme_id'],
            'created': result['created'],
            'has_forms': result['has_forms']
        })
    
    @action(methods=['GET'], detail=True, url_path="get-semester-data", permission_classes=[IsAuthenticated])
    def get_semester_data(self, request, *args, **kwargs):
        """Получение данных о семестрах для всех дисциплин плана"""
        plan_id = self.kwargs['pk']
        
        semester_data = SemesterData.objects.filter(
            planlineid__plan__mira_id=plan_id
        ).values(
            'planlineid_id',
            'num'
        )

        result = defaultdict(list)
        for item in semester_data:
            result[item['planlineid_id']].append(item['num'])
        
        return Response(dict(result))

    @action(methods=['GET'], detail=True, url_path='validate-scheme-indicators', permission_classes=[IsAuthenticated])
    def validate_scheme_indicators(self, request, *args, **kwargs):
        """Проверка соответствия промежуточных аттестаций и индикаторов"""
        plan_id = self.kwargs['pk']

        result = SchemaService.validate_scheme_indicators(plan_id=plan_id)
        return Response(result)


    @action(methods=['POST'], detail=False, url_path='fix-scheme-indicators', permission_classes=[CanEditCompetencePassport])
    def fix_scheme_indicators(self, request, *args, **kwargs):
        """Автоматическое исправление индикаторов при несоответствии с формами аттестации"""
        serializer = FixSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        result = SchemaService.fix_scheme_indicators(
            plan_id=validated_data['plan_id'],
            discipline_id=validated_data['discipline_id'],
            competence_index=validated_data['competence_index'],
            scheme_forms_count=validated_data['scheme_forms_count'],
        )
        return Response(result)

    @action(methods=['POST'], detail=False, url_path='update-competence-relations', permission_classes=[CanEditCompetencePassport])
    def update_competence_relations(self, request, *args, **kwargs):
        """Обновление связи компетенций в паспорте"""
        serializer = CompetenceRelationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return Response(CompetenceRelationsSerializer(instance).data)
    

    @action(methods=['POST'], detail=False, url_path='update-competence-final-indicators', permission_classes=[CanEditCompetencePassport])
    def update_competence_final_indicators(self,request, *args, **kwargs):
        """Обновление итогового индикатора"""
        serializer = FinalIndicatorUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        result = PassportService.update_competence_final_indicator(
            plan_id=validated_data['plan_id'],
            competence_index=validated_data['competence_index'],
            final_indicator_text=validated_data['final_indicator_text'],
        )

        indicator = result['indicator']
        
        return Response({
            'success': True,
            #'indicator_index': indicator.indicator_index,
            'final_indicator_text': indicator
        })
    
    @action(methods=['POST'], detail=False, url_path='update-indicator-details', permission_classes=[CanEditCompetencePassport])
    def update_indicator_details(self, request, *args, **kwargs):
        """Обновление деталей индикаторов"""
        input_serializer = IndicatorDetailsSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        discipline_indicator = PassportService.update_indicator_details(
            indicator_id=validated_data['indicator_id'],
            know=validated_data.get('know', ""),
            able=validated_data.get('able', ""),
            own=validated_data.get('own', ""),
            criteria=validated_data.get('criteria', ""),
            methods=validated_data.get('methods', "")
        )

        indicator = discipline_indicator.indicator
        output_data = {
            'indicator_index': indicator.indicator_index,
            'indicator': indicator.indicator,
            'know': discipline_indicator.know,
            'able': discipline_indicator.able,
            'own': discipline_indicator.own,
            'criteria': discipline_indicator.criteria,
            'methods': discipline_indicator.methods,
        }

        return Response(IndicatorSerializer(output_data).data)
    
    @action(methods=['POST'], detail=False, url_path='create-indicator', permission_classes=[CanEditCompetencePassport])
    def create_indicator(self, request, *args, **kwargs):
        serializer = IndicatorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        indicator = serializer.save()
        return Response(IndicatorsSerializer(indicator).data)
    
    @action(methods=['PUT'], detail=True, url_path='update-indicator', permission_classes=[CanEditCompetencePassport])
    def update_indicator(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        indicator = LinesIndicators.objects.get(id=pk)
        serializer = IndicatorsSerializer(indicator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(IndicatorsSerializer(updated).data)
    
    @action(methods=['DELETE'], detail=True, url_path='delete-indicator', permission_classes=[CanEditCompetencePassport])
    def delete_indicator(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        indicator = LinesIndicators.objects.get(id=pk)
        discipline = indicator.planlineid

        DisciplineIndicators.objects.filter(indicator=indicator).delete()

        indicator.delete()
        RuleService.update_discipline_kompetences(discipline)

        return Response({'success': True})
    
    @action(methods=['GET'], detail=True, url_path='get-matrix-report', permission_classes=[IsAuthenticated])
    def get_matrix_report(self, request, *args, **kwargs):
        """Экспорт матрицы компетенций в Word"""
        plan_id = self.kwargs['pk']

        doc_content = CompetencePassportDataService.get_matrix_report(plan_id, format_type='docx')

        response = HttpResponse(
            doc_content,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        #response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @action(methods=['GET'], detail=True, url_path='get-matrix-report-pdf', permission_classes=[IsAuthenticated])
    def get_matrix_report_pdf(self, request, *args, **kwargs):
        """Экспорт матрицы компетенций в PDF"""
        plan_id = self.kwargs['pk']
        
        pdf_content = CompetencePassportDataService.get_matrix_report(plan_id, format_type='pdf')

        response = HttpResponse(
            pdf_content, 
            content_type='application/pdf'
        )
        return response
    
    @action(methods=['GET'], detail=True, url_path='get-schema-report', permission_classes=[IsAuthenticated])
    def get_schema_report(self, request, *args, **kwargs):
        """Экспорт схемы компетенций в Word"""
        plan_id = self.kwargs['pk']

        doc_content = CompetencePassportDataService.get_schema_report(plan_id, format_type='docx')

        response = HttpResponse(
            doc_content,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

        return response
    
    @action(methods=['GET'], detail=True, url_path='get-schema-report-pdf', permission_classes=[IsAuthenticated])
    def get_schema_report_pdf(self, request, *args, **kwargs):
        """Экспорт схемы компетенций в PDF"""
        plan_id = self.kwargs['pk']
        
        pdf_content = CompetencePassportDataService.get_schema_report(plan_id, format_type='pdf')

        response = HttpResponse(
            pdf_content, 
            content_type='application/pdf'
        )
        return response
    
    @action(methods=['GET'], detail=True, url_path='get-passport-report', permission_classes=[IsAuthenticated])
    def get_passport_report(self, request, *args, **kwargs):
        """Экспорт паспорта компетенций в Word"""
        plan_id = self.kwargs['pk']

        doc_content = CompetencePassportDataService.get_passport_report(plan_id, format_type='docx')

        response = HttpResponse(
            doc_content,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

        return response
    
    @action(methods=['GET'], detail=True, url_path='get-passport-report-pdf', permission_classes=[IsAuthenticated])
    def get_passport_report_pdf(self, request, *args, **kwargs):
        """Экспорт паспорта компетенций в PDF"""
        plan_id = self.kwargs['pk']
        
        pdf_content = CompetencePassportDataService.get_passport_report(plan_id, format_type='pdf')

        response = HttpResponse(
            pdf_content, 
            content_type='application/pdf'
        )
        return response
    
