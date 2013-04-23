from django.conf.urls import patterns, url
from views import CaseFirstBookChangesView

urlpatterns = patterns('',
                       url(r'^case__first_book_change/(?P<page>\d+)$',
                           CaseFirstBookChangesView.as_view(),
                           name="book_detail"),
                       )
