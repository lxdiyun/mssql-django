from django.views.generic import TemplateView
from rfid.models import Bookinfo


class BookDetailView(TemplateView):
    template_name = "rfid/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        bookid = kwargs['bookid']
        book = None
        try:
            book = Bookinfo.objects.get(szbookid=bookid)
        except Bookinfo.DoesNotExist:
            book = {'szname': "Not exist"}

        context['book'] = book

        return context
