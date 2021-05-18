from django.contrib import admin
from .models import BuyBack
# Register your models here.


class BuyBackAdmin(admin.ModelAdmin):
    list_display = ['fk_item', 'dat_start', 'dat_end', 'dbl_amount']
    list_filter = ['dat_start', 'dat_end', 'int_status']
    search_fields = ['fk_item__vchr_item_name']
admin.site.register(BuyBack,BuyBackAdmin)
