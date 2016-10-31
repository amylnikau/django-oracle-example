from django import forms

from library.forms import LibraryFormHelper
from library.models import Work


class WorkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()

    class Meta:
        model = Work
        exclude = ('work_id', 'authors')
