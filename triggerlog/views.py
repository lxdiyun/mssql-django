from django.views.generic import ListView
from models import TriggerLog


class CaseFirstBookChangesView(ListView):
    template_name = "triggerlog/case_first_book_changes.html"
    paginate_by = 12
    table = 'bookcaseidinfo'
    context_object_name = 'logs'

    def get_queryset(self):
        logs = TriggerLog.objects.filter(
            tablename=self.table).order_by('-time')

        return logs
