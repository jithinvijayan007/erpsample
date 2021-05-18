from django.conf.urls import url
from company_permissions.views import CompanyPermissions,CompanyPermissionSave


urlpatterns = [
        url(r'^list/$', CompanyPermissions.as_view(), name='CompanyPermissions'),
        url(r'^save/$', CompanyPermissionSave.as_view(), name='CompanyPermissionSave'),
    ]
