from django.contrib import admin

from .models import MuscleGroup, Classification, Exercise, ExerciseInstance

admin.site.register(MuscleGroup)
admin.site.register(Classification)
admin.site.register(Exercise)
admin.site.register(ExerciseInstance)
