from django.conf.urls import patterns, url
from rfid.views import BookDetailView, BookQueryView

urlpatterns = patterns('',
                       url(r'^book/(?P<bookid>\d+)$',
                           BookDetailView.as_view(),
                           name="book_detail"),
                       url(r'^book_query$',
                           BookQueryView.as_view(),
                           name="book_query"),
                       )
