from crispy_forms.helper import FormHelper


class LibraryFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.html5_required = True
        self.template = 'bootstrap4/table_inline_formset.html'


class LibraryFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = 'form-horizontal'
        self.html5_required = True
        self.form_tag = False
        self.label_class = 'col-lg-4'
        self.field_class = 'col-lg-8'
