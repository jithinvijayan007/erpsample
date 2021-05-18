from django.conf.urls import url
from branch_report_download.views import MobileBranchReportDownload
urlpatterns=[
    url(r'^branch_pdf$',MobileBranchReportDownload.as_view(),name='branch_pdf'),
    ]
