from __future__ import absolute_import

from django.conf.urls import url

from management.views.general import InvalidateCache, SyncFRs
from management.views.reports import LoadResultStructure
from management.views.tasks_endpoints import UpdateHactValuesAPIView, UpdateAggregateHactValuesAPIView
from management.views.v1 import ActiveUsersSection, AgreementsStatisticsView, PortalDashView

app_name = 'management'
urlpatterns = ((
    url(r'^$', PortalDashView.as_view(), name='dashboard'),
    url(r'^load-results/$', LoadResultStructure.as_view(), name='load_result_structure'),
    url(r'^invalidate-cache/$', InvalidateCache.as_view(), name='invalidate_cache'),
    url(r'^sync-frs/$', SyncFRs.as_view(), name='sync_frs'),
    url(r'^api/stats/usercounts/$', ActiveUsersSection.as_view(), name='stats_user_counts'),
    url(r'^api/stats/agreements/$', AgreementsStatisticsView.as_view(), name='stats_agreements'),
    url(r'^tasks/update_hact_values/$', UpdateHactValuesAPIView.as_view(), name='tasks_update_hact_values'),
    url(r'^tasks/update_aggregate_hact_values/$', UpdateAggregateHactValuesAPIView.as_view(),
        name='tasks_aggregate_update_hact_values'),
), 'management')
