from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from check import check_area, check_catalog, CHECKED_CATALOG_LIST
from rfid.utils import AREA_DICT, CATALOG_DICT
from rfid.utils import preare_pre_and_next_catalog, preare_pre_and_next_area
from rfid import views as rfid_views


class AreaDetailBase(ContextMixin):
    view_name = ""

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaDetailBase, self).get_context_data(**kwargs)
        area = int(kwargs['area'])
        if area in AREA_DICT:
            context.update(check_area(area))
            context["list_title"] = "%s %s" % (AREA_DICT[area][0],
                                               AREA_DICT[area][1])
            context["triple_prefix"] = ['pre', 'cur', 'next']

            preare_pre_and_next_area(area, self.view_name, context)

        return context


class AreaDetailErrorOnlyView(TemplateView, AreaDetailBase):
    template_name = "checkcase/detail_error_only.html"
    view_name = "checkcase_area_detail_error_only"


class AreaDetailView(TemplateView, AreaDetailBase):
    template_name = "checkcase/detail.html"
    view_name = "checkcase_area_detail"


class AreaListView(rfid_views.AreaListView):
    template_name = "checkcase/area_list.html"


class CatalogDetailBase(ContextMixin):
    view_name = ""

    def get_context_data(self, **kwargs):
        context = super(CatalogDetailBase, self).get_context_data(**kwargs)
        catalog = int(kwargs['catalog'])
        if catalog in CATALOG_DICT:
            catalog_prefix = CATALOG_DICT[catalog][1]
            context.update(check_catalog(catalog_prefix))
            context["list_title"] = CATALOG_DICT[catalog][0]
            context["triple_prefix"] = ['pre', 'cur', 'next']

            if CATALOG_DICT[catalog][2]:
                context["static_total"] = CATALOG_DICT[catalog][2]

            preare_pre_and_next_catalog(catalog, self.view_name, context)

        return context


class CatalogDetailErrorOnlyView(TemplateView, CatalogDetailBase):
    template_name = "checkcase/detail_error_only.html"
    view_name = "checkcase_catalog_detail_error_only"


class CatalogDetailView(TemplateView, CatalogDetailBase):
    template_name = "checkcase/detail.html"
    view_name = "checkcase_catalog_detail"


class CatalogListView(rfid_views.CatalogListView):
    template_name = "checkcase/catalog_list.html"

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context["checked_catalog_list"] = CHECKED_CATALOG_LIST

        return context
