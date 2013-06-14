from django.views.generic import TemplateView
from rfid.models import Bookinfo
from rfid.forms import BookQueryForm


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


class BookQueryView(TemplateView):
    template_name = "rfid/book_query.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = BookQueryForm(self.request.POST)
        if form.is_valid():
            context['books'] = Bookinfo.get_books(form.get_ssid_list())
        return self.render_to_response(context)
