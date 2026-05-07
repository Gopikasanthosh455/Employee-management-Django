from django.urls import path

from . import views


urlpatterns = [
    path("", views.employee_list, name="employee_list"),
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/<int:employee_id>/", views.employee_detail, name="employee_detail"),
    path("employees/<int:employee_id>/edit/", views.employee_update, name="employee_update"),
    path("employees/<int:employee_id>/delete/", views.employee_delete, name="employee_delete"),
    path("section-b/payroll/", views.payroll_calculator, name="payroll_calculator"),
]
