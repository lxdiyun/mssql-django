from django.conf.urls import patterns, url
from checkbook.views import BooksNoCaseView, BooksShortIndexView

urlpatterns = patterns('',
                       url(r'books_no_case',
                           BooksNoCaseView.as_view(),
                           name="books_no_case"),
                       url(r'books_short_index',
                           BooksShortIndexView.as_view(),
                           name="books_short_index"),
                       )
