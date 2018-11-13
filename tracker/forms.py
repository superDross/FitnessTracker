from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Exercise


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())

class ExerciseForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
