from django.contrib import admin
from adminsettings.models import AdminSettings

# Register your models here.
class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ['vchr_name','vchr_code','bln_enabled']
    list_filter = ['bln_enabled','fk_company']
    search_fields = ['vchr_name','vchr_value','vchr_code','fk_company__vchr_name']

admin.site.register(AdminSettings,AdminSettingsAdmin)
