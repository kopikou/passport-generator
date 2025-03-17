from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from arim.services import AISServices
from rpdgen.models import AspPlan


class AspPlanViewSet(GenericViewSet):
    queryset = AspPlan.objects.all()
    serializer_class = None

    @action(methods=['get'], url_path='get-old-asp-plans', detail=True)
    def get_old_asp_plans(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')

        old_plans = AISServices.get_asp_old_plans(pk)

        del old_plans[pk]

        return Response(data=old_plans)
