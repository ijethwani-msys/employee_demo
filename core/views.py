from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *

class EmployeeView(APIView):
    """Employee VIew for all opration of retaed to employee"""
    def get(self,request):
        self.data = request.GET
        if "action" in self.data:
            action = self.data.get("action",1)
            action_mapper = {
                1: self.get_employees,
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"mag":"Action is not valid"}
                self.status = status.HTTP_400_BAD_REQUEST
        else:
            self.ctx = {"msg":"Action is not in data"}
            self.status = status.HTTP_400_BAD_REQUEST
        return Response(self.ctx, self.status)
    
    def get_employees(self):
        department_name = self.data.get("department_name")
        employee_name = self.data.get("employee_name")
        employee_id = self.data.get("employee_id")
        employees = []
        try:
            if department_name:
                departments = Department.objects.filter(name=department_name)
                employees = [employee.get_response for department in departments for employee in department.employees.all()]
            else:
                employe_queryset = Employee.objects.all()
                if employee_name:
                    employe_queryset = employe_queryset.filter(name__icontains=employee_name)
                elif employee_id:
                    employe_queryset = employe_queryset.filter(id=employee_id)
                employees = [employee.get_response for employee in employe_queryset]
            self.ctx = {"msg": "Employee list Loaded Sucessfully", "data":employees}
            self.status= status.HTTP_200_OK
        
        except Exception as e:
            self.ctx = {"msg":"Error","error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self, request):
        self.data = request.data
        if "action" in self.data:
            action = self.data.get("action",1)
            action_mapper = {
                1: self.add_employee,
                2: self.update_employee,
                3: self.delete_employee
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"mag":"Action is not valid"}
                self.status = status.HTTP_400_BAD_REQUEST
        else:
            self.ctx = {"msg":"Action is not in data"}
            self.status = status.HTTP_400_BAD_REQUEST
        return Response(self.ctx, self.status)
    
    def add_employee(self):
        name = self.data.get("name")
        salary_num = self.data.get("salary")
        salary = float(salary_num) if salary_num else 0
        department_id = self.data.get("department_id")
        try:
            department = Department.objects.get(id=department_id) if department_id else Department.objects.get(id=1)
            obj = Employee(
                name = name,
                salary = salary,
                department_name = department
            )
            obj.save()
            department.employees.add(obj)
            response = obj.get_response
            self.ctx = {"msg":"Employee Added Sucessdfully","data":response}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg":"Error","error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_employee(self):
        employee_id = self.data.get('employee_id')
        name = self.data.get("name")
        salary_num = self.data.get("salary")
        salary = float(salary_num) if salary_num else 0
        department_id = self.data.get("department_id")
        try:
            department = Department.objects.get(id=department_id) if department_id else Department.objects.get(id=1)
            obj = Employee.objects.filter(id=employee_id)
            if obj.exists():
                obj.update(
                    name = name,
                    salary = salary,
                    department_name = department
                    
                )
                response = obj.first().get_response
                self.ctx = {"msg":"Employee Updated Successfully", "data":response}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Not Found", "data":None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delete_employee(self):
        employee_id = self.data.get('employee_id')
        department_id = self.data.get("department_id")
        try:
            department = Department.objects.get(id=department_id) if department_id else Department.objects.get(id=1)
            emp_set = Employee.objects.filter(id=employee_id)
            if emp_set.exists():
                department.employees.remove(*emp_set)
                emp_set.delete()
                self.ctx = {"msg": "Employee is successfully deleted from data base"}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Not Found", "data":None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR



class DepartmentView(APIView):
    """Department View"""
    def get(self,request):
        self.data = request.GET
        if "action" in self.data:
            action = self.data.get("action",1)
            action_mapper = {
                1: self.get_departments,
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"mag":"Action is not valid"}
                self.status = status.HTTP_400_BAD_REQUEST
        else:
            self.ctx = {"msg":"Action is not in data"}
            self.status = status.HTTP_400_BAD_REQUEST
        return Response(self.ctx, self.status)
    
    def get_departments(self):
        department_name = self.data.get("department_name")
        department_id = self.data.get("department_id")
        departments_data = []
        try:
            department_queryset = Department. objects.all()
            departments = department_queryset.filter(department__icontains=department_name) if department_name else department_queryset.filter(id=department_id) if department_id else department_queryset
            if departments.exists():
                departments_data = [department.get_response for department in departments]
                self.ctx = {"msg":"Department LIst Loaded Successfully", "data":departments_data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Not Found", "data":None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self, request):
        self.data = request.data
        if "action" in self.data:
            action = self.data.get("action",1)
            action_mapper = {
                1: self.add_department,
                2: self.update_department,
                3: self.delete_department
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"mag":"Action is not valid"}
                self.status = status.HTTP_400_BAD_REQUEST
        else:
            self.ctx = {"msg":"Action is not in data"}
            self.status = status.HTTP_400_BAD_REQUEST
        return Response(self.ctx, self.status)
    
    def add_department(self):
        name = self.data.get("name")
        try:
            obj = Department(
                name = name
            )
            obj.save()
            response = obj.get_response
            self.ctx = {"msg":"Department Created Successfully","data":response}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_department(self):
        departmane_id = self.data.get("departmane_id")
        name = self.data.get("name")
        employee_id_list = self.data.get("employee_id_list")
        employee_action_data = self.data.get("emp+_action")
        employee_action = employee_action_data.lower() if employee_action_data else None
        try:
            departments = Department.objects.filter(id=departmane_id)
            if departments.exists():
                if employee_id_list:
                    employees = Employee.objects.filter(id__in=employee_id_list) 
                    departments.update(
                        name = name
                    )
                    if employee_action == "add":
                        departments.first().employees.add(*employees)
                    else:
                        departments.first().employees.remove(*employees)
                response = departments.first().get_response
                self.ctx = {"msg":"Department Updated Successfully", "data":response}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Not Found", "data":None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delete_department(self):
        """Delete department"""
        department_id = self.data.get("department_id")
        try:
            deparment = Department.objects.filter(id=department_id)
            if deparment.exists():
                deparment.delete()
                self.ctx = {"msg":"Deleted successfully"}
                self.status = status.HTTP_201_CREATED
            else:
                self.ctx = {"msg":"Not Found", "data":None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg":"Error", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
