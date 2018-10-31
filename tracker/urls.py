from django.urls import path
from tracker import views

urlpatterns = [
    path('profile/', views.profile_page, name='profile_page'),
    path('exercises/', views.exercise_list, name='exercises'),
]
