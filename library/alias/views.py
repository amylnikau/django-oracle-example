from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.alias.forms import AliasForm
from library.formsets import ModelFormSetView
from library.models import Alias
from library.views import ContextDataMixin


class AliasCreateView(ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Alias
    form_class = AliasForm
    success_url = reverse_lazy('library:aliases')
    success_message = 'Alias successful created.'
    template_name = 'library/object_form.html'


class AliasesView(ContextDataMixin, ModelFormSetView):
    model = Alias
    exclude = ('alias_id',)
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
