from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Exercise, Profile


@login_required
def profile_page(request):
    ''' Detailed view of a users Profile.'''
    profile = get_object_or_404(Profile, user=request.user)
    height = f'{profile.height}{profile.height_unit}'
    weight = f'{profile.weight}{profile.weight_unit}'
    # parse height and weight units
    return render(request=request,
                  template_name='tracker/profile_page.html',
                  context={'profile': profile,
                           'height': height,
                           'weight': weight})


def exercise_list(request):
    ''' List all exercises of a given profile.'''
    profile = get_object_or_404(Profile, user=request.user)
    return render(request=request,
                  template_name='tracker/exercises.html',
                  context={'profile': profile})


def exercise_page(request, exercise_id):
    ''' Detailed view of an Exercise.'''
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request=request,
                  template_name='tracker/exercise.html',
                  context={'exercise': exercise})
