# Create your views here.
from django.views.generic import ListView
from rfid.models import Bookinfo
from django.db.models import Q
from django.utils.dateparse import parse_date
from rfid.utils import AREA_DICT, CATALOG_DICT


class NotPopularBooksView(ListView):
    template_name = "report/not_popular_books.html"
    context_object_name = 'books'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        self.date = parse_date(request.REQUEST["date"])

        return super(NotPopularBooksView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.date:
            books = Bookinfo.objects.filter(
                Q(szbookindex__startswith='I')
                & Q(dtborrowdate__lte=self.date))

            return books
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(NotPopularBooksView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['AREA_DICT'] = AREA_DICT
        context['CATALOG_DICT'] = CATALOG_DICT

        return context
