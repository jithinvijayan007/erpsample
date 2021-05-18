from django.contrib import admin
from branch.models import Branch
# Register your models here.


class BranchAdmin(admin.ModelAdmin):
    list_display = ['vchr_code','vchr_name','int_status']
    list_filter = ['int_status']
    search_fields = ['vchr_code','vchr_name']
admin.site.register(Branch,BranchAdmin)
