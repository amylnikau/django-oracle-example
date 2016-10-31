from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.formsets import ModelFormSetView
from library.models import Work
from library.views import ContextDataMixin, DatabaseErrorMessageMixin, DatabaseErrorFormSetMessageMixin
from library.work.forms import WorkForm


class WorkCreateView(DatabaseErrorMessageMixin, ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:works')
    success_message = 'Work successful created.'


class WorksView(DatabaseErrorFormSetMessageMixin, ContextDataMixin, ModelFormSetView):
    model = Work
    exclude = ('work_id', 'authors')
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
