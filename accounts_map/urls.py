from django.conf.urls import url
from accounts_map.views import ChartOfAccountsTypehead,CategoryTypehead,AccountsMapView,AdditionsTypeahead
urlpatterns = [
    url(r'^chartofaccounts_typehead/$', ChartOfAccountsTypehead.as_view(), name='chartofaccounts_typehead'),
    url(r'^category_typehead/$', CategoryTypehead.as_view(), name='category_typehead'),
url(r'^accounts_map/$', AccountsMapView.as_view(), name='accounts_map'),
url(r'^additions_typeahead/$', AdditionsTypeahead.as_view(), name='additions_typeahead'),


]
