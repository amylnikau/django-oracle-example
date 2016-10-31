from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.formsets import ModelFormSetView
from library.models import Translation
from library.translations.forms import TranslationForm
from library.views import ContextDataMixin, DatabaseErrorMessageMixin


class TranslationCreateView(DatabaseErrorMessageMixin, ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Translation
    form_class = TranslationForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:translations')
    success_message = 'Translation successful created.'


class TranslationsView(DatabaseErrorMessageMixin, ContextDataMixin, ModelFormSetView):
    model = Translation
    exclude = ('work',)
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['col_size'] = 8
        return data
