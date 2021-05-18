
from django.conf.urls import url
from django.contrib import admin
from category.views import CategoryAdd,CategoryList,CategoryTypeHead,OtherCategoryTypeHead
urlpatterns = [
url(r'^categoryadd/',CategoryAdd.as_view(), name='categoryadd'),
url(r'^list_category/',CategoryList.as_view(), name='categorylist'),
url(r'^category_typeahead/$', CategoryTypeHead.as_view(), name='CategoryTypeHead'),
url(r'^other_categoryTypeahead/$', OtherCategoryTypeHead.as_view(), name='OtherCategoryTypeHead'),

]
