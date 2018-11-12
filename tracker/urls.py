from django.urls import path
from tracker import views

urlpatterns = [
    path('profile/', views.profile_page, name='profile_page'),
    path('exercises/', views.exercise_list, name='exercises'),
    path('exercise/<int:exercise_id>/', views.exercise_page, name='exercise'),
    path('activities/', views.exercise_instance_list, name='activities'),
    path('instance/<uuid:instance_id>/', views.exercise_instance_page, name='activity'),
    path('test_table/', views.test_view, name='test_view'),
]
