from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import DeferredAttribute

from .models import Exercise, ExerciseInstance, Profile, Set


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


def exercise_instance_list(request):
    ''' List all exercise instances related to a given profile.'''
    profile = get_object_or_404(Profile, user=request.user)
    return render(request=request,
                  template_name='tracker/activities.html',
                  context={'profile': profile})


def exercise_instance_page(request, instance_id):
    ''' Detailed view of an Exercise Instance.'''
    exercise_instance = get_object_or_404(ExerciseInstance, pk=instance_id)
    set_attr_keys = [k.replace('_', '') for k, i in Set.__dict__.items()
                     if isinstance(i, DeferredAttribute) and k != 'id']
    return render(request=request,
                  template_name='tracker/activity.html',
                  context={'instance': exercise_instance,
                           'set_attr': set_attr_keys})
