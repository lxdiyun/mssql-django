# -*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic.base import View
from rfid.models import Bookinfo
from django.db.models import Q
from django.utils.dateparse import parse_date
from rfid.utils import AREA_DICT, CATALOG_DICT
import exceptions
from django.http import HttpResponse
from adli_django_utils.actions import export_as_csv


class NotPopularBooksView(ListView):
    template_name = "report/not_popular_books.html"
    context_object_name = 'books'
    paginate_by = 100
    date = None
    query_by = None
    sub = None
    query_scope = None

    def get(self, request, *args, **kwargs):
        if "date" in request.REQUEST:
            self.date = parse_date(request.REQUEST["date"])

        if "query_by" in request.REQUEST:
            query_by = request.REQUEST["query_by"].split('_')
            if 2 == len(query_by):
                self.query_by = query_by[0]
                try:
                    self.sub = int(query_by[1])
                except exceptions.ValueError:
                    self.sub = None

        return super(NotPopularBooksView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        books = []
        if self.date and self.query_by:
            date_q = Q(dtborrowdate__lte=self.date)
            empty_date_q = Q(dtborrowdate__isnull=True)
            sub_q = None

            if "catalog" == self.query_by and (self.sub in CATALOG_DICT):
                catalog = CATALOG_DICT[self.sub]
                sub_q = Q(szpretendindexnum__startswith=CATALOG_DICT[self.sub][1])
                self.query_scope = catalog[0]
            elif "area" == self.query_by and (self.sub in AREA_DICT):
                area = AREA_DICT[self.sub]
                area_prefix = "%06d" % self.sub
                sub_q = Q(szbookcaseno__startswith=area_prefix)
                self.query_scope = area[0] + "-" + area[1]

            if sub_q:
                books = Bookinfo.objects.filter(sub_q & (date_q | empty_date_q))
                books = books.order_by('dtborrowdate', 'szbookid')

        return books

    def get_context_data(self, **kwargs):
        context = super(NotPopularBooksView, self).get_context_data(**kwargs)
        context['AREA_DICT'] = AREA_DICT
        context['CATALOG_DICT'] = CATALOG_DICT
        context['query_date'] = self.date
        context['query_by'] = self.query_by
        context['query_scope'] = self.query_scope
        context['sub'] = self.sub

        return context


class ExportNotPopualrBooksView(View):
    field_names = ['szbookid',
                   'szname',
                   'szbookindex',
                   'get_case_info',
                   'szbookcaseno',
                   'dtconvertdate',
                   'bforcesortcase',
                   'dtborrowdate']

    header = [u"登录号",
              u"书名",
              u"索书号",
              u"层位信息",
              u"层位代码",
              u"注册日期",
              u"强制定位",
              u"最近借出日期"]

    def get(self, request, *args, **kwargs):
        date = kwargs.get('date')
        query_by = kwargs.get('query_by')
        scope = int(kwargs.get('scope'))

        if date and query_by and scope:
            books = self.get_queryset(date, query_by, scope)

            return export_as_csv("not_popular_books",
                                 ExportNotPopualrBooksView.field_names,
                                 books,
                                 ExportNotPopualrBooksView.header)

        return HttpResponse()

    def get_queryset(self, date, query_by, scope):
        date_q = Q(dtborrowdate__lte=date)
        empty_date_q = Q(dtborrowdate__isnull=True)
        sub_q = None
        books = []

        if "catalog" == query_by and (scope in CATALOG_DICT):
            sub_q = Q(szpretendindexnum__startswith=CATALOG_DICT[scope][1])
        elif "area" == query_by and (scope in AREA_DICT):
            area_prefix = "%06d" % scope
            sub_q = Q(szbookcaseno__startswith=area_prefix)

        if sub_q:
            books = Bookinfo.objects.filter(sub_q & (date_q | empty_date_q))
            books = books.order_by('dtborrowdate', 'szbookid')

        return books
