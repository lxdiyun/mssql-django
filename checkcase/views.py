from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from check import check_area, check_catalog
from rfid.utils import AREA_DICT, CATALOG_DICT


class AreaDetailBase(ContextMixin):
    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaDetailBase, self).get_context_data(**kwargs)
        area = int(kwargs['area'])
        if area in AREA_DICT:
            context.update(check_area(area))
            context["list_title"] = "%s %s" % (AREA_DICT[area][0],
                                               AREA_DICT[area][1])
            context["triple_prefix"] = ['pre', 'cur', 'next']

        return context


class AreaDetailErrorOnlyView(TemplateView, AreaDetailBase):
    template_name = "checkcase/detail_error_only.html"


class AreaDetailView(TemplateView, AreaDetailBase):
    template_name = "checkcase/detail.html"


class AreaListView(TemplateView):
    template_name = "checkcase/area_list.html"

    def get_context_data(self, **kwargs):
        global AREA_DICT
        context = super(AreaListView, self).get_context_data(**kwargs)
        context["area_list"] = AREA_DICT

        return context


class CatalogDetailBase(ContextMixin):
    def get_context_data(self, **kwargs):
        global CATALOG_DICT
        context = super(CatalogDetailBase, self).get_context_data(**kwargs)
        catalog = int(kwargs['catalog'])
        if catalog in CATALOG_DICT:
            catalog_prefix = CATALOG_DICT[catalog][1]
            context.update(check_catalog(catalog_prefix))
            context["list_title"] = CATALOG_DICT[catalog][0]
            context["triple_prefix"] = ['pre', 'cur', 'next']

        return context


class CatalogDetailErrorOnlyView(TemplateView, CatalogDetailBase):
    template_name = "checkcase/detail_error_only.html"


class CatalogDetailView(TemplateView, CatalogDetailBase):
    template_name = "checkcase/detail.html"


class CatalogListView(TemplateView):
    template_name = "checkcase/catalog_list.html"

    def get_context_data(self, **kwargs):
        global CATALOG_DICT
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context["catalog_list"] = CATALOG_DICT

        return context
