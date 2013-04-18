from django.views.generic import TemplateView
from check import check_area
from models import Bookinfo
from utils import AREA_DICT


class CheckAreaView(TemplateView):
    template_name = "checkcase/check_area.html"

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(CheckAreaView, self).get_context_data(**kwargs)
        area = int(kwargs['area'])
        if area in AREA_DICT:
            context.update(check_area(area))
            context["area_string"] = "%s %s" % (AREA_DICT[area][0],
                                                AREA_DICT[area][1])

        return context


class AreaListView(TemplateView):
    template_name = "checkcase/area_list.html"

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaListView, self).get_context_data(**kwargs)
        context["area_list"] = AREA_DICT

        return context


class BookDetailView(TemplateView):
    template_name = "checkcase/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        bookid = kwargs['bookid']
        book = Bookinfo.objects.get(szbookid=bookid)
        context['book'] = book

        return context
