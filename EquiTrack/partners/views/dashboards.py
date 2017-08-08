from __future__ import unicode_literals

from datetime import datetime
from django.db.models import Case, When, F, Max, DateTimeField, DurationField, ExpressionWrapper

from rest_framework.permissions import IsAdminUser
from rest_framework.generics import (
    ListCreateAPIView
)

from partners.models import (
    Intervention,
)
from partners.serializers.dashboards import InterventionDashSerializer
from t2f.models import Travel, TravelType


class InterventionPartnershipDashView(ListCreateAPIView):
    """InterventionDashView
    Returns a list of Interventions.
    """
    serializer_class = InterventionDashSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        today = datetime.now()
        delta = ExpressionWrapper(today - F('last_pv_date'), output_field=DurationField())

        qs = Intervention.objects.exclude(status=Intervention.DRAFT)

        qs = qs \
            .annotate(last_pv_date=Max(Case(When(travel_activities__travel_type=TravelType.PROGRAMME_MONITORING,
                                                 travel_activities__travels__traveler=F(
                                                     'travel_activities__primary_traveler'),
                                                 travel_activities__travels__status=Travel.COMPLETED,
                                                 then=F('travel_activities__date')),
                                            output_field=DateTimeField())))

        qs = qs.annotate(days_since_last_pv=delta)
        return qs
