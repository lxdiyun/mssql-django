from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from check import check_area
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
            context["triple_prefix"] = ['pre', 'cur', 'next']

        return context


class AreaCheckView(TemplateView, AreaCheckBase):
    template_name = "checkcase/area_check.html"


class AreaListAllCasesView(TemplateView, AreaCheckBase):
    template_name = "checkcase/area_list_all_cases.html"

class AreaListView(TemplateView):
    template_name = "checkcase/area_list.html"

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaListView, self).get_context_data(**kwargs)
        context["area_list"] = AREA_DICT

        return context
