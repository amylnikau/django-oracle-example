from django import forms

from library.forms import LibraryFormHelper
from library.models import WorkAuthors


class WorkAuthorsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()

    class Meta:
        model = WorkAuthors
        fields = '__all__'
