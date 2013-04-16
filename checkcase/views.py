from django.views.generic import TemplateView
from check import check_area


class CheckAreaView(TemplateView):
    template_name = "checkcase/check_area.html"

    def get_context_data(self, **kwargs):
        area = int(kwargs['area'])
        context = super(CheckAreaView, self).get_context_data(**kwargs)
        context.update(check_area(area))
        print context

        return context
