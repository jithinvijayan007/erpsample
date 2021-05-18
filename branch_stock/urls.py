from django.conf.urls import url
from branch_stock.views import CompanyItemStockEcommerceAPI,BranchItemStockEcommerceAPI,BranchItemStockAPI,ListStockTransfer,BranchStockAPI,BranchStockAPI,ListBranchStock,GetPriceForItemAPI,GetPriceForItemAPI,ItemRestore,NonSaleableAPI

urlpatterns = [
        url(r'^list_stock_transfer/$', ListStockTransfer.as_view(), name='list_stock_transfer'),
        url(r'^add_branchstock/$', BranchStockAPI.as_view(), name='add_branchstock'),
        url(r'^listbranchstock/$', ListBranchStock.as_view(), name='listbranchstock'),
        url(r'^get_price_for_item/',GetPriceForItemAPI.as_view(), name='get_price_for_item'),

        url(r'^item_restore/',ItemRestore.as_view(), name='item_restore'),
        url(r'^non_saleable/',NonSaleableAPI.as_view(), name='non_saleable'),
        url(r'^branchitemstockapi/',BranchItemStockAPI.as_view(), name='branchitemstockapi'),
        url(r'^branchitemstockecommerceapi/',BranchItemStockEcommerceAPI.as_view(), name='branchitemstockecommerceapi'),
        url(r'^companyitemstockecommerceapi/',CompanyItemStockEcommerceAPI.as_view(), name='companyitemstockecommerceapi'),


    ]
