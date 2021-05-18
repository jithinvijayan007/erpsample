from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^save_settings_api/$', views.SaveAdminSettings.as_view(),name='save_settings_api'),
    # url(r'^airlinedelete/$', views.AirlineDeleteAPIView.as_view(),name='airlinedelete')
]
