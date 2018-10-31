from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Exercise, Profile


@login_required
def profile_page(request):
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
