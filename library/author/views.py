from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from library.author.forms import AuthorForm
from library.formsets import ModelFormSetView
from library.models import Author
from library.views import ContextDataMixin, DatabaseErrorFormSetMessageMixin, DatabaseErrorMessageMixin


class AuthorCreateView(DatabaseErrorMessageMixin, ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/object_form.html'
    success_url = reverse_lazy('library:authors')
    success_message = 'Author successful created.'


class AuthorsView(DatabaseErrorFormSetMessageMixin, ContextDataMixin, ModelFormSetView):
    model = Author
    exclude = ('author_id',)
    can_delete = True
    extra = 0
    paginate_by = 10
    template_name = 'library/objects.html'
