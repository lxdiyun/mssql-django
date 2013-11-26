# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.db.models import Q
from rfid.models import Bookinfo


class BooksNoCaseView(TemplateView):
    template_name = "rfid/book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BooksNoCaseView, self).get_context_data(**kwargs)
        context['subtitle'] = u"图书未上架"
        books = Bookinfo.objects.filter(Q(szbookcaseno__isnull=True)
                                        | Q(szbookcaseno=''))
        context['books'] = books

        return context


class BookIndexErrorView(TemplateView):
    template_name = "rfid/book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BookIndexErrorView, self).get_context_data(**kwargs)
        context['subtitle'] = u"错误索书号"
        books = Bookinfo.objects.filter(Q(szbookindex__regex="%/")
                                        | ~Q(szbookindex__contains="/"))
        context['books'] = books

        return context
