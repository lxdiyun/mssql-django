from django.conf.urls import patterns, url
from views import (AreaCheckView,
                   AreaListAllCasesView,
                   AreaListView,
                   )

urlpatterns = patterns('',
                       url(r'^$',
                           AreaListView.as_view(),
                           name="area_list"),
                       url(r'^(?P<area>\d+)$',
                           AreaCheckView.as_view(),
                           name="area_check"),
                       url(r'^all/(?P<area>\d+)$',
                           AreaListAllCasesView.as_view(),
                           name="area_list_all_cases"),
                       )
