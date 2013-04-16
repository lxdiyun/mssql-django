from django.conf.urls import patterns, url
from views import CheckAreaView

urlpatterns = patterns('',
                       url(r'^(?P<area>\d+)$',
                           CheckAreaView.as_view(),
                           name="check_area")
                       )
