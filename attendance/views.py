from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Concat, Cast
from django.db.models.fields import DateField,TimeField,TextField
from django.db.models import Q, F, Value, Sum , Case, When, CharField
from datetime import datetime, timedelta, date
from attendance.models import *
from shift_schedule.models import *
from job_position.models import JobPosition
from department.models import Department
from userdetails.models import UserDetails, AdminSettings
from django.contrib.auth.models import User as AuthUser
from POS import ins_logger
from django.conf import settings
import pandas as pd
from pandas import ExcelWriter
import traceback
import sys, os
from os import path
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import and_,func ,cast,Date,case, literal_column,or_,MetaData,desc,String,extract
from POS.dftosql import Savedftosql
from sqlalchemy.orm import mapper, aliased
from sqlalchemy.dialects.postgresql import array
from hierarchy.views_hrms import get_data, get_hierarchy
from sqlalchemy import and_, or_, JSON, Integer, Float, String
from aldjemy.core import get_engine
import sqlalchemy
from sqlalchemy import create_engine,inspect,MetaData,Table,Column,select,func
from branch.models import Branch
import calendar
from dutyroster.models import DutyRoster
from hierarchy.models import HierarchyLevel
from salary_process.views import AllSalaryDetails
from django.contrib.postgres.fields.jsonb import KeyTransform
# Create your views here.


AuthUserSA = AuthUser.sa
UserDetailsSA = UserDetails.sa
PunchingEmpSA = PunchingEmp.sa
PunchLogSA = PunchLog.sa
PunchLogDetailSA = PunchLogDetail.sa
ShiftScheduleSA = ShiftSchedule.sa
EmployeesSA = Employees.sa
DevicesSA = Devices.sa
JobPositionSA = JobPosition.sa
DepartmentSA = Department.sa
BranchSA = Branch.sa

sqlalobj = Savedftosql('','')
alengine = sqlalobj.engine
engine = get_engine()
metadata = MetaData()
metadata.reflect(bind=alengine)
Connection = sessionmaker()
Connection.configure(bind=alengine)

# UserDetailsJS = metadata.tables['user_details']
ShiftExemptionJs = metadata.tables['shift_exemption']


def Session():
    _Session = sessionmaker(bind = alengine)
    return _Session()
DeviceAliasSA = aliased(DevicesSA)

class PunchLogDetails(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """ Date Wise PunchLog Details """
        try:
            conn = engine.connect()
            import pdb;pdb.set_trace()

            lst_selected_dept = request.data.get('lstSelectedDept')
            lst_selected_location = request.data.get('lstSelectedLocation')
            int_employee_id = request.data.get('intEmployeeId')
            int_brand_id = request.data.get('intBrandId')
            lst_branch_id = request.data.get('lstSelectedBranch')
            lst_desig_id = request.data.get('lstSelectedDesig')
            lst_data = request.data.get('lstFilter')
            dct_filter = {}
            dct_filter['blnDept'] = False
            dct_filter['blnPhysicalLoc'] = False
            dct_filter['blnEmployee'] = False
            dct_filter['blnBrand'] = False
            dct_filter['blnDesignation'] = False
            dct_filter['blnBranch'] = False
            dat_attendance = datetime.strptime(request.data.get('datAttendance',datetime.strftime(datetime.now(),"%Y-%m-%d")),"%Y-%m-%d")

            str_query = """SELECT (pl.dat_end - pl.dat_start) dur_active, pl.pk_bint_id AS int_log_id, CONCAT(au.first_name,' ',CASE WHEN ud.vchr_middle_name IS NOT NULL THEN CONCAT(ud.vchr_middle_name,' ',au.last_name) ELSE au.last_name END) AS str_emp_name, shft.vchr_name AS str_shift_name, ud.vchr_employee_code, pl.vchr_direction, pl.dat_punch, pl.dat_start, pl.dat_end, CONCAT(emp.employeecode, '-', emp.employeename) AS employeename, devin.devicelocation AS str_in_location, devend.devicelocation AS str_out_location, ud.json_physical_loc, br.vchr_name as str_branch_name, brnd.vchr_name as vchr_brand_name, INITCAP(CASE WHEN hldy.pk_bint_id IS NOT NULL THEN CASE WHEN pl.vchr_direction = 'OUT' THEN CONCAT('Worked on ', hldy.vchr_name) ELSE CONCAT(hldy.vchr_name,' ', 'Holiday') END WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR('{0}'::DATE, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN CASE WHEN pl.vchr_direction = 'OUT' THEN 'Worked on Week Off' ELSE 'Week Off' END WHEN wklv.pk_bint_id IS NOT NULL THEN CONCAT('Week Off', CASE WHEN wklv.int_status = 1 THEN ' Pending Approval' WHEN wklv.int_status = 2 THEN ' Pending Verification' END) WHEN lev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN lev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' ', lvtyp.vchr_name, CASE WHEN lev.int_status = 1 THEN ' Pending Approval' END) WHEN cmblev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN cmblev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' Combo Off', CASE WHEN cmblev.int_status = 1 THEN ' Pending Approval' END) WHEN odr.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN odr.chr_day_type='F' THEN 'Full Day' ELSE 'Half Day' END, ' On-Duty', CASE WHEN odr.int_status = 0 THEN ' Pending Approval' WHEN odr.int_status = 1 THEN ' Pending Verification' END) WHEN lslv.pk_bint_id IS NOT NULL THEN 'LESS HOUR LEAVE' WHEN pl.dat_punch IS NULL THEN 'Absent' WHEN ltplcy.pk_bint_id IS NOT NULL THEN CONCAT(ltplcy.vchr_name, CASE WHEN ltrqst.int_status = 0 THEN ' Pending Approval' END) END) AS str_status,pemp.fk_user_id,(CASE WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR('{0}'::DATE, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN 'weekOff' WHEN cmblev.pk_bint_id IS NOT NULL THEN 'comboOff' WHEN hldy.pk_bint_id IS NOT NULL THEN 'holiDay' WHEN lev.pk_bint_id IS NOT NULL THEN 'leave' WHEN odr.pk_bint_id IS NOT NULL THEN 'onDuty' WHEN pl.dat_punch IS NULL THEN 'absent' END) AS str_day_type FROM auth_user AS au JOIN userdetails AS ud ON ud.user_ptr_id = au.id LEFT JOIN department AS dept ON dept.pk_bint_id = ud.fk_department_id LEFT JOIN job_position AS desg ON desg.pk_bint_id = ud.fk_desig_id LEFT JOIN brands AS brnd ON brnd.pk_bint_id = ud.fk_brand_id LEFT JOIN punching_emp AS pemp ON pemp.fk_user_id = ud.user_ptr_id LEFT JOIN branch as br ON br.pk_bint_id = ud.fk_branch_id LEFT JOIN employees AS emp ON emp.employeecode = pemp.vchr_user_log_id LEFT JOIN punch_log AS pl ON pl.fk_punchingemp_id = pemp.pk_bint_id AND pl.dat_punch = '{0}' LEFT JOIN shift_schedule AS shft ON shft.pk_bint_id = pl.fk_shift_id LEFT JOIN devices devin ON devin.deviceid=pl.int_start_device_id LEFT JOIN devices devend ON devend.deviceid=pl.int_end_device_id LEFT JOIN holiday hldy ON hldy.dat_holiday = '{0}' AND hldy.bln_active = TRUE LEFT JOIN duty_roster wkoff ON ud.int_weekoff_type=1 AND wkoff.fk_employee_id=ud.user_ptr_id AND wkoff.bln_active=TRUE AND wkoff.json_dates ? '{0}'::DATE::TEXT LEFT JOIN weekoff_leave wklv ON wklv.fk_employee_id = ud.user_ptr_id AND wklv.dat_from <= '{0}'::DATE AND wklv.dat_to >= '{0}'::DATE AND wklv.int_status IN (1, 2) LEFT JOIN leave lev ON lev.dat_from<='{0}'::DATE AND lev.dat_to>='{0}'::DATE AND lev.int_status NOT IN (3, 4) AND lev.fk_user_id=ud.user_ptr_id LEFT JOIN combo_off_users cmblev ON cmblev.dat_leave='{0}'::DATE AND cmblev.int_status IN (1, 2) AND cmblev.fk_user_id=ud.user_ptr_id LEFT JOIN leave_type lvtyp ON lvtyp.pk_bint_id=lev.fk_leave_type_id LEFT JOIN less_hour_leave lslv ON lslv.fk_employee_id=ud.user_ptr_id AND lslv.dat_leave='{0}'::DATE LEFT JOIN on_duty_request odr ON odr.fk_requested_id = ud.user_ptr_id AND odr.dat_request = '{0}'::DATE AND odr.int_status != -1 LEFT JOIN (late_hours_request ltrqst JOIN late_hours_policy ltplcy ON ltplcy.pk_bint_id = ltrqst.fk_late_hours_policy_id) ON ltrqst.dat_requested::DATE = '{0}'::DATE AND ltrqst.fk_employee_id = ud.user_ptr_id AND ltrqst.int_status != -1 WHERE au.is_active = TRUE"""

            str_query = str_query.format(str(dat_attendance))

            str_filter = ''
            rst_query = ''
            lst_loc = []
            if lst_selected_location:
                str_filter = ' AND ud.json_physical_loc ?| ARRAY'+str(lst_selected_location)
            if lst_selected_dept:
                str_filter += ' AND dept.pk_bint_id IN('+str(lst_selected_dept)[1:-1]+ ')'
            if int_employee_id:
                str_filter += ' AND ud.user_ptr_id = '+str(int_employee_id)
            if int_brand_id:
                str_filter += ' AND ud.fk_brand_id = '+str(int_brand_id)
            if lst_branch_id:
                str_filter += ' AND br.pk_bint_id IN('+str(lst_branch_id)[1:-1]+')'
            if lst_desig_id:
                str_filter += ' AND desg.fk_group_id IN('+str(lst_desig_id)[1:-1]+')'


            if not request.user.is_superuser:
                if lst_selected_location:
                    lst_loc = list(set(lst_selected_location) & set(request.user.userdetails.json_physical_loc))
                else:
                    lst_loc = request.user.userdetails.json_physical_loc
                int_desig_id = request.user.userdetails.fk_group_id
                int_department_id = request.user.userdetails.fk_department_id
                int_hierarchy_type = request.user.userdetails.int_hierarchy_type

                lst_desig = []
                if not int_hierarchy_type or int_hierarchy_type==0:
                    lst_desig = get_hierarchy([], int_desig_id, [0,1], [])
                elif int_hierarchy_type==1:
                    lst_desig = get_hierarchy([int_department_id], int_desig_id, [0,1], [])
                    str_filter += ' AND dept.pk_bint_id = '+str(int_department_id)
                elif int_hierarchy_type==2:
                    lst_desig = list(HierarchyLevel.objects.filter(fk_reporting_to_id=int_desig_id,int_status=1).values_list('fk_designation_id',flat=True))
                elif int_hierarchy_type==3:
                    lst_desig = list(HierarchyLevel.objects.filter(fk_department_id=int_department_id, fk_reporting_to_id=int_desig_id,int_status=1).values_list('fk_designation_id',flat=True))
                    str_filter += ' AND dept.pk_bint_id = '+str(int_department_id)
                lst_desig = list(set(lst_desig))

                if int_department_id and (request.user.userdetails.fk_department.vchr_name.upper() in ['HR & ADMIN','INTERNAL AUDIT'] or (request.user.userdetails.fk_department.vchr_name.upper() == 'IT PROJECTS' and int_desig_id and request.user.userdetails.fk_desig.vchr_name.upper() == 'HEAD- INFORMATION TECHNOLOGY')):
                    dct_filter['blnDept'] = True
                    dct_filter['blnEmployee'] = True
                    dct_filter['blnBrand'] = True
                    dct_filter['blnPhysicalLoc'] = True
                elif request.user.userdetails.fk_group.vchr_name.upper() in ['MANAGER - BUSINESS OPERATIONS']:
                    dct_filter['blnDept'] = True
                    dct_filter['blnEmployee'] = True
                    dct_filter['blnBrand'] = True
                    dct_filter['blnPhysicalLoc'] = True
                #     lst_hierarchy_des=list(HierarchyLevel.objects.filter(fk_reporting_to_id=int_desig_id,int_status=1).values_list('fk_designation_id',flat=True))
                #     str_filter += ' AND desg.pk_bint_id IN (' + str(lst_desig)[1:-1]+") OR ud.user_ptr_id = "+str(request.user.userdetails.user_ptr_id)
                elif request.user.userdetails.fk_group.vchr_name.upper() in ['GM SPECIAL PROJECTS']:
                    dct_filter['blnDept'] = True
                    dct_filter['blnEmployee'] = True
                    dct_filter['blnBrand'] = True
                    dct_filter['blnPhysicalLoc'] = True
                    if not lst_selected_dept and not int_brand_id and not int_employee_id and not lst_selected_location:
                        lst_dept=list(Department.objects.filter(vchr_name__in=['IT PROJECTS','MYG INFRA','SALES MIT','OPERATIONS'],int_status=1).values_list('pk_bint_id',flat=True))
                        lst_hierarchy_des=get_hierarchy(lst_dept, int_desig_id, [0,1], [])
                        str_filter += ' AND desg.pk_bint_id IN (' + str(lst_hierarchy_des)[1:-1]+")"
                elif request.user.userdetails.fk_group.vchr_name.upper() in ['BUISNESS HEAD','BUSINESS HEAD']:
                    dct_filter['blnDept'] = True
                    dct_filter['blnEmployee'] = True
                    dct_filter['blnBrand'] = True
                    dct_filter['blnPhysicalLoc'] = True
                    str_filter += ' AND desg.pk_bint_id IN (' + str(lst_desig)[1:-1]+")"
                elif lst_desig:
                    dct_filter['blnPhysicalLoc'] = True
                    str_filter += ' AND desg.pk_bint_id IN (' + str(lst_desig)[1:-1]+") AND ud.json_physical_loc ?| ARRAY"+str(lst_loc)
                # elif int_desig_id and int_department_id:
                #     # lst_desig = get_hierarchy([int_department_id], int_desig_id, [0,1])
                #     if lst_desig and lst_loc:
                #         dct_filter['blnPhysicalLoc'] = True
                #         str_filter = ' AND (dept.pk_bint_id = '+str(int_department_id)+' AND desg.pk_bint_id IN('+str(lst_desig)[1:-1]+ ') AND ud.json_physical_loc ?| ARRAY'+str(lst_loc)+' OR ud.user_ptr_id = '+str(request.user.userdetails.user_ptr_id)+')'
                #     else:
                #         str_filter = ' AND ud.user_ptr_id = '+str(request.user.userdetails.user_ptr_id)
                else:
                    str_filter = ' AND ud.user_ptr_id = '+str(request.user.userdetails.user_ptr_id)

                if not lst_selected_location and not lst_selected_dept and not int_employee_id and not int_brand_id and not lst_branch_id and not lst_desig_id:
                    str_filter += " OR ud.user_ptr_id = "+str(request.user.userdetails.user_ptr_id)
            else:
                dct_filter['blnDept'] = True
                dct_filter['blnEmployee'] = True
                dct_filter['blnBrand'] = True
                dct_filter['blnPhysicalLoc'] = True
                dct_filter['blnDesignation'] = True
                dct_filter['blnBranch'] = True
                if lst_desig_id:
                    str_filter += ' AND desg.pk_bint_id IN('+str(lst_desig_id)[1:-1]+')'

            rst_sub_query = str_query + str_filter + ' ORDER BY pl.dat_start'
            lst_status = request.data.get('lstAttendanceStatus')
            if lst_status:
                rst_query = "SELECT * from ("+rst_sub_query+") as sub "
            if not request.data.get('lstAttendanceStatus'):
                rst_attendance = conn.execute(rst_sub_query).fetchall()

            elif 'all' in request.data.get('lstAttendanceStatus'):
                rst_query += "WHERE sub.str_day_type IS NOT NULL"
                rst_attendance = conn.execute(rst_query).fetchall()
            else:
                rst_query += "WHERE sub.str_day_type in ({0})"
                rst_query = rst_query.format(str(lst_status)[1:-1])
                rst_attendance = conn.execute(rst_query).fetchall()
            lst_data = []
            now_date = datetime.now()

            # 0) dur_active, 1) int_log_id, 2) str_emp_name, 3) str_shift_name, 4) vchr_employee_code, 5) vchr_direction, 6) dat_punch, 7) dat_start, 8) dat_end, 9) employeename, 10) str_in_location, 11) str_out_location, 12) json_physical_loc, 13) str_branch_name, 14) vchr_brand_name, 15) str_status
            lst_emp_code=[]
            if not request.user.is_superuser and not request.user.userdetails.fk_department.vchr_name.upper() in ['BUISNESS HEAD']:
                pass
            elif not request.user.is_superuser and not lst_loc and not request.user.userdetails.fk_department.vchr_name.upper() in ['HR & ADMIN','INTERNAL AUDIT','IT PROJECTS']:
                rst_attendance=''

            for ins_data in rst_attendance:
                dct_data = {}
                dct_data['intLogId'] = ins_data[1]
                dct_data['strEMPCode'] = ins_data[4]
                lst_emp_code.append(ins_data[4])
                if ins_data[2].strip():
                    dct_data['strEMPName'] = ins_data[2].title()
                else:
                    dct_data['strEMPName'] = ins_data[9].title()
                if len(dct_data['strEMPName'])>25 and len(dct_data['strEMPName'][:22].strip()) == 22:
                    dct_data['strEMPName'] = dct_data['strEMPName'][:22].strip()+'...'
                dct_data['timFirstPunch'] = '--'
                if ins_data[7]:
                    dct_data['timFirstPunch'] = datetime.strftime(ins_data[7], '%I:%M %p')
                dct_data['strInLocation'] = '--'
                if ins_data[10]:
                    dct_data['strInLocation'] = ins_data[10].title()
                dct_data['timLastPunch'] = '--'
                dct_data['strOutLocation'] = '--'
                if ins_data[8] and ins_data[5]=='OUT':
                    dct_data['timLastPunch'] = datetime.strftime(ins_data[8], '%I:%M %p')
                    if ins_data[11]:
                        dct_data['strOutLocation'] = ins_data[11].title()
                if ins_data[0] and ins_data[5]=='IN' and ins_data[8] and dat_attendance.date()==now_date.date() and ins_data[8].time() <= now_date.time():
                    dct_data['strDuration'] = str(ins_data[0]+(timedelta(hours=now_date.hour,minutes=now_date.minute,seconds=now_date.second)-timedelta(hours=ins_data[8].hour,minutes=ins_data[8].minute,seconds=ins_data[8].second)))[:-3]
                elif ins_data[0]:
                    dct_data['strDuration'] = str(ins_data[0])[:-3]
                elif now_date.date() == dat_attendance.date() and ins_data[7] and ins_data[7].time() <= now_date.time():
                    dct_data['strDuration'] = str(timedelta(hours=now_date.hour,minutes=now_date.minute,seconds=now_date.second)-timedelta(hours=ins_data[7].hour,minutes=ins_data[7].minute,seconds=ins_data[7].second))[:-3]
                else:
                    dct_data['strDuration'] = '--'
                if ins_data[15]:
                    dct_data['strRemarks'] = ins_data[15]
                else:
                    dct_data['strRemarks'] = ''

                dct_data['strDirection'] = '--'
                if ins_data[5]:
                    dct_data['strDirection'] = ins_data[5]
                dct_data['blnCurrDate'] = dat_attendance.date()==datetime.now().date()
                dct_data['strBranchName'] = '--'
                dct_data['strBrandName'] = '--'
                if ins_data[13]:
                    dct_data['strBranchName'] = ins_data[13]
                if ins_data[14]:
                    dct_data['strBrandName'] = ins_data[14]
                lst_data.append(dct_data)
            conn.close()
            return Response({'status':1, 'data':lst_data, 'filters':dct_filter})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def put(self, request):
        try:
            conn = engine.connect()
            int_log_id = request.data.get('intLogId')
            str_query = "SELECT plogdt.tim_start, devin.devicelocation AS str_in_location, plogdt.tim_end, devout.devicelocation AS str_out_location, shft.vchr_name AS str_shift_name, shft.time_shift_from, shft.time_shift_to, shft.bln_time_shift, INITCAP(CASE WHEN shftex.pk_bint_id IS NOT NULL THEN 'Free Shift' WHEN shft.pk_bint_id IS NULL THEN 'Shift Not Assigned' WHEN shft.bln_time_shift = TRUE THEN shft.vchr_name WHEN hldy.vchr_name IS NOT NULL THEN CASE WHEN plog.vchr_direction = 'OUT' THEN CONCAT('Worked on ', hldy.vchr_name) ELSE CONCAT(hldy.vchr_name, ' Holiday') END WHEN (ud.int_weekoff_type = 0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(plog.dat_punch::DATE, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN CASE WHEN plog.vchr_direction = 'OUT' THEN 'Worked on Week Off' ELSE 'Week Off' END WHEN lev.chr_leave_mode ='F' THEN lvtyp.vchr_name WHEN cmblev.chr_leave_mode = 'F' THEN 'Compo-Off' WHEN odr.chr_day_type = 'F' THEN 'On-Duty' WHEN plog.dat_start::TIME > ((CASE WHEN lev.chr_leave_mode ='M' OR cmblev.chr_leave_mode = 'M' OR odr.chr_day_type = 'M' THEN (shft.time_shift_to::TIME - (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_from::TIME END) + (CASE WHEN ltplcy.vchr_name ILIKE '%late%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) AND plog.vchr_direction = 'OUT' AND plog.dat_end::TIME < ((CASE WHEN lev.chr_leave_mode = 'E' OR cmblev.chr_leave_mode = 'E' OR odr.chr_day_type = 'E' THEN (shft.time_shift_from::TIME + (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_to::TIME END) - (CASE WHEN ltplcy.vchr_name ILIKE '%early%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) THEN 'Latecomer and Early Leaver' WHEN plog.dat_start::TIME > ((CASE WHEN lev.chr_leave_mode = 'M' OR cmblev.chr_leave_mode = 'M' OR odr.chr_day_type ='M' THEN (shft.time_shift_to::TIME - (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_from::TIME END) + (CASE WHEN ltplcy.vchr_name ILIKE '%late%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) THEN 'Latecomer' WHEN plog.vchr_direction = 'OUT' AND plog.dat_end::TIME < ((CASE WHEN lev.chr_leave_mode = 'E' OR cmblev.chr_leave_mode = 'E' OR odr.chr_day_type = 'E' THEN (shft.time_shift_from::TIME + (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_to::TIME END) - (CASE WHEN ltplcy.vchr_name ILIKE '%early%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) THEN 'Early Leaver' WHEN plog.dat_start::TIME <= ((CASE WHEN lev.chr_leave_mode = 'M' OR cmblev.chr_leave_mode = 'M' OR odr.chr_day_type ='M' THEN (shft.time_shift_to::TIME - (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_from::TIME END) + (CASE WHEN ltplcy.vchr_name ILIKE '%late%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) AND plog.vchr_direction = 'OUT' AND plog.dat_end::TIME >= ((CASE WHEN lev.chr_leave_mode = 'E' OR cmblev.chr_leave_mode = 'E' OR odr.chr_day_type = 'E' THEN (shft.time_shift_from::TIME + (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END)) ELSE shft.time_shift_to::TIME END) - (CASE WHEN ltplcy.vchr_name ILIKE '%early%' THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END)) THEN 'On Time' END) AS str_status FROM punch_log_detail plogdt JOIN punch_log plog ON plog.pk_bint_id = plogdt.fk_log_id JOIN punching_emp pemp ON pemp.pk_bint_id = plog.fk_punchingemp_id LEFT JOIN user_details ud ON ud.user_ptr_id = pemp.fk_user_id LEFT JOIN devices devin ON devin.deviceid = plog.int_start_device_id LEFT JOIN devices devout ON devout.deviceid = plog.int_end_device_id LEFT JOIN employee_shift eshft ON eshft.fk_employee_id = ud.user_ptr_id AND eshft.bln_active = TRUE LEFT JOIN shift_allocation salloc ON salloc.fk_employee_id = ud.user_ptr_id AND salloc.int_status IN (0, 2) AND salloc.dat_shift = plog.dat_punch LEFT JOIN shift_schedule shft ON shft.pk_bint_id = (CASE WHEN eshft.int_shift_type = 0 THEN (eshft.json_shift#>>'{lstShift,0}')::INT WHEN eshft.int_shift_type = 1 THEN salloc.fk_shift_id END) LEFT JOIN (late_hours_request ltrqst JOIN late_hours_policy ltplcy ON ltplcy.pk_bint_id = ltrqst.fk_late_hours_policy_id) ON ltrqst.fk_employee_id = ud.user_ptr_id AND ltrqst.dat_requested = plog.dat_punch AND ltrqst.int_status IN (1, 2) LEFT JOIN leave lev ON lev.dat_from <= plog.dat_punch AND lev.dat_to >= plog.dat_punch AND lev.int_status = 2 AND lev.fk_user_id = ud.user_ptr_id LEFT JOIN leave_type lvtyp ON lvtyp.pk_bint_id = lev.fk_leave_type_id LEFT JOIN combo_off_users cmblev ON cmblev.dat_leave = plog.dat_punch AND cmblev.int_status = 2 AND cmblev.fk_user_id = ud.user_ptr_id LEFT JOIN on_duty_request odr ON odr.fk_requested_id = ud.user_ptr_id AND odr.dat_request = plog.dat_punch AND odr.int_status = 2 LEFT JOIN holiday hldy ON hldy.dat_holiday = plog.dat_punch AND hldy.bln_active = TRUE LEFT JOIN duty_roster wkoff ON ud.int_weekoff_type=1 AND wkoff.fk_employee_id=ud.user_ptr_id AND wkoff.bln_active=TRUE AND wkoff.json_dates ? plog.dat_punch::TEXT LEFT JOIN shift_exemption shftex ON shftex.int_status = 1 AND shftex.dat_start <= plog.dat_punch::DATE AND shftex.dat_end >= plog.dat_punch::DATE AND (CASE WHEN shftex.int_type = 0 OR (shftex.int_type IN (1, 2, 3) AND (shftex.json_type_ids->>'int_type')::INT = 1) THEN ud.user_ptr_id IN (SELECT JSONB_ARRAY_ELEMENTS_TEXT((shftex.json_type_ids->>'lst_emp_id')::JSONB)::INT) WHEN shftex.int_type = 1 AND (shftex.json_type_ids->>'int_type')::INT = 0 THEN ud.fk_department_id IN (SELECT JSONB_ARRAY_ELEMENTS_TEXT((shftex.json_type_ids->>'lst_type_ids')::JSONB)::INT) WHEN shftex.int_type = 2 AND (shftex.json_type_ids->>'int_type')::INT = 0 THEN ud.fk_desig_id IN (SELECT JSONB_ARRAY_ELEMENTS_TEXT((shftex.json_type_ids->>'lst_type_ids')::JSONB)::INT) WHEN shftex.int_type = 3 AND (shftex.json_type_ids->>'int_type')::INT = 0 THEN ud.fk_branch_id IN (SELECT JSONB_ARRAY_ELEMENTS_TEXT((shftex.json_type_ids->>'lst_type_ids')::JSONB)::INT) END) AND (CASE WHEN (shftex.json_type_ids->>'lst_exclude_ids')::JSONB IS NOT NULL THEN ud.user_ptr_id NOT IN (SELECT JSONB_ARRAY_ELEMENTS_TEXT((shftex.json_type_ids->>'lst_exclude_ids')::JSONB)::INT) END) WHERE plog.pk_bint_id = " + str(int_log_id) + "ORDER BY plogdt.tim_start"

            rst_attendance = conn.execute(sqlalchemy.text(str_query)).fetchall()

            # session = Connection()
            # rst_attendance = session.query(PunchLogDetailSA.tim_start, ShiftExemptionJs.c.pk_bint_id.label('exempt_id'), PunchLogDetailSA.tim_end, case([(ShiftExemptionJs.c.pk_bint_id!=None, literal_column("'Free Shift'")), (PunchLogSA.int_ellc==-1, literal_column("'Early Leaver'")),\
            #                     (PunchLogSA.int_ellc==0, literal_column("'On Time'")), (PunchLogSA.int_ellc==1, literal_column("'Latecomer'")), (PunchLogSA.int_ellc==2, literal_column("'Latecomer and Early Leaver'"))], else_=literal_column("'Shift Not Assigned'")).label('str_status'),\
            #                     ShiftScheduleSA.vchr_name.label('str_shift_name'), ShiftScheduleSA.time_shift_from, ShiftScheduleSA.time_shift_to, DevicesSA.devicelocation.label('str_in_location'), DeviceAliasSA.devicelocation.label('str_out_location'))\
            #                     .join(PunchLogSA, PunchLogSA.pk_bint_id == PunchLogDetailSA.fk_log_id)\
            #                     .join(PunchingEmpSA, PunchingEmpSA.pk_bint_id == PunchLogSA.fk_punchingemp_id)\
            #                     .outerjoin(UserDetailsSA, UserDetailsSA.user_ptr_id == PunchingEmpSA.fk_user_id)\
            #                     .outerjoin(ShiftScheduleSA, ShiftScheduleSA.pk_bint_id == PunchLogSA.fk_shift_id)\
            #                     .outerjoin(DevicesSA, DevicesSA.deviceid == PunchLogDetailSA.int_start_device_id)\
            #                     .outerjoin(DeviceAliasSA, DeviceAliasSA.deviceid == PunchLogDetailSA.int_end_device_id)\
            #                     .outerjoin(ShiftExemptionJs, and_(ShiftExemptionJs.c.dat_start <= PunchLogSA.dat_punch, ShiftExemptionJs.c.dat_end >= PunchLogSA.dat_punch, ShiftExemptionJs.c.int_status == 1,
            #                     or_(and_(or_(ShiftExemptionJs.c.int_type == 0, and_(ShiftExemptionJs.c.int_type.in_([1,2,3]), ShiftExemptionJs.c.json_type_ids['int_type'].astext.cast(Integer) == 1)), ShiftExemptionJs.c.json_type_ids['lst_emp_id'].has_any(array([cast(UserDetailsSA.user_ptr_id, String)]))),
            #                     and_(ShiftExemptionJs.c.int_type == 1, ShiftExemptionJs.c.json_type_ids['lst_type_ids'].has_any(array([cast(UserDetailsSA.fk_department_id, String)])), ShiftExemptionJs.c.json_type_ids['lst_exclude_ids'].has_any(array([cast(UserDetailsSA.user_ptr_id, String)])) == False),
            #                     and_(ShiftExemptionJs.c.int_type == 2, ShiftExemptionJs.c.json_type_ids['lst_type_ids'].has_any(array([cast(UserDetailsSA.fk_desig_id, String)])), ShiftExemptionJs.c.json_type_ids['lst_exclude_ids'].has_any(array([cast(UserDetailsSA.user_ptr_id, String)])) == False),
            #                     and_(ShiftExemptionJs.c.int_type == 3, ShiftExemptionJs.c.json_type_ids['lst_type_ids'].has_any(array([cast(UserDetailsSA.fk_branch_id, String)])), ShiftExemptionJs.c.json_type_ids['lst_exclude_ids'].has_any(array([cast(UserDetailsSA.user_ptr_id, String)])) == False))))\
            #                     .filter(PunchLogSA.pk_bint_id == int_log_id)\
            #                     .order_by(PunchLogDetailSA.tim_start)


            lst_data = []
            now_date = datetime.now().time()
            dct_shift = {}
            dct_shift['strShiftName'] = '--'
            dct_shift['strShiftStart'] = '--'
            dct_shift['strShiftEnd'] = '--'
            for ins_data in rst_attendance:
                ins_data = dict(ins_data)
                dct_data = {}
                dct_data['timStart'] = ins_data['tim_start'].strftime("%I:%M %p")
                dct_data['strInLocation'] = '--'
                if ins_data['str_in_location']:
                    dct_data['strInLocation'] = ins_data['str_in_location'].title()
                dct_data['timEnd'] = '--'
                dct_data['strOutLocation'] = '--'
                dct_shift['strEmpStatus'] = ins_data['str_status']
                if ins_data['str_shift_name']:
                    dct_shift['strShiftName'] = ins_data['str_shift_name']
                    if not ins_data['bln_time_shift']:
                        dct_shift['strShiftStart'] = ins_data['time_shift_from'].strftime("%I:%M %p")
                        dct_shift['strShiftEnd'] = ins_data['time_shift_to'].strftime("%I:%M %p")
                if ins_data['tim_end']:
                    if ins_data['str_out_location']:
                        dct_data['strOutLocation'] = ins_data['str_out_location'].title()
                    dct_data['timEnd'] = ins_data['tim_end'].strftime("%I:%M %p")
                    dct_data['strDuration'] = str(timedelta(hours=ins_data['tim_end'].hour, minutes=ins_data['tim_end'].minute, seconds=ins_data['tim_end'].second)-timedelta(hours=ins_data['tim_start'].hour, minutes=ins_data['tim_start'].minute, seconds=ins_data['tim_start'].second))
                else:
                    dct_data['strDuration'] = str(timedelta(hours=now_date.hour, minutes=now_date.minute, seconds=now_date.second)-timedelta(hours=ins_data['tim_start'].hour, minutes=ins_data['tim_start'].minute, seconds=ins_data['tim_start'].second))
                lst_data.append(dct_data)
            conn.close()
            return Response({'status':1, 'data':lst_data, 'dct_shift':dct_shift})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class AttendanceDetails(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        """ Employee Wise Monthly PunchLog Details """
        try:
            conn = engine.connect()
            int_emp_id = request.data.get('intEmpId')
            int_month = request.data.get('intMonth')
            int_year = request.data.get('intYear')
            now_date = datetime.now()
            dur_calendar = calendar.monthrange(int_year, int_month)
            str_start_date = str(int_year)+'-'+str(int_month)+'-1'
            str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(dur_calendar[1])

            # if not request.user.is_superuser:
            #     ins_admin = AdminSettings.objects.filter(vchr_code='PAYROLL_PERIOD',bln_enabled=True,fk_company_id=request.user.userdetails.fk_company_id).values('vchr_value', 'int_value').first()
            #     if ins_admin and ins_admin['int_value'] != 0:
            #         str_start_date = str(int_year)+'-'+str(int_month+ins_admin['int_value'])+'-'+ins_admin['vchr_value'][0]
            #         str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(int(ins_admin['vchr_value'][0])-1)

            if int_month == now_date.month and int_year == now_date.year and now_date.day <= int(str_end_date.split('-')[2]):
                str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(now_date.day)

            dct_filter = {}
            dct_filter['blnEmployee'] = True

            str_query = "SELECT sris.dat_punch, plog.pk_bint_id, plog.dat_start AS tim_in, INITCAP(indev.devicelocation) AS str_in_location, plog.dat_end AS tim_end, CASE WHEN plog.vchr_direction='OUT' THEN INITCAP(outdev.devicelocation) END AS str_out_location, (plog.dat_end - plog.dat_start) AS tim_duration, plog.vchr_direction, INITCAP(CASE WHEN hldy.pk_bint_id IS NOT NULL THEN CASE WHEN plog.vchr_direction = 'OUT' THEN CONCAT('Worked on ', hldy.vchr_name) ELSE CONCAT(hldy.vchr_name,' ', 'Holiday') END WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN CASE WHEN plog.vchr_direction='OUT' THEN 'Worked on Week Off' ELSE 'Week Off' END WHEN wklv.pk_bint_id IS NOT NULL THEN CONCAT('Week Off', CASE WHEN wklv.int_status = 1 THEN ' Pending Approval' WHEN wklv.int_status = 2 THEN ' Pending Verification' END) WHEN lev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN lev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' ', lvtyp.vchr_name, CASE WHEN lev.int_status = 1 THEN ' Pending Approval' END) WHEN cmblev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN cmblev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' Combo Off', CASE WHEN cmblev.int_status = 1 THEN ' Pending Approval' END) WHEN odr.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN odr.chr_day_type='F' THEN 'Full Day' ELSE 'Half Day' END, ' On-Duty', CASE WHEN odr.int_status = 0 THEN ' Pending Approval' WHEN odr.int_status = 1 THEN ' Pending Verification' END) WHEN plog.vchr_direction='IN' AND sris.dat_punch != NOW()::DATE THEN 'Punch-Out Missing' WHEN plog.dat_punch IS NULL AND sris.dat_punch<=now()::date THEN 'Absent' WHEN ltplcy.pk_bint_id IS NOT NULL THEN CONCAT(ltplcy.vchr_name, CASE WHEN ltrqst.int_status = 0 THEN ' Pending Approval' END) END) AS str_status,(CASE WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN 'weekOff' WHEN cmblev.pk_bint_id IS NOT NULL THEN 'comboOff' WHEN hldy.pk_bint_id IS NOT NULL THEN 'holiDay' WHEN lev.pk_bint_id IS NOT NULL THEN 'leave' WHEN odr.pk_bint_id IS NOT NULL THEN 'onDuty' WHEN plog.dat_punch IS NULL AND sris.dat_punch<=now()::date THEN 'absent' END) AS str_day_type FROM user_details AS ud JOIN auth_user au ON au.id=ud.user_ptr_id LEFT JOIN job_position desg ON desg.pk_bint_id=ud.fk_desig_id LEFT JOIN department dept ON dept.pk_bint_id=ud.fk_department_id LEFT JOIN branch br ON br.pk_bint_id=ud.fk_branch_id LEFT JOIN brands brnd ON brnd.pk_bint_id=ud.fk_brand_id RIGHT JOIN (SELECT (GENERATE_SERIES('"+str_start_date+"'::DATE, '"+str_end_date+"'::DATE, '1 day'::INTERVAL)::DATE) AS dat_punch) AS sris ON true LEFT JOIN punching_emp pemp ON pemp.fk_user_id=ud.user_ptr_id LEFT JOIN punch_log plog ON plog.fk_punchingemp_id=pemp.pk_bint_id AND plog.dat_punch=sris.dat_punch LEFT JOIN devices indev ON indev.deviceid=plog.int_start_device_id LEFT JOIN devices outdev ON outdev.deviceid=plog.int_end_device_id LEFT JOIN holiday hldy ON hldy.dat_holiday=sris.dat_punch AND hldy.bln_active = TRUE LEFT JOIN duty_roster wkoff ON ud.int_weekoff_type=1 AND wkoff.fk_employee_id=ud.user_ptr_id AND wkoff.bln_active=TRUE AND wkoff.json_dates ? sris.dat_punch::text LEFT JOIN weekoff_leave wklv ON wklv.fk_employee_id = ud.user_ptr_id AND wklv.dat_from <= sris.dat_punch::DATE AND wklv.dat_to >= sris.dat_punch::DATE AND wklv.int_status IN (1, 2) LEFT JOIN leave lev ON lev.dat_from<=sris.dat_punch AND lev.dat_to>=sris.dat_punch AND lev.int_status NOT IN (3, 4) AND lev.fk_user_id=ud.user_ptr_id LEFT JOIN combo_off_users cmblev ON cmblev.dat_leave = sris.dat_punch AND cmblev.int_status IN (1, 2) AND cmblev.fk_user_id=ud.user_ptr_id LEFT JOIN leave_type lvtyp ON lvtyp.pk_bint_id=lev.fk_leave_type_id LEFT JOIN on_duty_request odr ON odr.fk_requested_id = ud.user_ptr_id AND odr.dat_request = sris.dat_punch AND odr.int_status != -1 LEFT JOIN (late_hours_request ltrqst JOIN late_hours_policy ltplcy ON ltplcy.pk_bint_id = ltrqst.fk_late_hours_policy_id) ON ltrqst.dat_requested::DATE = sris.dat_punch::DATE AND ltrqst.fk_employee_id = ud.user_ptr_id AND ltrqst.int_status != -1 WHERE au.is_active=TRUE"
            # 0 dat_punch
            # 1 pk_bint_id
            # 2 tim_in
            # 3 str_in_location
            # 4 tim_end
            # 5 str_out_location
            # 6 tim_duration
            # 7 vchr_direction
            # 8 str_status

            if not request.user.is_superuser:
                int_desig_id = request.user.userdetails.fk_desig_id
                int_department_id = request.user.userdetails.fk_department_id
                if int_desig_id and int_department_id and not request.user.userdetails.fk_department.vchr_name.upper() in ['HR & ADMIN','INTERNAL AUDIT'] and not request.user.userdetails.fk_desig.vchr_name.upper() in ['GM SPECIAL PROJECTS','BUISNESS HEAD','BUSINESS HEAD','MANAGER - BUSINESS OPERATIONS'] and not get_data(int_department_id, int_desig_id, []):
                    dct_filter['blnEmployee'] = False
                    str_query += ' AND ud.user_ptr_id='+str(request.user.userdetails.user_ptr_id)
                elif int_emp_id:
                    str_query += ' AND ud.user_ptr_id='+str(int_emp_id)
                else:
                    str_query += ' AND ud.user_ptr_id='+str(request.user.userdetails.user_ptr_id)
            elif int_emp_id:
                str_query += ' AND ud.user_ptr_id='+str(int_emp_id)
            else:
                str_query = ''
            rst_query = ''
            if not str_query:
                conn.close()
                return Response({'status':1, 'data':[], 'filters':dct_filter})
            if str_query:
                rst_sub_query = str_query+' ORDER BY sris.dat_punch'
                lst_status = request.data.get('lstAttendanceStatus')
                if lst_status:
                    rst_query = "SELECT * from ("+rst_sub_query+") as sub "
                if not request.data.get('lstAttendanceStatus'):
                    rst_attendance = conn.execute(rst_sub_query).fetchall()
                elif 'all' in request.data.get('lstAttendanceStatus'):
                    rst_query += "WHERE sub.str_day_type IS NOT NULL"
                    rst_attendance = conn.execute(rst_query).fetchall()
                else:
                    rst_query += "WHERE sub.str_day_type in ({0})"
                    rst_query = rst_query.format(str(lst_status)[1:-1])
                    rst_attendance = conn.execute(rst_query).fetchall()
            lst_data = []
            for ins_data in rst_attendance:
                dct_data = {}
                dct_data['datPunch'] = datetime.strftime(ins_data[0],"%d-%m-%Y")
                if ins_data[6] and ins_data[7] == 'IN' and ins_data[0] == now_date.date() and ins_data[4].time() <= now_date.time():
                    dct_data['strDuration'] = str(ins_data[6]+(timedelta(hours=now_date.hour,minutes=now_date.minute,seconds=now_date.second)-timedelta(hours=ins_data[4].hour,minutes=ins_data[4].minute,seconds=ins_data[4].second)))[:-3]
                elif ins_data[6]:
                    dct_data['strDuration'] = str(ins_data[6])[:-3]
                elif ins_data[0] == now_date.date() and ins_data[2] and ins_data[2].time() <= now_date.time():
                    dct_data['strDuration'] = str(timedelta(hours=now_date.hour,minutes=now_date.minute,seconds=now_date.second)-timedelta(hours=ins_data[2].hour,minutes=ins_data[2].minute,seconds=ins_data[2].second))[:-3]
                else:
                    dct_data['strDuration'] = '--'
                dct_data['strDirection'] = ins_data[7]
                dct_data['intLogId'] = ins_data[1]
                dct_data['timFirstPunch'] = '--'
                if ins_data[2]:
                    dct_data['timFirstPunch'] = datetime.strftime(ins_data[2],"%I:%M %p")
                dct_data['strInLocation'] = '--'
                if ins_data[3]:
                    dct_data['strInLocation'] = ins_data[3].title()
                dct_data['timLastPunch'] = '--'
                dct_data['strOutLocation'] = '--'
                dct_data['blnCurrDate'] = ins_data[0]==datetime.now().date()
                if ins_data[4] and ins_data[7]=='OUT':
                    dct_data['timLastPunch'] = datetime.strftime(ins_data[4],"%I:%M %p")
                    if ins_data[5]:
                        dct_data['strOutLocation'] = ins_data[5].title()
                dct_data['strStatus'] = ins_data[8]
                lst_data.append(dct_data)
            conn.close()
            return Response({'status':1, 'data':lst_data, 'filters':dct_filter})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'Reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class AuditMonthWise(APIView):
    permission_classes=[IsAuthenticated]
    '''month wise duration for audit'''
    def post(self,request):
        try:
            conn = engine.connect()
            int_month = request.data.get('int_month')
            int_year = request.data.get('int_year')
            dat_selected = request.data.get('dat_selected')

            dur_calendar = calendar.monthrange(int_year, int_month)
            str_start_date = str(int_year)+'-'+str(int_month)+'-1'
            str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(dur_calendar[1])

            if not request.user.is_superuser:
                ins_admin = AdminSettings.objects.filter(vchr_code='PAYROLL_PERIOD',bln_enabled=True,fk_company_id=request.user.userdetails.fk_company_id).values('vchr_value', 'int_value').first()
                if ins_admin and ins_admin['int_value'] != 0:
                    if dat_selected and int(ins_admin['vchr_value']) < dat_selected.day:
                        dat_next_month = datetime.strptime(str(int_year)+'-'+str(int_month)+'-'+ins_admin['vchr_value'],'%Y-%m-%d')+timedelta(days=dur_calendar[1]-int(ins_admin['vchr_value'])+1)
                        int_month = dat_next_month.month
                        int_year = dat_next_month.year
                    str_start_date = datetime.strftime(datetime.strptime(str(int_year)+'-'+str(int_month)+'-'+ins_admin['vchr_value'][0],'%Y-%m-%d')+timedelta(days=int(ins_admin['vchr_value'][0])*ins_admin['int_value']),'%Y-%m-')+ins_admin['vchr_value'][0]
                    str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(int(ins_admin['vchr_value'][0])-1)
            now_date = datetime.now()
            if int_month == now_date.month and int_year == now_date.year and now_date.day <= int(str_end_date.split('-')[2]):
                str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(now_date.day)

            ins_punch_log = PunchLog.objects.filter(fk_punchingemp__fk_user__fk_department__vchr_name__in=["INTERNAL AUDIT","AUDITING"],dat_punch__gte=datetime.strptime(str_start_date,'%Y-%m-%d'),dat_punch__lte=datetime.strptime(str_end_date,'%Y-%m-%d'),fk_punchingemp__fk_user__is_active=True).values('fk_punchingemp__fk_user__first_name','fk_punchingemp__fk_user__last_name','fk_punchingemp__fk_user__vchr_employee_code').annotate(int_dur_active=Sum('dur_active'))
            lst_audit=[]

            for data in ins_punch_log:
                dct_data={}
                dct_data['EmpName']=data['fk_punchingemp__fk_user__first_name']+' '+data['fk_punchingemp__fk_user__last_name']
                dct_data['EmpCode']=data['fk_punchingemp__fk_user__vchr_employee_code']
                dct_data['DurActive']='--'
                if data['int_dur_active']:
                    dct_data['DurActive']=round(data['int_dur_active'].total_seconds()//3600)+((data['int_dur_active'].seconds//60)%60/100)

                lst_audit.append(dct_data)
            conn.close()
            return Response({'status':1,'lst_audit':lst_audit})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class AttendanceExport(APIView):
    permission_classes=[IsAuthenticated]
    '''Attendance Export To Excel'''
    def post(self,request):
        try:
            conn = engine.connect()
            str_dat_from = request.data.get('datFrom')
            str_dat_to = request.data.get('datTo')

            str_query = "SELECT sris.dat_punch, ud.vchr_employee_code, INITCAP(CONCAT(au.first_name, ' ', CASE WHEN ud.vchr_middle_name IS NOT NULL THEN CONCAT(ud.vchr_middle_name, ' ', au.last_name) ELSE au.last_name END)) AS str_emp_name, INITCAP(dept.vchr_name) AS str_department, INITCAP(desg.vchr_name) AS str_designation, INITCAP(br.vchr_name) AS str_branch, plog.dat_start AS tim_in, INITCAP(indev.devicelocation) AS str_in_location, CASE WHEN plog.vchr_direction='OUT' THEN plog.dat_end END AS tim_end, CASE WHEN plog.vchr_direction='OUT' THEN INITCAP(outdev.devicelocation) END AS str_out_location, (CASE WHEN plog.vchr_direction = 'OUT' THEN (plog.dat_end - plog.dat_start) WHEN plog.dur_active IS NOT NULL THEN plog.dur_active END) AS tim_duration, INITCAP(CASE WHEN hldy.pk_bint_id IS NOT NULL THEN CASE WHEN plog.vchr_direction='OUT' THEN CONCAT('Worked on ', hldy.vchr_name) ELSE CONCAT(hldy.vchr_name,' ', 'Holiday') END WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN CASE WHEN plog.vchr_direction='OUT' THEN 'Worked on Week Off' ELSE 'Week Off' END WHEN wklv.pk_bint_id IS NOT NULL THEN CONCAT('Week Off', CASE WHEN wklv.int_status = 1 THEN ' Pending Approval' WHEN wklv.int_status = 2 THEN ' Pending Verification' END) WHEN lev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN lev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' ', lvtyp.vchr_name, CASE WHEN lev.int_status = 1 THEN ' Pending Approval' END) WHEN cmblev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN cmblev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' Combo Off', CASE WHEN cmblev.int_status = 1 THEN ' Pending Approval' END) WHEN odr.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN odr.chr_day_type='F' THEN 'Full Day' ELSE 'Half Day' END, ' On-Duty', CASE WHEN odr.int_status = 0 THEN ' Pending Approval' WHEN odr.int_status = 1 THEN ' Pending Verification' END) WHEN plog.vchr_direction='IN' AND (CASE WHEN plog.vchr_direction = 'OUT' THEN (plog.dat_end - plog.dat_start) WHEN plog.dur_active IS NOT NULL THEN plog.dur_active END) IS NOT NULL THEN (CASE WHEN shft.pk_bint_id IS NULL THEN 'Shift Not Assigned' WHEN (CASE WHEN plog.vchr_direction = 'OUT' THEN (plog.dat_end - plog.dat_start) WHEN plog.dur_active IS NOT NULL THEN plog.dur_active END) + (CASE WHEN ltrqst.int_status IN (1, 2) THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END) < (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END) THEN 'Absent' WHEN (CASE WHEN plog.vchr_direction = 'OUT' THEN (plog.dat_end - plog.dat_start) WHEN plog.dur_active IS NOT NULL THEN plog.dur_active END) + (CASE WHEN ltrqst.int_status IN (1, 2) THEN ('01:00:00'::INTERVAL)*ltplcy.dbl_hours ELSE '00:00:00'::INTERVAL END) < (CASE WHEN shft.time_full_day IS NOT NULL THEN shft.time_full_day::INTERVAL WHEN shft.time_shed_hrs IS NOT NULL THEN shft.time_shed_hrs::INTERVAL ELSE (shft.time_shift_to-shft.time_shift_from) END) THEN 'Half Day' ELSE 'Full Day' END) WHEN plog.vchr_direction = 'IN' AND plog.dat_punch != NOW()::DATE THEN 'Punch-Out Missing' WHEN (plog.dat_punch IS NULL OR (CASE WHEN plog.vchr_direction = 'OUT' THEN (plog.dat_end - plog.dat_start) WHEN plog.dur_active IS NOT NULL THEN plog.dur_active END) IS NULL) AND sris.dat_punch<=now()::date THEN 'Absent' WHEN ltrqst.int_status IN (1, 2) THEN ltplcy.vchr_name END) AS str_status,(CASE WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN 'weekOff' WHEN cmblev.pk_bint_id IS NOT NULL THEN 'comboOff' WHEN hldy.pk_bint_id IS NOT NULL THEN 'holiDay' WHEN lev.pk_bint_id IS NOT NULL THEN 'leave' WHEN odr.pk_bint_id IS NOT NULL THEN 'onDuty' WHEN (plog.dat_punch IS NULL OR plog.dur_active IS NULL) AND sris.dat_punch<=now()::date THEN 'absent' END) AS str_day_type FROM user_details AS ud JOIN auth_user au ON au.id=ud.user_ptr_id LEFT JOIN job_position desg ON desg.pk_bint_id=ud.fk_desig_id LEFT JOIN department dept ON dept.pk_bint_id=ud.fk_department_id LEFT JOIN branch br ON br.pk_bint_id=ud.fk_branch_id LEFT JOIN brand brnd ON brnd.pk_bint_id=ud.fk_brand_id RIGHT JOIN (SELECT (GENERATE_SERIES('"+str_dat_from+"'::DATE, '"+str_dat_to+"'::DATE, '1 day'::INTERVAL)::DATE) AS dat_punch) AS sris ON true LEFT JOIN punching_emp pemp ON pemp.fk_user_id=ud.user_ptr_id LEFT JOIN punch_log plog ON plog.fk_punchingemp_id=pemp.pk_bint_id AND plog.dat_punch=sris.dat_punch LEFT JOIN devices indev ON indev.deviceid=plog.int_start_device_id LEFT JOIN devices outdev ON outdev.deviceid=plog.int_end_device_id LEFT JOIN holiday hldy ON hldy.dat_holiday=sris.dat_punch AND hldy.bln_active = TRUE LEFT JOIN duty_roster wkoff ON ud.int_weekoff_type=1 AND wkoff.fk_employee_id=ud.user_ptr_id AND wkoff.bln_active=TRUE AND wkoff.json_dates ? sris.dat_punch::text LEFT JOIN weekoff_leave wklv ON wklv.fk_employee_id = ud.user_ptr_id AND wklv.dat_from <= sris.dat_punch::DATE AND wklv.dat_to >= sris.dat_punch::DATE AND wklv.int_status IN (1, 2) LEFT JOIN leave lev ON lev.dat_from<=sris.dat_punch AND lev.dat_to>=sris.dat_punch AND lev.int_status NOT IN (3, 4) AND lev.fk_user_id=ud.user_ptr_id LEFT JOIN combo_off_users cmblev ON cmblev.dat_leave=sris.dat_punch AND cmblev.int_status IN (1, 2) AND cmblev.fk_user_id=ud.user_ptr_id LEFT JOIN leave_type lvtyp ON lvtyp.pk_bint_id=lev.fk_leave_type_id LEFT JOIN on_duty_request odr ON odr.fk_requested_id = ud.user_ptr_id AND odr.dat_request = sris.dat_punch AND odr.int_status != -1 LEFT JOIN employee_shift eshft ON eshft.fk_employee_id=ud.user_ptr_id AND eshft.bln_active=TRUE LEFT JOIN shift_allocation AS alctn ON alctn.fk_employee_id = ud.user_ptr_id AND alctn.dat_shift = sris.dat_punch AND alctn.int_status IN (0,2) LEFT JOIN shift_schedule shft ON shft.pk_bint_id = (CASE WHEN eshft.int_shift_type = 0 THEN (eshft.json_shift#>>'{lstShift,0}')::INT ELSE alctn.fk_shift_id END) LEFT JOIN (late_hours_request ltrqst JOIN late_hours_policy ltplcy ON ltplcy.pk_bint_id = ltrqst.fk_late_hours_policy_id) ON ltrqst.dat_requested::DATE = sris.dat_punch::DATE AND ltrqst.fk_employee_id = ud.user_ptr_id AND ltrqst.int_status != -1 WHERE au.is_active=TRUE"
            #
            # str_query = "SELECT sris.dat_punch, ud.vchr_employee_code, INITCAP(CONCAT(au.first_name, ' ', CASE WHEN ud.vchr_middle_name IS NOT NULL THEN CONCAT(ud.vchr_middle_name, ' ', au.last_name) ELSE au.last_name END)) AS str_emp_name, INITCAP(dept.vchr_name) AS str_department, INITCAP(desg.vchr_name) AS str_designation, INITCAP(br.vchr_name) AS str_branch, plog.dat_start AS tim_in, INITCAP(indev.devicelocation) AS str_in_location, CASE WHEN plog.vchr_direction='OUT' THEN plog.dat_end END AS tim_end, CASE WHEN plog.vchr_direction='OUT' THEN INITCAP(outdev.devicelocation) END AS str_out_location, plog.dur_active AS tim_duration, INITCAP(CASE WHEN hldy.pk_bint_id IS NOT NULL THEN CONCAT(hldy.vchr_name,' ', 'Holiday') WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN 'Week Off' WHEN lev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN lev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' ', lvtyp.vchr_name, CASE WHEN lev.int_status = 1 THEN ' Pending Approval' END) WHEN cmblev.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN cmblev.chr_leave_mode='F' THEN 'Full Day' ELSE 'Half Day' END, ' Combo Off', CASE WHEN cmblev.int_status = 1 THEN ' Pending Approval' END) WHEN odr.pk_bint_id IS NOT NULL THEN CONCAT(CASE WHEN odr.chr_day_type='F' THEN 'Full Day' ELSE 'Half Day' END, ' On-Duty', CASE WHEN odr.int_status = 0 THEN ' Pending Approval' WHEN odr.int_status = 1 THEN ' Pending Verification' END) WHEN plog.vchr_direction='IN' AND plog.dur_active IS NOT NULL THEN (CASE WHEN shft.pk_bint_id IS NULL THEN 'Shift Not Assigned' WHEN plog.dur_active < (CASE WHEN shft.time_half_day IS NOT NULL THEN shft.time_half_day::INTERVAL WHEN shft.time_full_day IS NOT NULL THEN (shft.time_full_day::INTERVAL)/2 WHEN shft.time_shed_hrs IS NOT NULL THEN (shft.time_shed_hrs::INTERVAL)/2 ELSE (shft.time_shift_to-shft.time_shift_from)/2 END) THEN 'Absent' WHEN plog.dur_active < (CASE WHEN shft.time_full_day IS NOT NULL THEN shft.time_full_day::INTERVAL WHEN shft.time_shed_hrs IS NOT NULL THEN shft.time_shed_hrs::INTERVAL ELSE (shft.time_shift_to-shft.time_shift_from) END) THEN 'Half Day' ELSE 'Full Day' END) WHEN (plog.dat_punch IS NULL OR plog.dur_active IS NULL) AND sris.dat_punch<=now()::date THEN 'Absent' END) AS str_status,(CASE WHEN (ud.int_weekoff_type=0 AND TRIM(ud.vchr_weekoff_day) ILIKE TRIM(TO_CHAR(sris.dat_punch, 'Day'))) OR wkoff.pk_bint_id IS NOT NULL THEN 'weekOff' WHEN cmblev.pk_bint_id IS NOT NULL THEN 'comboOff' WHEN hldy.pk_bint_id IS NOT NULL THEN 'holiDay' WHEN lev.pk_bint_id IS NOT NULL THEN 'leave' WHEN odr.pk_bint_id IS NOT NULL THEN 'onDuty' WHEN (plog.dat_punch IS NULL OR plog.dur_active IS NULL) AND sris.dat_punch<=now()::date THEN 'absent' END) AS str_day_type FROM user_details AS ud JOIN auth_user au ON au.id=ud.user_ptr_id LEFT JOIN job_position desg ON desg.pk_bint_id=ud.fk_desig_id LEFT JOIN department dept ON dept.pk_bint_id=ud.fk_department_id LEFT JOIN branch br ON br.pk_bint_id=ud.fk_branch_id LEFT JOIN brand brnd ON brnd.pk_bint_id=ud.fk_brand_id RIGHT JOIN (SELECT (GENERATE_SERIES('"+str_dat_from+"'::DATE, '"+str_dat_to+"'::DATE, '1 day'::INTERVAL)::DATE) AS dat_punch) AS sris ON true LEFT JOIN punching_emp pemp ON pemp.fk_user_id=ud.user_ptr_id LEFT JOIN punch_log plog ON plog.fk_punchingemp_id=pemp.pk_bint_id AND plog.dat_punch=sris.dat_punch LEFT JOIN devices indev ON indev.deviceid=plog.int_start_device_id LEFT JOIN devices outdev ON outdev.deviceid=plog.int_end_device_id LEFT JOIN holiday hldy ON hldy.dat_holiday=sris.dat_punch LEFT JOIN duty_roster wkoff ON ud.int_weekoff_type=1 AND wkoff.fk_employee_id=ud.user_ptr_id AND wkoff.bln_active=TRUE AND wkoff.json_dates ? sris.dat_punch::text LEFT JOIN leave lev ON lev.dat_from<=sris.dat_punch AND lev.dat_to>=sris.dat_punch AND lev.int_status NOT IN (3, 4) AND lev.fk_user_id=ud.user_ptr_id LEFT JOIN combo_off_users cmblev ON cmblev.dat_leave=sris.dat_punch AND cmblev.int_status IN (1, 2) AND cmblev.fk_user_id=ud.user_ptr_id LEFT JOIN leave_type lvtyp ON lvtyp.pk_bint_id=lev.fk_leave_type_id LEFT JOIN on_duty_request odr ON odr.fk_requested_id = ud.user_ptr_id AND odr.dat_request = sris.dat_punch AND odr.int_status != -1 LEFT JOIN employee_shift eshft ON eshft.fk_employee_id=ud.user_ptr_id AND eshft.bln_active=TRUE LEFT JOIN shift_allocation AS alctn ON alctn.fk_employee_id = ud.user_ptr_id AND alctn.dat_shift = sris.dat_punch AND alctn.int_status IN (0,2) LEFT JOIN shift_schedule shft ON shft.pk_bint_id = (CASE WHEN eshft.int_shift_type = 0 THEN (eshft.json_shift#>>'{lstShift,0}')::INT ELSE alctn.fk_shift_id END) WHERE au.is_active=TRUE"

            str_filter = ''
            if request.data.get('lstBranchId'):
                str_filter += ' AND br.pk_bint_id IN('+str(request.data.get('lstBranchId'))[1:-1]+')'
            if request.data.get('lstDepartmentId'):
                str_filter += ' AND dept.pk_bint_id IN('+str(request.data.get('lstDepartmentId'))[1:-1]+')'
            if request.data.get('lstDesigId'):
                str_filter += ' AND desg.pk_bint_id IN('+str(request.data.get('lstDesigId'))[1:-1]+')'
            if request.data.get('lstBrandId'):
                str_filter += ' AND brnd.pk_bint_id IN('+str(request.data.get('lstBrandId'))[1:-1]+')'
            if request.data.get('intEmployeeId'):
                str_filter += ' AND ud.user_ptr_id IN('+str(request.data.get('intEmployeeId'))+')'

            # rst_attendance = conn.execute(str_query + str_filter + " ORDER BY sris.dat_punch, TRIM(TRIM(TRIM(TRIM(ud.vchr_employee_code,'MYGE-'),'MYGC-'),'MYGT-'),'MYGB-')::INT").fetchall()
            rst_query = ''
            if str_query:
                rst_sub_query = str_query + str_filter + " ORDER BY sris.dat_punch, TRIM(TRIM(TRIM(TRIM(ud.vchr_employee_code,'MYGE-'),'MYGC-'),'MYGT-'),'MYGB-')::int"
                lst_status = request.data.get('lstAttendanceStatus')
                if lst_status:
                    rst_query = "SELECT * from ("+rst_sub_query+") as sub "
                if not request.data.get('lstAttendanceStatus'):
                    rst_attendance = conn.execute(rst_sub_query).fetchall()
                elif 'all' in request.data.get('lstAttendanceStatus'):
                    rst_query += "WHERE sub.str_day_type IS NOT NULL"
                    rst_attendance = conn.execute(rst_query).fetchall()
                else:
                    rst_query += "WHERE sub.str_day_type in ("+str(lst_status)[1:-1]+")"
                    rst_attendance = conn.execute(rst_query).fetchall()
            if not rst_attendance:
                conn.close()
                return Response({'status':0,'message':'No Data'})

            file_name = 'AttendanceReport/Attendance_Report(' + str_dat_from+ '--'+ str_dat_to + ').xlsx'
            if not path.exists(settings.MEDIA_ROOT + '/AttendanceReport/'):
                os.mkdir(settings.MEDIA_ROOT + '/AttendanceReport/')
            writer = pd.ExcelWriter(settings.MEDIA_ROOT + '/' + file_name, engine ='xlsxwriter')
            workbook = writer.book
            head_style = workbook.add_format({'font_size':11, 'bold':1, 'align': 'center','border':1,'border_color':'#000000'})
            head_style.set_pattern(1)
            head_style.set_bg_color('#bfbfbf')
            head_style.set_align('vcenter')

            row_style = workbook.add_format({'font_size':11, 'text_wrap': True})
            row_style.set_align('vcenter')
            worksheet = workbook.add_worksheet()

            title_style = workbook.add_format({'font_size':14, 'bold':1, 'align': 'center', 'border':1})
            title_style.set_align('vcenter')
            title_style.set_pattern(1)
            title_style.set_bg_color('#ffe0cc')
            # str_date = ' ('+datetime.strftime(datetime.strptime(str_dat_from,'%Y-%m-%d'),'%d-%m-%Y')+' To '+datetime.strftime(datetime.strptime(str_dat_from,'%Y-%m-%d'),'%d-%m-%Y')+')'
            worksheet.merge_range('A1+:L1', 'Attendance Report', title_style)
            worksheet.set_row(0, 30)
            worksheet.autofilter('A2:L2')
            worksheet.protect('',{'autofilter':True})

            int_row = 1
            worksheet.write(int_row, 0, 'DATE', head_style)
            worksheet.write(int_row, 1, 'EMP CODE', head_style)
            worksheet.write(int_row, 2, 'EMP NAME', head_style)
            worksheet.write(int_row, 3, 'DEPARTMENT', head_style)
            worksheet.write(int_row, 4, 'DESIGNATION', head_style)
            worksheet.write(int_row, 5, 'BRANCH', head_style)
            worksheet.write(int_row, 6, 'TIME IN', head_style)
            worksheet.write(int_row, 7, 'IN LOCATION', head_style)
            worksheet.write(int_row, 8, 'TIME OUT', head_style)
            worksheet.write(int_row, 9, 'OUT LOCATION', head_style)
            worksheet.write(int_row, 10, 'DURATION', head_style)
            worksheet.write(int_row, 11, 'REMARKS', head_style)
            worksheet.set_column(0, 1, 13)
            worksheet.set_column(2, 3, 30)
            worksheet.set_column(4, 4, 45)
            worksheet.set_column(5, 5, 25)
            worksheet.set_column(6, 6, 12)
            worksheet.set_column(7, 7, 20)
            worksheet.set_column(8, 8, 12)
            worksheet.set_column(9, 9, 20)
            worksheet.set_column(10, 10, 12)
            worksheet.set_column(11, 11, 20)
            worksheet.set_row(int_row, 23)

            for ins_data in rst_attendance:
                int_row += 1
                worksheet.write(int_row, 0, datetime.strftime(ins_data[0],'%d-%m-%Y'), row_style)
                worksheet.write(int_row, 1, ins_data[1], row_style)
                worksheet.write(int_row, 2, ins_data[2], row_style)
                worksheet.write(int_row, 3, ins_data[3], row_style)
                worksheet.write(int_row, 4, ins_data[4], row_style)
                worksheet.write(int_row, 5, ins_data[5], row_style)
                worksheet.write(int_row, 6, datetime.strftime(ins_data[6], '%I:%M %p') if ins_data[6] else '', row_style)
                worksheet.write(int_row, 7, ins_data[7], row_style)
                worksheet.write(int_row, 8, datetime.strftime(ins_data[8], '%I:%M %p') if ins_data[8] else '', row_style)
                worksheet.write(int_row, 9, ins_data[9], row_style)
                worksheet.write(int_row, 10, str(ins_data[10])[:-3] if ins_data[10] else '', row_style)
                worksheet.write(int_row, 11, ins_data[11], row_style)
                worksheet.set_row(int_row, 20, row_style)
            writer.save()
            conn.close()
            return Response({'status':1,'data':request.scheme+'://'+request.get_host()+settings.MEDIA_URL+file_name})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class DayWiseAttendanceReport(APIView):
    permission_classes=[IsAuthenticated]
    '''Attendance Export To Excel'''
    def post(self,request):
        try:
            int_month = int(request.data.get('intMonthYear').split('-')[0])
            int_year = int(request.data.get('intMonthYear').split('-')[1])
            now_date = datetime.now()

            dur_calendar = calendar.monthrange(int_year, int_month)
            str_start_date = str(int_year)+'-'+str(int_month)+'-1'
            str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(dur_calendar[1])

            if not request.user.is_superuser:
                ins_admin = AdminSettings.objects.filter(vchr_code='PAYROLL_PERIOD',bln_enabled=True,fk_company_id=request.user.userdetails.fk_company_id).values('vchr_value', 'int_value').first()
                if ins_admin and ins_admin['int_value'] != 0:
                    str_start_date = datetime.strftime(datetime.strptime(str(int_year)+'-'+str(int_month)+'-'+ins_admin['vchr_value'][0],'%Y-%m-%d')+timedelta(days=int(ins_admin['vchr_value'][0])*ins_admin['int_value']),'%Y-%m-')+ins_admin['vchr_value'][0]
                    str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(int(ins_admin['vchr_value'][0])-1)

            if int_month == now_date.month and int_year == now_date.year and now_date.day <= int(str_end_date.split('-')[2]):
                str_end_date = str(int_year)+'-'+str(int_month)+'-'+str(now_date.day-1)

            dat_month_last = datetime.strptime(str_end_date, '%Y-%m-%d')
            dat_month_first = datetime.strptime(str_start_date, '%Y-%m-%d')

            str_filter = ''
            if request.data.get('intCategoryId'):
                str_filter += ' AND cat.pk_bint_id = '+str(request.data.get('intCategoryId'))
            if request.data.get('lstDesignation'):
                str_filter += ' AND desig.pk_bint_id IN ('+str(request.data.get('lstDesignation'))[1:-1]+')'
            if request.data.get('intDepartmentId'):
                str_filter += ' AND dept.pk_bint_id = '+str(request.data.get('intDepartmentId'))
            if request.data.get('lstBranch'):
                str_filter += ' AND brnch.pk_bint_id IN ('+str(request.data.get('lstBranch'))[1:-1]+')'
            if request.data.get('lstEmployee'):
                str_filter += ' AND ud.user_ptr_id IN('+str(request.data.get('lstEmployee'))[1:-1]+')'

            lst_data = AllSalaryDetails(request, request.data.get('intMonthYear'), str_start_date, str_end_date, str_filter)
            if not lst_data:
                return Response({'status':0,'reason':'No Data'})

            file_name = 'AttendanceReport/DailyAttendanceReport' + datetime.strftime(date.today(), "%d-%m-%Y") + '.xlsx'
            if path.exists(file_name):
                os.remove(file_name)
            if not path.exists(settings.MEDIA_ROOT + '/AttendanceReport/'):
                os.mkdir(settings.MEDIA_ROOT + '/AttendanceReport/')
            writer = pd.ExcelWriter(settings.MEDIA_ROOT + '/' + file_name, engine ='xlsxwriter')
            workbook = writer.book
            worksheet = workbook.add_worksheet()

            title_style = workbook.add_format({'font_size':14, 'bold':1, 'align': 'center', 'border':1})
            title_style.set_align('vcenter')
            title_style.set_pattern(1)
            title_style.set_bg_color('#ffe0cc')
            worksheet.set_row(0, 30)

            head_style = workbook.add_format({'font_size':11, 'bold':1, 'align': 'center','border':1,'border_color':'#000000', 'text_wrap': True})
            head_style.set_pattern(1)
            head_style.set_bg_color('#bfbfbf')
            head_style.set_align('vcenter')

            row_style = workbook.add_format({'font_size':11})
            row_style.set_align('vcenter')

            worksheet.protect('',{'autofilter':True})

            int_row = 1
            worksheet.write(int_row, 0, 'SL. No', head_style); worksheet.set_column(0, 0, 8)
            worksheet.write(int_row, 1, 'EMP CODE', head_style); worksheet.set_column(1, 1, 13)
            worksheet.write(int_row, 2, 'EMP NAME', head_style);
            worksheet.write(int_row, 3, 'DEPARTMENT', head_style);
            worksheet.write(int_row, 4, 'DESIGNATION', head_style);
            worksheet.write(int_row, 5, 'BRANCH', head_style); worksheet.set_column(2, 5, 30)
            int_col=6
            dat_first = dat_month_first
            while dat_first <= dat_month_last:
                worksheet.write(int_row, int_col, datetime.strftime(dat_first,'%d-%m-%Y'), head_style); worksheet.set_column(int_col, int_col, 28)
                dat_first = dat_first + timedelta(days=1)
                int_col += 1
            worksheet.write(int_row, int_col, 'TOTAL HOUR WORKED', head_style); worksheet.set_column(int_col, int_col, 15)
            int_col += 1
            worksheet.write(int_row, int_col, 'LATE HOUR', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'LATE HOUR DAYS', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'ABSENT', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'LEAVE', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'LOP', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'PRESENT', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'CASUAL LEAVE', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'ON DUTY', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'COMBO OFF', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'WEEK OFF', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'HOLIDAYS', head_style); worksheet.set_column(int_col, int_col, 13)
            int_col += 1
            worksheet.write(int_row, int_col, 'SALARY', head_style); worksheet.set_column(int_col, int_col, 13)
            worksheet.merge_range(0, 0, 0, int_col, 'Attendance Report ('+calendar.month_name[int_month]+' '+str(int_year)+')', title_style)
            worksheet.autofilter(1, 0, 1, int_col)
            worksheet.set_row(int_row, 25)

            for ins_data in lst_data:
                int_row += 1
                worksheet.write(int_row, 0, int_row-1, row_style)
                worksheet.write(int_row, 1, ins_data.get('str_employee_code'), row_style)
                worksheet.write(int_row, 2, ins_data.get('str_emp_name'), row_style)
                worksheet.write(int_row, 3, ins_data.get('str_department'), row_style)
                worksheet.write(int_row, 4, ins_data.get('str_designation'), row_style)
                worksheet.write(int_row, 5, ins_data.get('str_branch'), row_style)
                int_col=6
                dat_first = dat_month_first
                while dat_first <= dat_month_last:
                    worksheet.write(int_row, int_col, ins_data['json_attendance'][datetime.strftime(dat_first,'%d-%m-%Y')], row_style)
                    dat_first = dat_first + timedelta(days=1)
                    int_col += 1
                worksheet.write(int_row, int_col, str(ins_data['dur_worked_hour'].days*24+ins_data['dur_worked_hour'].seconds //3600)+':'+str((ins_data['dur_worked_hour'].seconds % 3600)//60).zfill(2) if ins_data['dur_worked_hour'] else '0:00', row_style)
                int_col += 1
                worksheet.write(int_row, int_col, str(ins_data['dur_less_hours'].days*24+ins_data['dur_less_hours'].seconds //3600)+':'+str((ins_data['dur_less_hours'].seconds % 3600)//60).zfill(2) if ins_data['dur_less_hours'] else '0:00', row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_less_hour_days'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_absent'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_lop_leave'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_tot_lop'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_present'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_leave'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_on_duty'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('dbl_combo'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('int_week_off'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('int_holiday'), row_style)
                int_col += 1
                worksheet.write(int_row, int_col, ins_data.get('Net_Salary'), row_style)
                # worksheet.set_row(int_row, 25)
            writer.save()
            return Response({'status':1, 'data':request.scheme+'://'+request.get_host()+settings.MEDIA_URL+file_name})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})
