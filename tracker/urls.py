from django.urls import path
from tracker import views

urlpatterns = [
    path('<int:pk>/profile/', views.profile_page, name='profile_page'),
    path('<int:pk>/exercises/', views.exercise_list, name='exercises'),
]
