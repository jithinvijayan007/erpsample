from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from . import views
from day_closure.views import DayClosureReport

urlpatterns = [
    url(r'^lst_dayclosure/', views.DayClosureList.as_view(),name='DayClosureList'),
    url(r'^request_mail/', views.RequestMail.as_view(),name='RequestMail'),
    url(r'^dayclosure_list/', views.ListDayClosure.as_view(),name='ListDayClosure'),
    url(r'^approve_mail/(?P<hash>\w+)/$', views.ApproveMail.as_view(),name='ApproveMail'),
    url(r'^day_closure_report/',DayClosureReport.as_view(),name='day_closure_report')

]
