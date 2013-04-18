from django.conf.urls import patterns, url
from views import CheckAreaView, AreaListView, BookDetailView

urlpatterns = patterns('',
                       url(r'^$',
                           AreaListView.as_view(),
                           name="are_list"),
                       url(r'^(?P<area>\d+)$',
                           CheckAreaView.as_view(),
                           name="check_area"),
                       url(r'^book/(?P<bookid>\d+)$',
                           BookDetailView.as_view(),
                           name="book_detail"),
                       )
