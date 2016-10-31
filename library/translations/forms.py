from django import forms

from library.forms import LibraryFormHelper
from library.models import Work, Translation


class TranslationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()
        self.fields["work"].queryset = Work.objects.exclude(work_id__in=Translation.objects.all()).filter(type=3)
        self.fields["translated_work"].queryset = Work.objects.exclude(type=3)

    class Meta:
        model = Translation
        fields = '__all__'
