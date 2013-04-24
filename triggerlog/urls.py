from django.conf.urls import patterns, url
from views import CaseFirstBookChangesView

urlpatterns = patterns('',
                       url(r'^case_first_book_change/(?P<page>\d+)$',
                           CaseFirstBookChangesView.as_view(),
                           name="log_first_book_changes"),
                       )
