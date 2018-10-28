import uuid

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_measurement.models import MeasurementField

from measurement.measures import Distance, Weight
import datetime
import pytz


class Profile(User):
    ''' Proxy model for User.'''

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    _height = MeasurementField(measurement=Distance)
    _weight = MeasurementField(measurement=Weight)
    _birth_date = models.DateField(null=True, blank=True)
    bmi = models.FloatField()
    country = CountryField()
    time_zone = models.CharField(
        max_length=100, blank=True, null=True,
        choices=TIMEZONES, default='UTC')
    age = models.IntegerField(default=0)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.username} - {self.pk}'

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = eval(f'Distance({value})')

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = eval(f'Weight({value})')
        bmi = (self._weight.kg / self.height.m) / self.height.m
        self.bmi = bmi

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value
        days_diff = datetime.date.today() - self._birth_date
        self.age = int((days_diff / 365).days)

    def all_exercises(self):
        ''' Returns all default and user created exercises.'''
        admin = Profile.objects.get(username='david')
        return Exercise.objects.filter(Q(created_by=self) |
                                       Q(created_by=admin))

    def all_exercise_instances(self):
        ''' Returns all user created exercise instances.'''
        return ExerciseInstance.objects.filter(participant=self)


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
    ''' A specific exercise e.g. pushups'''
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
                                       null=True,
                                       blank=True)

    created_by = models.OneToOneField(Profile,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return self.name


class Set(models.Model):
    ''' A set of repetitions of an exercise.'''
    reps = models.IntegerField(default=1)
    _weight = MeasurementField(measurement=Weight)
    _distance = MeasurementField(measurement=Distance)
    time = models.TimeField(null=True, blank=True)
    bpm = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'Reps - {self.number}'

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = eval(f'Weight({value})')

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = eval(f'Distance({value})')

    def __str__(self):
        return f'Sets - {self.number}'


class ExerciseInstance(models.Model):
    '''A specific execution of the exercise'''
    FEELING = (
        ('e', 'Energetic'),
        ('s', 'Sleep Deprived'),
        ('m', 'Motivated'),
        ('d', 'Demotivated'),
        ('u', 'Uninterested'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True)
    participant = models.ForeignKey(Profile,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    date = models.DateField(null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL,
                                 null=True)
    time = models.TimeField(null=True, blank=True),
    sets = models.ManyToManyField(Set)
    mood = models.CharField(max_length=40,
                            choices=FEELING,
                            null=True,
                            blank=True)
    fatigued = models.NullBooleanField(
        help_text='Whether you feel the muscles involved are fatigued/tired')
    note = models.CharField(max_length=500,
                            blank=True,
                            null=True)

    def __str__(self):
        return f'{self.exercise.name} ({self.id})'
