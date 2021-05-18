from django.conf.urls import url
from django.contrib import admin
# from coupon.views import ListCoupon,AddCoupon,ViewCoupon,EditCoupon
from coupon.views import ItemsData,AddCoupon,ListCoupon,ViewCoupon,EditCoupon,ImportCoupon,Staffcoupondetails,StaffCoupon,StaffcoupondetailsMobile
urlpatterns = [
url(r'^coupon_list/$',ListCoupon.as_view(),name='coupon_list'),
url(r'^coupon_add/$',AddCoupon.as_view(),name='coupon_add'),
url(r'^get_coupon_by_id/$',ViewCoupon.as_view(),name='get_coupon_by_id'),
url(r'^coupon_edit/$',EditCoupon.as_view(),name='coupon_edit'),
url(r'^coupon_import/$',ImportCoupon.as_view(),name='coupon_import'),
url(r'^staff_coupon/$',StaffCoupon.as_view(),name='staffcoupon'),
url(r'^staff_coupon_details/$',Staffcoupondetails.as_view(),name='coupon_import'),
url(r'^mobile_staff_coupon_details/$',StaffcoupondetailsMobile.as_view(),name='mobile_staff_coupon_details'),
url(r'^item_details/$',ItemsData.as_view(),name='item_details')

]
