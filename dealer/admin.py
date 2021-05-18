from django.contrib import admin
from dealer.models import Dealer,DealerAddress,DealerContactPerson,DealerLog
# Register your models here.

admin.site.register(DealerAddress)
admin.site.register(DealerContactPerson)

class DealerAdmin(admin.ModelAdmin):
    list_display = ['vchr_code','vchr_name','int_is_act_del']
    list_filter = ['int_is_act_del']
    search_fields = ['vchr_code','vchr_name']
admin.site.register(Dealer,DealerAdmin)

class DealerLogAdmin(admin.ModelAdmin):
    list_display = ['dat_created','fk_dealer','fk_created','vchr_status']
admin.site.register(DealerLog,DealerLogAdmin)
