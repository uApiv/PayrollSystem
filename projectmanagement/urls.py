from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('project_list/', views.project_list, name='project_list'),
    path('project_append/', views.project_append, name='project_append'),
    path('project_modify/<int:proj_pk>', views.project_modify, name='project_modify'),
    path('project_delete/<int:proj_pk>', views.project_delete, name='project_delete'),
]