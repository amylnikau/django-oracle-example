from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.authors_works.forms import WorkAuthorsForm
from library.formsets import ModelFormSetView
from library.models import WorkAuthors
from library.views import ContextDataMixin, DatabaseErrorFormSetMessageMixin, DatabaseErrorMessageMixin


class WorkAuthorsCreateView(DatabaseErrorMessageMixin, ContextDataMixin, SuccessMessageMixin, CreateView):
    model = WorkAuthors
    form_class = WorkAuthorsForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:work-authors')
    success_message = 'WorkAuthors successful created.'


class WorkAuthorsView(DatabaseErrorFormSetMessageMixin, ContextDataMixin, ModelFormSetView):
    model = WorkAuthors
    fields = '__all__'
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
