from django.conf.urls import url
from department.views import AddDepartment,DepartmentList
urlpatterns = [
    url(r'^add_department/',AddDepartment.as_view(), name='add_department'),
    url(r'^list_departments/',DepartmentList.as_view(), name='list_department'),
]
