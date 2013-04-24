from django.conf.urls import patterns, url
from rfid.views import BookDetailView

urlpatterns = patterns('',
                       url(r'^book/(?P<bookid>\d+)$',
                           BookDetailView.as_view(),
                           name="book_detail"),
                       )
