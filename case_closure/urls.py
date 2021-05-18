from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from case_closure.views import CaseClosureList,CaseClosureAdd,CaseClosureNotification

urlpatterns = [
        url(r'^case_closure_notification/$', CaseClosureNotification.as_view(), name='case_closure_notification'),
        url(r'^add_case_closure/$', CaseClosureAdd.as_view(), name='add_case_closure'),
        url(r'^case_closure_list/$', CaseClosureList.as_view(), name='case_closure_list'),


        ]
