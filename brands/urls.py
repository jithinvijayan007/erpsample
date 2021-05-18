from django.conf.urls import url
from brands.views import AddBrands,BrandsTypeHead

urlpatterns = [
        url(r'^add_brands/$', AddBrands.as_view(), name='add_brands'),
        url(r'^brands_typeahead/$', BrandsTypeHead.as_view(), name='BrandsTypeHead'),
    ]
