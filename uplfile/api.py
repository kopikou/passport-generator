from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.utils import UserProfileHasPermission
from arim.services import AISServices
from auths.models import Permissions
from rpd.models import PlanData


class UploadFileViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = None
    serializer_class = None
    permission_classes = [UserProfileHasPermission(Permissions.can_upload_files)]

    @action(methods=['GET'], url_path="get-admission-data", detail=False)
    def get_admission_data(self, request, *args, **kwargs):

        mira_id = self.request.user.userprofile.mira_id
        mira_id = 16236
        data = AISServices.get_admission_list_by_person(mira_id)

        abbrprofile_list = list(set([i['abbrprofile'] for i in data]))
        startyear_list = list(set([i['startyear'] for i in data]))

        filtered_data = PlanData.objects.filter(abbrprofile__in=abbrprofile_list, startyear__in=startyear_list, file__status=4)
        filtered_data_sorted = {f"{i.abbrprofile}_{i.startyear}": i for i in filtered_data}

        result = []
        for item in data:
            res = filtered_data_sorted.get(f"{item['abbrprofile']}_{item['startyear']}")
            if res:
                plan_documents = [i for i in res.plan_documents.values("id", "name", "new_type", "new_type__name")]
                result.append({
                    **item,
                    "plan_documents": plan_documents,
                    "plan_id": res.id,
                    "plan_name": res.file.title,
                })

        return Response(result)
