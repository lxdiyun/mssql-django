from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from check import check_area
from rfid.models import Bookinfo
from rfid.utils import AREA_DICT


class AreaCheckBase(ContextMixin):
    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaCheckBase, self).get_context_data(**kwargs)
        area = int(kwargs['area'])
        if area in AREA_DICT:
            context.update(check_area(area))
            context["area_string"] = "%s %s" % (AREA_DICT[area][0],
                                                AREA_DICT[area][1])

        return context


class AreaCheckView(TemplateView, AreaCheckBase):
    template_name = "checkcase/area_check.html"


class AreaListAllCasesView(TemplateView, AreaCheckBase):
    template_name = "checkcase/area_list_all_cases.html"

    def get_context_data(self, **kwargs):
        context = super(AreaListAllCasesView, self).get_context_data(**kwargs)
        cases = context['all_cases']
        book_id_list = list(case.szfirstbookid for case in cases)
        books = list(Bookinfo.objects.filter(szbookid__in=book_id_list))
        book_dict = dict((book.szbookid, book) for book in books)
        for case in cases:
            if case.szfirstbookid in book_dict:
                case.book = book_dict[case.szfirstbookid]
        context['all_cases'] = cases

        return context


class AreaListView(TemplateView):
    template_name = "checkcase/area_list.html"

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaListView, self).get_context_data(**kwargs)
        context["area_list"] = AREA_DICT

        return context
