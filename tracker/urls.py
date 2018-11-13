from django.urls import path
from tracker import views

urlpatterns = [
    path('profile/', views.profile_page, name='profile_page'),
    path('exercises/', views.exercise_list, name='exercises'),
    path('exercise/<int:exercise_id>/', views.exercise_page, name='exercise'),
    path('activities/',
         views.exercise_instance_list,
         name='activities'),
    path('activities/table/date/',
         views.exercise_instance_date_table,
         name='date_table'),
    path('activities/table/exercise/',
         views.exercise_instance_exercise_table,
         name='exercise_table'),
    path('activities/table/class/',
         views.exercise_instance_class_table,
         name='class_table'),
    path('instance/<uuid:instance_id>/',
         views.exercise_instance_page,
         name='activity'),
]
