from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^add_combo/', views.AddCombo.as_view(),name='AddCombo'),
    url(r'^list_combo/', views.ListCombo.as_view(),name='ListCombo'),
    url(r'^list_detail_combo/', views.ListDetailedCombo.as_view(),name='ListDetailedCombo'),
    url(r'^delete_combo/', views.DeleteCombo.as_view(),name='DeleteCombo'),
    url(r'^item_offers/', views.ItemOffers.as_view(),name='ItemOffers'),
]
