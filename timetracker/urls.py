from django.urls import path
from . import views

app_name = 'timetracker'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('select-team/', views.select_team, name='select_team'),
    path('task/create/<int:team_id>/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/start/', views.task_start, name='task_start'),
    path('task/<int:pk>/stop/', views.task_stop, name='task_stop'),
    path('team/<int:team_id>/categories/', views.category_manage, name='category_manage'),
    path('team/categories/', views.select_team_categories, name='select_team_categories'),
    path('export/excel/', views.export_tasks_excel, name='export_tasks_excel'),
]
