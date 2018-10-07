from django.db import models


class MuscleGroup(models.Model):
    ''' Areas of body e.g. back.'''
    MUSCLE_GROUPS = (
        ('Back', 'Back'),
        ('Chest', 'Chest'),
        ('Arms', 'Arms'),
        ('Legs', 'Legs'),
    )

    muscle_group = models.CharField(max_length=20,
                                    choices=MUSCLE_GROUPS,
                                    help_text='name of body area')

    muscle = models.CharField(max_length=50,
                              help_text='name of body area')

    def __str__(self):
        return '{}: {}'.format(self.muscle_group, self.muscle)


class Classification(models.Model):
    ''' A classification of exercises e.g. Push'''
    name = models.CharField(max_length=50,
                            help_text='Name of classification.')

    def __str__(self):
        return self.name


class Exercise(models.Model):
    ''' A sepcific exercise e.g. pushups'''
    name = models.CharField(max_length=50,
                            help_text='Name of movement')
    description = models.CharField(max_length=1000,
                                   help_text='Movement description.')
    video = models.URLField(max_length=500,
                            help_text='Video demonstrating exercise.')
    classification = models.ForeignKey(Classification,
                                       on_delete=models.SET_NULL,
                                       null=True)
    muscles = models.ManyToManyField(MuscleGroup)

    def __str__(self):
        return self.name


class ExerciseInstance(models.Model):
    '''A specific execution of the exercise'''
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL,
                                 null=True)
    date = models.DateField(null=True, blank=True)
