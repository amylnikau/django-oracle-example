from django import forms

from library.forms import LibraryFormHelper
from library.models import Writing, Work


class WritingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()
        self.fields["work"].queryset = Work.objects.exclude(work_id__in=Writing.objects.all()).filter(type=1)

    class Meta:
        model = Writing
        fields = '__all__'
