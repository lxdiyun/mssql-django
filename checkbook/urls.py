from django.conf.urls import patterns, url
from checkbook.views import BooksNoCaseView, BookIndexErrorView

urlpatterns = patterns('',
                       url(r'books_no_case',
                           BooksNoCaseView.as_view(),
                           name="books_no_case"),
                       url(r'books_short_index',
                           BookIndexErrorView.as_view(),
                           name="books_index_error"),
                       )
