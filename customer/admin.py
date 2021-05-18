from django.contrib import admin
from customer.models import CustomerDetails
# Register your models here.

class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ['vchr_name','vchr_email','int_mobile','state','dbl_purchase_amount']
    list_filter = ['fk_state']
    search_fields = ['vchr_name','vchr_email','int_mobile','fk_state__vchr_name','fk_state__vchr_code']
    def state(self,obj):
        if obj.fk_state:
            return obj.fk_state.vchr_name+' ('+obj.fk_state.vchr_code+')'
        else:
            return ''
admin.site.register(CustomerDetails,CustomerDetailsAdmin)
