from django import forms

from library.forms import LibraryFormHelper
from library.models import Publication, Work


class PublicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = LibraryFormHelper()
        self.fields["work"].queryset = Work.objects.exclude(work_id__in=Publication.objects.all()).filter(type=2)

    class Meta:
        model = Publication
        fields = '__all__'
