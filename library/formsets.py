from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin


class FormSetMixin(object):
    """
    Base class for constructing a FormSet within a view
    """

    initial = []
    form_class = None
    formset_class = None
    success_url = None
    extra = 2
    max_num = None
    can_order = False
    can_delete = False
    prefix = None

    def get_formset(self):
        """
        Returns an instance of the formset
        """
        formset_class = self.construct_formset()
        return formset_class(**self.get_formset_kwargs())

    def get_initial(self):
        """
        Returns the initial data to use for formsets on this view.
        """
        return self.initial

    def get_prefix(self):
        """
        Returns the prefix to use for forms on this view
        """
        return self.prefix

    def get_formset_class(self):
        """
        Returns the formset class to use in the formset factory
        """
        return self.formset_class

    def get_form_class(self):
        """
        Returns the form class to use with the formset in this view
        """
        return self.form_class

    def construct_formset(self):
        """
        Returns the formset class from the formset factory
        """
        return formset_factory(self.get_form_class(), **self.get_factory_kwargs())

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = {
            'extra': self.extra,
            'max_num': self.max_num,
            'can_order': self.can_order,
            'can_delete': self.can_delete
        }

        if self.get_formset_class():
            kwargs['formset'] = self.get_formset_class()

        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            url = self.request.get_full_path()
        return url

    def formset_valid(self, formset):
        """
        If the formset is valid redirect to the supplied URL
        """
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        """
        If the formset is invalid, re-render the context data with the
        data-filled formset and errors.
        """
        return self.render_to_response(self.get_context_data(formset=formset))


class ModelFormSetMixin(FormSetMixin, MultipleObjectMixin):
    """
    A base view for displaying a list of objects.
    """
    exclude = None
    fields = None
    formfield_callback = None
    widgets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.paginate_by and not self.ordering:
            self.ordering = 'pk'

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = super().get_formset_kwargs()
        if hasattr(self, 'object_list'):
            kwargs['queryset'] = self.object_list
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        self.object_list = data.pop('object_list')
        if 'formset' not in kwargs:
            data['formset'] = self.get_formset()
        return data

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = super().get_factory_kwargs()
        kwargs.update({
            'exclude': self.exclude,
            'fields': self.fields,
            'formfield_callback': self.formfield_callback,
            'widgets': self.widgets,
        })
        if self.get_form_class():
            kwargs['form'] = self.get_form_class()
        if self.get_formset_class():
            kwargs['formset'] = self.get_formset_class()
        return kwargs

    def construct_formset(self):
        """
        Returns the formset class from the model formset factory
        """
        return modelformset_factory(self.model, **self.get_factory_kwargs())

    def formset_valid(self, formset):
        """
        If the formset is valid, save the associated models.
        """
        self.object_list = formset.save()
        return super(ModelFormSetMixin, self).formset_valid(formset)


class ProcessFormSetView(View):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the formset.
        """
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a formset instance with the passed
        POST variables and then checked for validity.
        """
        formset = self.get_formset()
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)


class BaseModelFormSetView(ModelFormSetMixin, ProcessFormSetView):
    """
    A base view for displaying a model formset
    """

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(BaseModelFormSetView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(BaseModelFormSetView, self).post(request, *args, **kwargs)


class ModelFormSetView(MultipleObjectTemplateResponseMixin, BaseModelFormSetView):
    """
    A view for displaying a model formset, and rendering a template response
    """
