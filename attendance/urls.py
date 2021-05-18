from django.conf.urls import url
from .views import *

urlpatterns = [
            url(r'^punch_log_details/', PunchLogDetails.as_view(), name='punch_log_details'),
            url(r'^attendance_details/', AttendanceDetails.as_view(), name='attendance_details'),
            url(r'^audit_month_wise/', AuditMonthWise.as_view(), name='audit_month_wise'),
            url(r'^attendance_export/', AttendanceExport.as_view(), name='attendance_export'),
            url(r'^daily_attendance_report/', DayWiseAttendanceReport.as_view(), name='daily_attendance_report'),
            ]
