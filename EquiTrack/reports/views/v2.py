import operator
import functools

from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from reports.models import Result, CountryProgramme, Indicator
from reports.serializers.v2 import ResultListSerializer
from reports.serializers.v1 import IndicatorSerializer


class ResultListAPIView(ListAPIView):
    serializer_class = ResultListSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        current_cp = CountryProgramme.current()
        q = Result.objects.filter(country_programme=current_cp)

        query_params = self.request.query_params
        if query_params:
            queries = []

            if "country_programme" in query_params.keys():
                cp_year = query_params.get("country_programme", None)
                queries.append(Q(country_programme__wbs__contains='/A0/'))
                queries.append(Q(country_programme__from_date__year__lte=cp_year))
                queries.append(Q(country_programme__to_date__year__gte=cp_year))
            if "result_type" in query_params.keys():
                queries.append(Q(result_type__name=query_params.get("result_type")))

            if queries:
                expression = functools.reduce(operator.and_, queries)
                q = q.filter(expression)
        return q


class ResultDetailAPIView(RetrieveAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultListSerializer
    permission_classes = (IsAdminUser,)


class ResultIndicatorListAPIView(ListAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, pk=None, format=None):
        """
        Return All Indicators for Result
        """
        indicators = Indicator.objects.filter(result_id=pk)
        serializer = self.get_serializer(indicators, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )