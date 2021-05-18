from django.conf.urls import url
from customer.views import EditCustomer,CustomerTypeHead,CustomerView,UpdateCustomer,GenerateOtp,UpdateCustomerInvoice,VarifyOtp,CustomerHistory,AddCustomerPOS,AddCustomerSalesReturn, getSelectedCustomerList, getCustomerList


urlpatterns = [
        url(r'^customer_update/$', EditCustomer.as_view(), name='customer_update'),
        url(r'^customerTypeahead/$', CustomerTypeHead.as_view(), name='CustomerTypeHead'),
        url(r'^customer_view/$', CustomerView.as_view(), name='customer_view'),
        url(r'^edit_customer/$', UpdateCustomer.as_view(), name='edit_customer'),
        url(r'^generateotp/$', GenerateOtp.as_view(), name='generatotp'),
        url(r'^edit_customer_sales/$', UpdateCustomerInvoice.as_view(), name='edit_customer'),
        url(r'^varifyotp/$', VarifyOtp.as_view(), name='edit_customer'),
        url(r'^customer_details/$', CustomerHistory.as_view(), name='customer_details'),
        url(r'^add_customer_pos/',AddCustomerPOS.as_view(),name='add_customer_pos'),
        url(r'^add_customer_sales_return/',AddCustomerSalesReturn.as_view(),name='add_customer_pos'),
       
        url(r'^getselectedcustomer/$', getSelectedCustomerList.as_view(),name='getSelectedCustomerList'),
        url(r'^getcustomerlist/$', getCustomerList.as_view(),name='getCustomerList'),

    ]
