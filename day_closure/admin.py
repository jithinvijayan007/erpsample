from django.contrib import admin
from day_closure.models import DayClosureDetails,DayClosureMaster
# Register your models here.
class DayClosureMasterAdmin(admin.ModelAdmin):
    list_display = ['vchr_name','bln_active']
    list_filter = ['vchr_name']
    search_fields = ['vchr_name','pk_bint_id']
admin.site.register(DayClosureMaster,DayClosureMasterAdmin)

class DayClosureDetailsAdmin(admin.ModelAdmin):
    list_display = ['dat_time','fk_staff','total_amount','json_dayclosure','int_closed','fk_branch']
    list_filter = ['int_closed','dat_time']
    search_fields = ['dat_time']
admin.site.register(DayClosureDetails,DayClosureDetailsAdmin)
