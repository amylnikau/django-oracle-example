from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.formsets import ModelFormSetView
from library.models import Writing
from library.views import ContextDataMixin
from library.writings.forms import WritingForm


class WritingCreateView(ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Writing
    form_class = WritingForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:writings')
    success_message = 'Work successful created.'


class WritingsView(ContextDataMixin, ModelFormSetView):
    model = Writing
    exclude = ('work',)
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
