from django.urls import path
from . import views


urlpatterns = [
    #path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('payroll_view/', views.payroll_view, name='payroll_view'),
    path('run_payroll/', views.run_payroll, name='run_payroll'),
]