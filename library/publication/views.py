from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.formsets import ModelFormSetView
from library.models import Publication
from library.publication.forms import PublicationForm
from library.views import ContextDataMixin


class PublicationCreateView(ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:publications')
    success_message = 'Publication successful created.'


class PublicationsView(ContextDataMixin, ModelFormSetView):
    model = Publication
    fields = '__all__'
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
