from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import (AreaDetailErrorOnlyView,
                   AreaDetailView,
                   AreaListView,
                   CatalogDetailErrorOnlyView,
                   CatalogDetailView,
                   CatalogListView,
                   )

urlpatterns = patterns('',
                       url(r'^$',
                           TemplateView.as_view(
                               template_name="checkcase/index.html"),
                           name="checkcase_index"),
                       url(r'^area$',
                           AreaListView.as_view(),
                           name="checkcase_area_list"),
                       url(r'^area/error/(?P<area>\d+)$',
                           AreaDetailErrorOnlyView.as_view(),
                           name="checkcase_area_detail_error_only"),
                       url(r'^area/detail/(?P<area>\d+)$',
                           AreaDetailView.as_view(),
                           name="checkcase_area_detail"),
                       url(r'^catalog$',
                           CatalogListView.as_view(),
                           name="checkcase_catalog_list"),
                       url(r'^catalog/error/(?P<catalog>\d+)$',
                           CatalogDetailErrorOnlyView.as_view(),
                           name="checkcase_catalog_detail_error_only"),
                       url(r'^catalog/detail/(?P<catalog>\d+)$',
                           CatalogDetailView.as_view(),
                           name="checkcase_catalog_detail"),
                       )
