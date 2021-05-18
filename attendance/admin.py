from django.contrib import admin
from .models import *
# Register your models here.


class PunchingEmpAdmin(admin.ModelAdmin):
    list_display = ['fk_user', 'vchr_user_log_id', 'int_active']
    list_filter = ['int_active']
    search_fields = ['vchr_user_log_id', 'fk_user__username', 'fk_user__first_name', 'fk_user__last_name']
admin.site.register(PunchingEmp, PunchingEmpAdmin)

class PunchLogAdmin(admin.ModelAdmin):
    list_display = ['fk_punchingemp', 'dat_punch', 'dat_start', 'dat_end', 'vchr_direction']
    list_filter = [ 'vchr_direction', 'dat_punch']
    search_fields = ['fk_punchingemp__fk_user__username', 'fk_punchingemp__fk_user__first_name', 'fk_punchingemp__fk_user__last_name']
admin.site.register(PunchLog, PunchLogAdmin)

class PunchLogDetailAdmin(admin.ModelAdmin):
    list_display = ['fk_log', 'tim_start', 'tim_end']
    list_filter = ['fk_log__dat_punch']
    search_fields = ['fk_log__fk_punchingemp__fk_user__username', 'fk_log__fk_punchingemp__fk_user__first_name', 'fk_log__fk_punchingemp__fk_user__last_name']
admin.site.register(PunchLogDetail, PunchLogDetailAdmin)

class TriggerErrorLogAdmin(admin.ModelAdmin):
    list_display = ['vchr_user_id', 'int_device_id', 'dat_error', 'txt_error']
    search_fields = ['txt_error']
admin.site.register(TriggerErrorLog, TriggerErrorLogAdmin)


# iclock DATABASE TABLE
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['employeecode', 'employeename', 'employeecodeindevice', 'recordstatus']
    list_filter = ['recordstatus']
    search_fields = ['employeecode', 'employeename', 'employeecodeindevice']
admin.site.register(Employees, EmployeesAdmin)

class DevicesAdmin(admin.ModelAdmin):
    list_display = ['devicefname', 'serialnumber', 'devicelocation']
    search_fields = ['devicefname', 'serialnumber', 'devicelocation']
admin.site.register(Devices, DevicesAdmin)
