from django.conf.urls import url
from bonus.views import *

urlpatterns = [
    url(r'^save_bonus/', SaveBonus.as_view(), name='save_bonus'),
    url(r'^delete_bonus/', DeleteBonusDetails.as_view(), name='delete_bonus'),
    url(r'^list_employee/', EmployeeList.as_view(), name='list_employee'),
    url(r'^bonus_paid_list/', BonusPaidList.as_view(), name='bonus_paid_list'),
]
