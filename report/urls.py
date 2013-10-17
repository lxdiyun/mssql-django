from django.conf.urls import patterns, url
from views import NotPopularBooksView

urlpatterns = patterns('',
                       url(r'^not_popular_books$',
                           NotPopularBooksView.as_view(),
                           name="query_not_popular_books"),
                       )
