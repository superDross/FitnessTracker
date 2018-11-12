from django import forms
from django.forms.widgets import SelectDateWidget


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
