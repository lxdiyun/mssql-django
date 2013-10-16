from django.conf.urls import patterns, url
from views import NotPopularBooksView

urlpatterns = patterns('',
                       url(r'^not_popular_books/(?P<page>\d*)$',
                           NotPopularBooksView.as_view(),
                           name="not_popular_books"),
                       )
