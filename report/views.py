# Create your views here.
from django.views.generic import ListView
from rfid.models import Bookinfo
from django.db.models import Q
from django.utils.dateparse import parse_date


class NotPopularBooksView(ListView):
    template_name = "report/not_popular_books.html"
    context_object_name = 'books'
    paginate_by = 1000

    def get_queryset(self):
        books = Bookinfo.objects.filter(
            Q(szbookindex__startswith='I')
            & Q(dtborrowdate__lte=parse_date('2011-01-01')))

        return books

    def get_context_data(self, **kwargs):
        context = super(NotPopularBooksView, self).get_context_data(**kwargs)
        context['request'] = self.request

        return context
