from django.views.generic import ListView
from models import TriggerLog


class CaseFirstBookChangesView(ListView):
    template_name = "triggerlog/case_first_book_changes.html"
    paginate_by = 25
    table = 'bookcaseidinfo'
    context_object_name = 'logs'

    def get_queryset(self):
        logs = TriggerLog.objects.filter(tablename=self.table).order_by('-time')
        return list(logs)

    def get_context_data(self, **kwargs):
        context = super(
            CaseFirstBookChangesView,
            self
        ).get_context_data(**kwargs)
        context['request'] = self.request
        return context
