from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Exercise, Profile


def profile_page(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    height = f'{profile.height}{profile.height_unit}'
    weight = f'{profile.weight}{profile.weight_unit}'
    # parse height and weight units
    return render(request=request,
                  template_name='tracker/profile_page.html',
                  context={'profile': profile,
                           'height': height,
                           'weight': weight})


def exercise_list(request, pk):
    ''' List all exercises of a given profile.'''
    profile = get_object_or_404(Profile, pk=pk)
    return render(request=request,
                  template_name='tracker/exercises.html',
                  context={'profile': profile})
