# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from rfid.models import Bookinfo
from django.db.models import Q


class BooksNoCaseView(TemplateView):
    template_name = "rfid/book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BooksNoCaseView, self).get_context_data(**kwargs)
        context['subtitle'] = u"无层位信息"
        books = Bookinfo.objects.filter(Q(szbookcaseno__isnull=True)
                                        | Q(szbookcaseno=''))
        context['books'] = books

        return context


class BooksShortIndexView(TemplateView):
    template_name = "rfid/book_list.html"

    def get_context_data(self, **kwargs):
        context = super(BooksShortIndexView, self).get_context_data(**kwargs)
        context['subtitle'] = u"疑似简短数据"
        books = Bookinfo.objects.filter(Q(szbookindex__regex=".*/")
                                        | ~Q(szbookindex__contains="/"))
        context['books'] = books

        return context
