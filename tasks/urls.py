from django.urls import path
from . import views

urlpatterns = [
    # Task URLs
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/add/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete_confirm, name='task_delete'),
    path('task/<int:pk>/complete/', views.task_complete_confirm, name='task_complete'),
    
    # Priority URLs
    path('priorities/', views.priority_list, name='priority_list'),
    path('priority/add/', views.priority_create, name='priority_create'),
    path('priority/<int:pk>/edit/', views.priority_update, name='priority_update'),
    path('priority/<int:pk>/delete/', views.priority_delete_confirm, name='priority_delete'),
]
