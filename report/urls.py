from django.conf.urls import patterns, url
from views import NotPopularBooksView, ExportNotPopualrBooksView

urlpatterns = patterns('',
                       url(r'^not_popular_books$',
                           NotPopularBooksView.as_view(),
                           name="query_not_popular_books"),
                       url(r'^export_not_popular_books/'
                           '(?P<date>\d{4}-\d{2}-\d{2})/'
                           '(?P<query_by>\w+)/'
                           '(?P<scope>\d+)$',
                           ExportNotPopualrBooksView.as_view(),
                           name="export_not_popular_books"),
                       )
