from django import forms

from library.forms import LibraryFormHelper
from library.models import Author


class DateInput(forms.DateInput):
    input_type = 'date'


class AuthorForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DateInput(), required=False)
    death_date = forms.DateField(widget=DateInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()

    class Meta:
        model = Author
        exclude = ('author_id',)
