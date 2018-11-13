from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Exercise


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())


class ModelChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # set ModelChoiceForm to parsed querset
        qs = kwargs.pop('queryset')
        super().__init__(*args, **kwargs)
        self.fields['objects'].queryset = qs

    objects = forms.ModelChoiceField(queryset=Exercise.objects.none())
