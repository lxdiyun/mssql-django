from django.conf.urls import patterns, url
from views import CheckAreaView, AreaListView

urlpatterns = patterns('',
                       url(r'^(?P<area>\d+)$',
                           CheckAreaView.as_view(),
                           name="check_area"),
                       url(r'^$',
                           AreaListView.as_view(),
                           name="are_list")
                       )
