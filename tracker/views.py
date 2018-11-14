from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import DeferredAttribute
from django.http import HttpResponse
from django.template import loader

from .models import Exercise, ExerciseInstance, Profile, Set, Classification
from .tables.tables import exercise_instance_table
from .forms import DateForm, ModelChoiceForm


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


def activity_navigator(request):
    ''' List all exercise instances related to a given profile.'''
    profile = get_object_or_404(Profile, user=request.user)
    return render(request=request,
                  template_name='tracker/activities.html',
                  context={'profile': profile})


def exercise_instance_list(request):
    ''' List all exercise instances related to a given profile.'''
    profile = get_object_or_404(Profile, user=request.user)
    return render(request=request,
                  template_name='tracker/instance_list.html',
                  context={'profile': profile})


def exercise_instance_page(request, instance_id):
    ''' Detailed view of an Exercise Instance.'''
    exercise_instance = get_object_or_404(ExerciseInstance, pk=instance_id)
    instance_table = exercise_instance_table([exercise_instance])
    return render(request=request,
                  template_name='tracker/activity.html',
                  context={'table': instance_table})


# A list view that precedes this which gives you links
# to pages that can filter instances by date range,
# classification, exercise etc.
def exercise_instance_date_table(request):
    ''' Test filtering exercise instances by date ranges.'''
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            qs = ExerciseInstance.objects.filter(
                date__range=(start_date, end_date))
            instance_table = exercise_instance_table(qs)
            return render(request=request,
                          template_name='tracker/activity.html',
                          context={'table': instance_table})
    # GET
    else:
        return render(request=request,
                      template_name='tracker/generic_form.html',
                      context={'form': DateForm()})


def exercise_instance_exercise_table(request):
    profile = Profile.objects.get(user__id=request.user.id)
    qs = profile.all_exercises()
    if request.method == 'POST':
        # parse user created exercises to form
        form = ModelChoiceForm(request.POST, queryset=qs)
        if form.is_valid():
            exercise = form.cleaned_data['objects']
            qs = ExerciseInstance.objects.filter(
                exercise=exercise)
            instance_table = exercise_instance_table(qs)
            return render(request=request,
                          template_name='tracker/activity.html',
                          context={'table': instance_table})
    else:
        # parse user created exercises to form
        return render(request=request,
                      template_name='tracker/generic_form.html',
                      context={'form': ModelChoiceForm(queryset=qs)})


def exercise_instance_class_table(request):
    profile = Profile.objects.get(user__id=request.user.id)
    qs = Classification.objects.all()
    if request.method == 'POST':
        form = ModelChoiceForm(request.POST, queryset=qs)
        if form.is_valid():
            classification = form.cleaned_data['objects']
            exercises = classification.exercise_set.all()
            instances = ExerciseInstance.objects.filter(exercise__in=exercises,
                                                        participant=profile)
            if instances:
                instance_table = exercise_instance_table(instances)
                template = 'tracker/activity.html'
                context = {'table': instance_table}
            else:
                template = 'tracker/error.html'
                context = {'classification': classification}
            return render(request=request,
                          template_name=template,
                          context=context)

    else:
        return render(request=request,
                      template_name='tracker/generic_form.html',
                      context={'form': ModelChoiceForm(queryset=qs)})
