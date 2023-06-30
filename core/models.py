from django.db import models
import datetime

class Employee(models.Model):
    name = models.CharField("Employee Name", max_length=100, blank=True, null=True)
    salary = models.PositiveIntegerField("Salary", blank=True, null=True)
    department_name = models.ForeignKey("department", related_name="department", on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{str(self.pk)}:{str(self.name)}"
    
    class Meta:
        ordering = ["-joined_date"]
    
    @property
    def get_response(self):
        data = {
            "id": self.pk,
            "name":self.name,
            "salary": str(self.salary),
            "department": self.department_name.name,
            "joined_date": datetime.datetime.strftime(self.joined_date, "%d/%b/%y")
        }
        return data



class Department(models.Model):
    name = models.CharField("Name of Department", max_length=100, blank=True, null=True)
    employees = models.ManyToManyField(Employee, verbose_name="Employees", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ["-updated_on"]
    
    @property
    def get_response(self):
        data = {
            "id": self.pk,
            "name":self.name,
            "employee": self.employees.all(),
            "created_on": datetime.datetime.strftime(self.created_on, "%H:%M:%S, %d/%b/%y"),
            "updated_on": datetime.datetime.strftime(self.updated_on, "%H:%M:%S, %d/%b/%y")
        }
        return data


    
