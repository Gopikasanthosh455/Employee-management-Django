from django.test import TestCase
from django.urls import reverse

from .models import Employee
from .section_b import calculate_net_salary


class EmployeeTests(TestCase):
    def test_active_list_excludes_inactive_employees(self):
        Employee.objects.create(
            name="Asha",
            email="asha@example.com",
            department="Engineering",
            salary=50000,
            status=Employee.ACTIVE,
        )
        Employee.objects.create(
            name="Ravi",
            email="ravi@example.com",
            department="HR",
            salary=40000,
            status=Employee.INACTIVE,
        )

        response = self.client.get(reverse("employee_list"))

        self.assertContains(response, "Asha")
        self.assertNotContains(response, "Ravi")

    def test_delete_is_soft_delete(self):
        employee = Employee.objects.create(
            name="Meera",
            email="meera@example.com",
            department="Finance",
            salary=45000,
        )

        self.client.post(reverse("employee_delete", args=[employee.id]))
        employee.refresh_from_db()

        self.assertEqual(employee.status, Employee.INACTIVE)

    def test_search_unknown_employee_id_shows_message(self):
        response = self.client.get(reverse("employee_list"), {"employee_id": "99"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Employee ID 99 is not registered.")


class PayrollTests(TestCase):
    def test_payroll_for_employee(self):
        self.assertEqual(calculate_net_salary(8000, False), 6400)

    def test_payroll_for_contractor(self):
        self.assertEqual(calculate_net_salary(8000, True), 6300)
