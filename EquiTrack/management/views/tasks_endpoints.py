from rest_framework.response import Response
from rest_framework.views import APIView

from EquiTrack.permissions import IsSuperUser
from hact.tasks import update_hact_values, update_aggregate_hact_values


class BasicTaskAPIView(APIView):
    permission_classes = (IsSuperUser,)
    task_function = None
    success_message = 'Task generated Successfully'

    def get(self, request, *args, **kwargs):
        try:
            self.task_function.delay(**self.request.query_params)
        except BaseException as e:
            return Response(status=500, data=str(e))

        return Response({'success': self.success_message})


class UpdateHactValuesAPIView(BasicTaskAPIView):
    task_function = update_hact_values
    success_message = 'Task generated Successfully UpdateHactValues'


class UpdateAggregateHactValuesAPIView(BasicTaskAPIView):
    task_function = update_aggregate_hact_values
    success_message = 'Task generated Successfully UpdateHactValues'

