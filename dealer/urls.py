from django.conf.urls import url,include
from dealer.views import AddDealer,ListDealer,ViewDealer,EditDealer,DealerHistory,DeleteDealer
urlpatterns = [
    url(r'^add_dealer/$', AddDealer.as_view(), name='add_dealer'),
    url(r'^list_dealer/$', ListDealer.as_view(), name='list_dealer'),
    url(r'^view_dealer/$', ViewDealer.as_view(), name='view_dealer'),
    url(r'^update_dealer/$', EditDealer.as_view(), name='update_dealer'),
    url(r'^dealer_history/$',DealerHistory.as_view(), name='dealer_history'),
    url(r'^delete_dealer/$',DeleteDealer.as_view(), name='delete_dealer')

]
