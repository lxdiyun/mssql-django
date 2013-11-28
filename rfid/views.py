from django.views.generic import TemplateView
from rfid.models import Bookinfo, Bookcaseidinfo
from rfid.forms import BookQueryForm
from rfid.utils import CATALOG_DICT, AREA_DICT
from rfid.utils import preare_pre_and_next_catalog, preare_pre_and_next_area
from checkcase.check import CHECKED_CATALOG_LIST
from django.utils.translation import ugettext as _


class BookDetailView(TemplateView):
    template_name = "rfid/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book_id = kwargs['bookid']
        book = None
        try:
            book = Bookinfo.objects.get(szbookid=book_id)
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
        case_id = kwargs['caseid']
        case = None
        books = None
        try:
            case = Bookcaseidinfo.objects.select_related('firstbook').get(
                szbookcaseno=case_id)
            books = Bookinfo.objects.filter(szbookcaseno=case.szbookcaseno)
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


class CaseCatalogListView(TemplateView):
    template_name = "rfid/case_list.html"
    view_name = "case_catalog_list"

    def get_context_data(self, **kwargs):
        context = super(CaseCatalogListView, self).get_context_data(**kwargs)
        catalog = int(kwargs['catalogid'])
        if catalog in CATALOG_DICT:
            catalog_prefix = CATALOG_DICT[catalog][1]
            order_by = "dtlastordercase"
            cases = Bookcaseidinfo.get_cases_by_catalog(catalog_prefix,
                                                        order_by=order_by,
                                                        exculde_empty=False,
                                                        select_related=False)
            context['cases'] = cases
            context["list_title"] = CATALOG_DICT[catalog][0]
            context["total_count"] = len(cases)

            preare_pre_and_next_catalog(catalog, self.view_name, context)

        return context


class CaseAreaListView(TemplateView):
    template_name = "rfid/case_list.html"
    view_name = "case_area_list"

    def get_context_data(self, **kwargs):
        context = super(CaseAreaListView, self).get_context_data(**kwargs)
        area = int(kwargs['areaid'])
        if area in AREA_DICT:
            context["list_title"] = "%s %s" % (AREA_DICT[area][0],
                                               AREA_DICT[area][1])
            order_by = "dtlastordercase"
            cases = Bookcaseidinfo.get_cases_by_area(area,
                                                     order_by=order_by,
                                                     exculde_empty=False,
                                                     select_related=False)
            context['cases'] = cases
            context["total_count"] = len(cases)

            preare_pre_and_next_area(area, self.view_name, context)

        return context


class AreaListView(TemplateView):
    template_name = "rfid/area_list.html"
    title = _("RFID Area List")
    forward_view = "case_area_list"
    check_error_view = "checkcase_area_detail_error_only"
    check_error_detail_view = "checkcase_area_detail"
    column_names = [_("Number"),
                    _("Area"),
                    _("Area content"),
                    _("Check first book")]
    area_list = AREA_DICT

    def get_context_data(self, **kwargs):
        context = super(AreaListView, self).get_context_data(**kwargs)
        context["area_list"] = self.area_list
        context["title"] = self.title
        context["forward_view"] = self.forward_view
        context["check_error_view"] = self.check_error_view
        context["check_error_detail_view"] = self.check_error_detail_view
        context["columns"] = self.column_names

        return context


class CatalogListView(AreaListView):
    title = _("RFID Catalog List")
    forward_view = "case_catalog_list"
    check_error_view = "checkcase_catalog_detail_error_only"
    check_error_detail_view = "checkcase_catalog_detail"
    column_names = [_("Number"),
                    _("Catalog"),
                    _("Catalog Prefix"),
                    _("Check first book")]
    area_list = CATALOG_DICT

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context["checked_catalog_list"] = CHECKED_CATALOG_LIST

        return context


class IndexView(TemplateView):
    template_name = "rfid/index.html"
