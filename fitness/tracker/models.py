import uuid

from django.db import models
from django.contrib.auth.models import User


class MuscleGroup(models.Model):
    ''' Areas of body e.g. back.'''
    MUSCLE_GROUPS = (
        ('Back', 'Back'),
        ('Chest', 'Chest'),
        ('Arms', 'Arms'),
        ('Legs', 'Legs'),
    )

    group = models.CharField(max_length=20,
                             choices=MUSCLE_GROUPS,
                             help_text='name of body area')

    muscle = models.CharField(max_length=50,
                              help_text='name of body area')

    def __str__(self):
        return '{}: {}'.format(self.group, self.muscle)


class Classification(models.Model):
    ''' A classification of exercises e.g. Push'''
    name = models.CharField(max_length=50,
                            help_text='Name of classification.')

    def __str__(self):
        return self.name


class Exercise(models.Model):
    ''' A sepcific exercise e.g. pushups'''
    EXERCISE_TYPE = (
        ('m', 'Isometric'),
        ('i', 'Isotonic'),
        ('c', 'Cardiovascular'),
    )

    name = models.CharField(max_length=50,
                            help_text='Name of movement')
    description = models.CharField(max_length=1000,
                                   help_text='Movement description.')
    type = models.CharField(
        max_length=20,
        choices=EXERCISE_TYPE,
        blank=True,
        help_text='Exercise catagory'
    )
    video = models.URLField(max_length=500,
                            help_text='Video demonstrating exercise.')

    classification = models.ForeignKey(Classification,
                                       on_delete=models.SET_NULL,
                                       null=True)
    muscles = models.ManyToManyField(MuscleGroup)
    progression = models.OneToOneField('self',
                                       on_delete=models.SET_NULL,
                                       null=True)
    creator = models.ForeignKey(User,
                                models.SET_NULL,
                                null=True,
                                blank=True)

    def __str__(self):
        return self.name


class Reps(models.Model):
    ''' Number of repetions of a movement.'''
    number = models.IntegerField(default=1)

    def __str__(self):
        return f'Reps - {self.number}'


class Sets(models.Model):
    ''' A set of repetitions of movements.'''
    number = models.IntegerField(default=1)
    reps = models.ManyToManyField(Reps)
    weight = models.IntegerField(default=0)
    time = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Sets - {self.number}'


class ExerciseInstance(models.Model):
    '''A specific execution of the exercise'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL,
                                 null=True)
    date = models.DateField(null=True, blank=True)
    set = models.ForeignKey(Sets,
                            on_delete=models.SET_NULL,
                            null=True)
    participant = models.ForeignKey(User,
                                    models.SET_NULL,
                                    null=True,
                                    blank=True)

    def __str__(self):
        return f'{self.id} ({self.exercise.name})'
