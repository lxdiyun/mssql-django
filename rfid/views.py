from django.views.generic import TemplateView
from rfid.models import Bookinfo, Bookcaseidinfo
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
            all_ssid = form.get_ssid_list()
            books = Bookinfo.get_books(all_ssid)
            context['books'] = books
            founded_ssid = map(lambda book: book.szbookid, books)
            not_founed_ssid = list(set(all_ssid) - set(founded_ssid))
            context['not_found'] = not_founed_ssid
            context['book_ssid_list'] = form.cleaned_data['book_ssid_list']

        return self.render_to_response(context)


class CaseDetailView(TemplateView):
    template_name = "rfid/case_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CaseDetailView, self).get_context_data(**kwargs)
        caseid = kwargs['caseid']
        case = None
        firstbook = None
        books = None
        try:
            case = Bookcaseidinfo.objects.get(szbookcaseno=caseid)
            books = Bookinfo.objects.filter(szbookcaseno=case.szbookcaseno)
            firstbook = Bookinfo.objects.get(szbookid=case.szfirstbookid)
            case.book = firstbook
        except Bookcaseidinfo.DoesNotExist:
            pass
        except Bookinfo.DoesNotExist:
            pass

        context['case'] = case
        if books:
            context['books'] = books
            context['total'] = len(books)
            context['borrowed'] = len(filter(lambda b: b.nbookstatus != 1,
                                             books))

        return context


class IndexView(TemplateView):
    template_name = "rfid/index.html"
