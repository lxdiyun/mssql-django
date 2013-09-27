from django.conf.urls import patterns, url
from rfid.views import BookDetailView, BookQueryView, IndexView, CaseDetailView

urlpatterns = patterns('',
                       url(r'^book/(?P<bookid>\d+)$',
                           BookDetailView.as_view(),
                           name="book_detail"),
                       url(r'^book_query$',
                           BookQueryView.as_view(),
                           name="book_query"),
                       url(r'^case/(?P<caseid>\d+)$',
                           CaseDetailView.as_view(),
                           name="case_detail"),
                       url(r'^$',
                           IndexView.as_view(),
                           name="index"),
                       )
