from django.urls import path
from . import views


urlpatterns = [
    #path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('admin_report/', views.admin_report, name='admin_report'),
    path('employee_report/', views.employee_report, name='employee_report'),
]