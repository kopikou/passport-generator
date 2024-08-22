from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from arim_library.services import LibraryServices
from auths.models import Permissions
from generator.models import PlanLinesLink, FormControl, IndependentTypes
from generator.serializer import PlanLinesLinkSerializer
from rpd.models import LinesData


class GeneratorViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = PlanLinesLink.objects.all()
    serializer_class = PlanLinesLinkSerializer
    permission_classes = [UserProfileHasPermission(Permissions.can_use_generator)]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        instance = (PlanLinesLink.objects.filter(id=pk)
                    .select_related("planlines")
                    .prefetch_related("planlines__semesters", "planlines__indicators").first())
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @action(methods=['GET'], url_path="get-program-list", detail=False)
    def get_program_list(self, request, *args, **kwargs):

        user = self.request.user.userprofile.mira_id
        user = 2103
        data = AISServices.get_disciplines_by_person(user)

        result = []
        for item in data:

            line = LinesData.objects.filter(dis=item['discpl'], plan__abbrprofile=item['abbr'],
                                            plan__startyear=item['yr'], plan__file__status=4).first()

            if line:
                lines, created = PlanLinesLink.objects.get_or_create(
                    cadmission=item['id_admission'],
                    mira_id=item['planlin'],
                    person=item['mira_id'],
                    defaults={
                        "cadmission": item['id_admission'],
                        "mira_id": item['planlin'],
                        "person": item['mira_id'],
                        "status": PlanLinesLink.StatusChoices.appointed,
                        "planlines_id": line.id,
                    }
                )

                result.append({
                    **item,
                    "id": lines.id,
                    "status": lines.status,
                    "status_verbose": lines.status_verbose,
                    "kafcode": lines.planlines.caf,
                    "discode": lines.planlines.newdisid,
                })

        return Response(
            data=result
        )

    @action(methods=['GET'], url_path="search-book", detail=False)
    def search_book(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = LibraryServices.search_book(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-software", detail=False)
    def search_soft(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')

        data = AISServices.search_software(val)

        return Response(data)

    @action(methods=['GET'], url_path="search-oborud", detail=False)
    def search_oborud(self, request, *args, **kwargs):
        val = self.request.query_params.get('val')
        type = int(self.request.query_params.get('type'))
        caf = int(self.request.query_params.get('caf'))

        data = AISServices.search_oborud(val, type, caf)

        return Response(data)

    @action(methods=['GET'], url_path="get-form-control-data", detail=False)
    def get_form_control_data(self, request, *args, **kwargs):

        data = FormControl.objects.all().values("id", "name")

        return Response(data)

    @action(methods=['GET'], url_path="get-independent-types-data", detail=False)
    def get_independent_types_data(self, request, *args, **kwargs):

        data = IndependentTypes.objects.all().values("id", "name")

        return Response(data)
