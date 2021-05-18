from django.contrib import admin
from brands.models import Brands
# Register your models here.


class BrandsAdmin(admin.ModelAdmin):
    list_display = ['vchr_code','vchr_name','int_status']
    list_filter = ['int_status']
    search_fields = ['vchr_code','vchr_name']
admin.site.register(Brands,BrandsAdmin)
