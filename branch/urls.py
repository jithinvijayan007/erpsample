from django.conf.urls import url
from branch.views import BranchApi,BranchTypeHead,BranchCategoryList

urlpatterns = [
        url(r'^branchapi/$', BranchApi.as_view(), name='branchapi'),
        url(r'^branch_typeahead/$', BranchTypeHead.as_view(), name='BranchTypeHead'),
        url(r'^branch_category_list/$', BranchCategoryList.as_view(), name='BranchCategoryList'),

    ]
