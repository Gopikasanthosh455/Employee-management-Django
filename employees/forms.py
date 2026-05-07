from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "email", "department", "salary", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Employee name"}),
            "email": forms.EmailInput(attrs={"placeholder": "employee@example.com"}),
            "department": forms.TextInput(attrs={"placeholder": "Department"}),
            "salary": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }

    def clean_salary(self):
        salary = self.cleaned_data["salary"]
        if salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary
