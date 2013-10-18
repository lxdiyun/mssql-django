# Create your views here.
from django.views.generic import ListView
from rfid.models import Bookinfo
from django.db.models import Q
from django.utils.dateparse import parse_date
from rfid.utils import AREA_DICT, CATALOG_DICT
import exceptions


class NotPopularBooksView(ListView):
    template_name = "report/not_popular_books.html"
    context_object_name = 'books'
    paginate_by = 2000
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
            sub_q = None

            if "catalog" == self.query_by and (self.sub in CATALOG_DICT):
                catalog = CATALOG_DICT[self.sub]
                sub_q = Q(szbookindex__startswith=CATALOG_DICT[self.sub][0])
                self.query_scope = catalog[0]
            elif "area" == self.query_by and (self.sub in AREA_DICT):
                area = AREA_DICT[self.sub]
                area_prefix = "%06d" % self.sub
                sub_q = Q(szbookcaseno__startswith=area_prefix)
                self.query_scope = area[0] + "-" + area[1]

            if date_q and sub_q:
                books = Bookinfo.objects.filter(sub_q & date_q)

        return books

    def get_context_data(self, **kwargs):
        context = super(NotPopularBooksView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['AREA_DICT'] = AREA_DICT
        context['CATALOG_DICT'] = CATALOG_DICT
        context['query_date'] = self.date
        context['query_by'] = self.query_by
        context['query_scope'] = self.query_scope

        return context
