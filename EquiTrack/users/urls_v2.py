
from django.conf.urls import patterns, url

from .views import (
    MyProfileAPIView,
    UserProfileAPIView,
    CountryView
)


urlpatterns = patterns(
    '',
    url(r'^myprofile/$', MyProfileAPIView.as_view(), name="myprofile-detail"),
    url(r'^api/(?P<user_id>\d+)/profile/$', UserProfileAPIView.as_view(), name="profile-detail"),
    url(r'^country/$', CountryView.as_view(http_method_names=['get']), name="country-detail"),

)
