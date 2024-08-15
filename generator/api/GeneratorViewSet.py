from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from auths.models import Permissions
from generator.models import PlanLinesLink
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

    @action(methods=['GET'], url_path="get-program-list", detail=False)
    def get_program_list(self, request, *args, **kwargs):

        user = self.request.user.userprofile.mira_id
        user = 2103
        data = AISServices.get_disciplines_by_person(user)

        result = []
        for item in data:

            line = LinesData.objects.filter(dis=item['discpl'], plan__abbrprofile=item['abbr'], plan__startyear=item['yr'], plan__file__status=4).first()

            if line:
                lines, created = PlanLinesLink.objects.get_or_create(
                    cadmission=item['id_admission'],
                    mira_id=item['planlin'],
                    person=item['mira_id'],
                    defaults={
                        "cadmission": item['id_admission'],
                        "mira_id": item['planlin'],
                        "person": item['mira_id'],
                        "status": 1,
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
