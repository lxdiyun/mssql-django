# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from check import check_area


AREA_DICT = {
    1: (u"一楼西区", u"外文图书"),
    2: (u"一楼西北区", u"N"),
    3: (u"一楼西南区", u"A,N"),
    4: (u"一楼东南区", u"A"),
    5: (u"一夹层西北区", u"X"),
    6: (u"一夹层东南区", u"A"),
    7: (u"二夹层西北区", u"Q"),
    8: (u"二夹层东北区", u"C,Q,R,S,U,V"),
    9: (u"二夹层东南区", u"C"),
    10: (u"二夹层西南区", u"C,P"),
    11: (u"二楼西区", u"K"),
    12: (u"二楼西北区外侧", u"T-TP"),
    13: (u"二楼西北区内侧", u"TP,TU"),
    14: (u"二楼北区", u"O"),
    15: (u"二楼东北区", u"E,Z,TS,TQ"),
    16: (u"二楼东南区", u"B"),
    17: (u"二楼南区", u"B"),
    18: (u"二楼西南区", u"K"),
    19: (u"三楼西区", u"F"),
    20: (u"三楼西北区外侧", u"F"),
    21: (u"三楼西北区内侧", u"G,J"),
    22: (u"三楼北区", u"D"),
    23: (u"三楼东北区", u"I"),
    24: (u"三楼西南区", u"H"),
}


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
