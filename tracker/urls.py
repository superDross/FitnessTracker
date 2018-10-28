from django.urls import path
from tracker import views

urlpatterns = [
    path('exercise-list/', views.ExerciseView.as_view(), name='exercises'),
]
