from django.contrib import admin
from add_combo.models import AddComboMaster,AddComboDiscount,AddComboDiscountItem

# Register your models here.
class AddComboMasterAdmin(admin.ModelAdmin):
    list_display = ['int_offer_type','vchr_offer_name','fk_item','fk_brand','dbl_amt','int_quantity','int_status','dat_to','dat_from']
    list_filter = ['int_offer_type','vchr_offer_name']
    search_fields = ['int_offer_type','vchr_offer_name']
admin.site.register(AddComboMaster,AddComboMasterAdmin)

class AddComboDiscountAdmin(admin.ModelAdmin):
    list_display = ['fk_master','int_discount_type','dbl_amt','dbl_percent']
    list_filter = ['int_discount_type','fk_master']
    search_fields = ['int_discount_type','fk_master']
admin.site.register(AddComboDiscount,AddComboDiscountAdmin)

class AddComboDiscountItemAdmin(admin.ModelAdmin):
    list_display = ['fk_master','int_quantity','dbl_amt','dbl_percent','fk_item']
    list_filter = ['int_quantity','fk_master']
    search_fields = ['int_quantity','fk_master']
admin.site.register(AddComboDiscountItem,AddComboDiscountItemAdmin)
