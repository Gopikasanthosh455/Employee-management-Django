from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee
from .section_b import calculate_net_salary


def employee_list(request):
    employees = Employee.objects.filter(status=Employee.ACTIVE)
    search_id = request.GET.get("employee_id", "").strip()
    search_error = None

    if search_id:
        employee = Employee.objects.filter(id=search_id).first()
        if employee:
            return redirect("employee_detail", employee_id=employee.id)
        search_error = f"Employee ID {search_id} is not registered."

    return render(
        request,
        "employees/employee_list.html",
        {"employees": employees, "search_error": search_error},
    )


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, "employees/employee_detail.html", {"employee": employee})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("employee_detail", employee_id=employee.id)
    else:
        form = EmployeeForm()

    return render(request, "employees/employee_form.html", {"form": form, "title": "Add Employee"})


def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employee_detail", employee_id=employee.id)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "employees/employee_form.html", {"form": form, "title": "Update Employee"})


def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        employee.status = Employee.INACTIVE
        employee.save(update_fields=["status", "updated_at"])
        messages.success(request, "Employee marked as INACTIVE.")
        return redirect("employee_list")

    return render(request, "employees/employee_confirm_delete.html", {"employee": employee})


def payroll_calculator(request):
    result = None

    if request.method == "POST":
        gross_salary = float(request.POST.get("gross_salary", 0))
        is_contractor = request.POST.get("is_contractor") == "on"
        result = calculate_net_salary(gross_salary, is_contractor)

    return render(request, "employees/payroll.html", {"result": result})
