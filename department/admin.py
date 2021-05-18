from django.contrib import admin

# Register your models here.
from department.models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['vchr_code', 'vchr_name', 'int_status']
    list_filter = ['fk_company']
    search_fields = ['vchr_code', 'vchr_name', 'fk_company__vchr_name']
admin.site.register(Department, DepartmentAdmin)
