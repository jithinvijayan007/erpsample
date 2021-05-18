from django.conf.urls import url
from .views import CompanyRegistration,CompanyTypeHead


urlpatterns = [
    url(r'^registration/$', CompanyRegistration.as_view(), name='company_registration'),
    url(r'^company_typeahead/$', CompanyTypeHead.as_view(), name='CompanyTypeHead'),

]
