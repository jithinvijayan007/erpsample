from django.conf.urls import url
from .views import AddBuyBack, BuyBackList, GetItemBuyback,BuyBackView


urlpatterns = [
    url(r'^add_buyback/$', AddBuyBack.as_view(), name='add_buyback'),
    url(r'^buyback_list/$', BuyBackList.as_view(), name='buyback_list'),
    url(r'^item_buyback/$', GetItemBuyback.as_view(), name='item_buyback'),
    url(r'^buyback_view/$', BuyBackView.as_view(), name='buyback_view'),
]
