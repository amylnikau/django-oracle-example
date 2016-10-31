from django import forms

from library.forms import LibraryFormHelper
from library.models import Alias


class AliasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()

    class Meta:
        model = Alias
        exclude = ('alias_id',)
