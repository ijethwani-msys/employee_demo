from django.urls import path
from .views import *

urlpatterns = [
    path("employees/", EmployeeView.as_view(), name="employee"),
    path("department/", DepartmentView.as_view(), name="department")
]