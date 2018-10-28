from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exercise


class ExerciseView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    template_name = 'tracker/exercise_list.html'
    context_object_name = 'exercise_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(profile__username=self.kwargs['username'])
