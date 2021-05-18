from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from bonus.models import BonusDetails,BonusPaid
from datetime import datetime
from user_model.models import ReligionCaste, UserDetails
from department.models import Department
from job_position.models import JobPosition
import sys, os
from HRMS_python import ins_logger
from HRMS_python.dftosql import Savedftosql
from django.db.models.functions import Concat
from django.db.models import Value
from salary_process.models import SalaryDetails
from dateutil.relativedelta import relativedelta
from django.db.models import F, Q, Value, Case, When, IntegerField, CharField, DateField,BooleanField, Count, ExpressionWrapper, Func

sqlalobj = Savedftosql('','')
engine = sqlalobj.engine
# Create your views here.


class SaveBonus(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            rst_bonus_details = request.data
            # int_month = int(rst_bonus_details['intMonthYear'].split('-')[0])
            # int_year = int(rst_bonus_details['intMonthYear'].split('-')[1])

            ins_dept = Department.objects.filter(pk_bint_id = rst_bonus_details["intDeptId"]).first()
            ins_desig = JobPosition.objects.filter(pk_bint_id = rst_bonus_details["intDesigId"]).first()
            ins_religion = ReligionCaste.objects.filter(pk_bint_id = rst_bonus_details["intReligionId"]).first()



            if rst_bonus_details.get("pk_bint_id"):
                rst_bonus_paid = BonusPaid.objects.filter(fk_bonus_id = rst_bonus_details.get("pk_bint_id")).values()
                if rst_bonus_paid:
                    return Response({"status":0,'reason':'Can not make changes on this Bonus'})
                BonusDetails.objects.filter(pk_bint_id = rst_bonus_details["pk_bint_id"]).update( fk_updated_id = request.user.id,
                                                                                                  dat_updated = datetime.now(),
                                                                                                  int_status = 0
                                                                                                 )
                ins_bonus_details = BonusDetails.objects.create( dbl_gross_from = rst_bonus_details["dblGrossFrom"],
                                                                 dbl_gross_to = rst_bonus_details["dblGrossTo"],
                                                                 fk_dept= ins_dept if ins_dept else None,
                                                                 fk_desig = ins_desig if ins_desig else None,
                                                                 fk_religion = ins_religion if ins_religion else None,
                                                                 # int_month = int_month,
                                                                 # int_year = int_year,
                                                                 dbl_bonus_percent = rst_bonus_details["dblBonusPercent"],
                                                                 fk_created_id = request.user.id,
                                                                 dat_created = datetime.now(),
                                                                 int_status = 1,
                                                                 int_bonus_over_type = int(rst_bonus_details.get('intBonusOver')),
                                                                 int_consider_months = int(rst_bonus_details.get('intMonthsConsider')),
                                                                 int_eligibility_months = int(rst_bonus_details.get('intEligibilityMonths')),
                                                                 vchr_bonus_name = rst_bonus_details.get('strName'),
                                                                 json_employee = request.data.get("lstSelectedEmpId")
                                                                )
                ins_bonus_details.save()
            else:
                ins_bonus_details = BonusDetails.objects.create( dbl_gross_from = rst_bonus_details["dblGrossFrom"],
                                                                 dbl_gross_to = rst_bonus_details["dblGrossTo"],
                                                                 fk_dept= ins_dept if ins_dept else None,
                                                                 fk_desig = ins_desig if ins_desig else None,
                                                                 fk_religion = ins_religion if ins_religion else None,
                                                                 # int_month = int_month,
                                                                 # int_year = int_year,
                                                                 dbl_bonus_percent = rst_bonus_details["dblBonusPercent"],
                                                                 fk_created_id = request.user.id,
                                                                 dat_created = datetime.now(),
                                                                 int_status = 1,
                                                                 int_bonus_over_type = int(rst_bonus_details.get('intBonusOver')),
                                                                 int_consider_months = int(rst_bonus_details.get('intMonthsConsider')),
                                                                 int_eligibility_months = int(rst_bonus_details.get('intEligibilityMonths')),
                                                                 vchr_bonus_name = rst_bonus_details.get('strName'),
                                                                 json_employee = request.data.get("lstSelectedEmpId")
                                                                )
                ins_bonus_details.save()
            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})

    def put(self,request):
        try:
            id = request.data.get("pk_bint_id")
            lst_user_data=[]
            if id :
                bonus_list = BonusDetails.objects.filter(pk_bint_id = id).values(
                                                                                "pk_bint_id",
                                                                                "dbl_gross_from",
                                                                                "dbl_gross_to",
                                                                                "fk_dept__vchr_name",
                                                                                "fk_desig__vchr_name",
                                                                                "fk_religion__vchr_name",
                                                                                "fk_dept_id",
                                                                                "fk_desig_id",
                                                                                "fk_religion_id",
                                                                                # "int_month",
                                                                                "int_year",
                                                                                "dbl_bonus_percent",
                                                                                'int_bonus_over_type',
                                                                               'int_consider_months',
                                                                               'int_eligibility_months',
                                                                               'vchr_bonus_name',
                                                                               'json_employee'
                                                                                ).first()

                if bonus_list['json_employee']:
                    lst_user = UserDetails.objects.filter(user_ptr_id__in=bonus_list['json_employee']).annotate(fullname=Concat('first_name', Value(' '),'vchr_middle_name', Value(' ') ,'last_name')).values('vchr_employee_code','fullname','user_ptr_id')
                    for dct_user in lst_user:
                        dct_data={}
                        dct_data['intId'] = dct_user['user_ptr_id']
                        dct_data['strEMPCode'] = dct_user['vchr_employee_code']
                        dct_data['strUserCode'] = dct_user['vchr_employee_code']
                        dct_data['strUserName'] = dct_user['fullname']
                        lst_user_data.append(dct_data)


            else :
                bonus_list = BonusDetails.objects.filter(int_status = 1).values(
                                                                                "pk_bint_id",
                                                                                "dbl_gross_from",
                                                                                "dbl_gross_to",
                                                                                "fk_dept__vchr_name",
                                                                                "fk_desig__vchr_name",
                                                                                "fk_religion__vchr_name",
                                                                                # "int_month",
                                                                                "int_year",
                                                                                "dbl_bonus_percent",
                                                                                'int_bonus_over_type',
                                                                               'int_consider_months',
                                                                               'int_eligibility_months',
                                                                               'vchr_bonus_name',
                                                                               'json_employee'
                                                                            )
                for dct_data in bonus_list:
                    dct_data['dbl_gross'] = str(dct_data['dbl_gross_from'])+' - '+str(dct_data['dbl_gross_to'])
                    str_bonus_over=''
                    if dct_data['int_bonus_over_type']==1:
                        str_bonus_over='Gross Pay'
                    elif dct_data['int_bonus_over_type']==2:
                        str_bonus_over='Basic Pay+DA'
                    elif dct_data['int_bonus_over_type']==3:
                        str_bonus_over='CTC'
                    dct_data['dbl_percent'] = str(dct_data['dbl_bonus_percent']) +'% of '+str_bonus_over
            return Response({"status":1,"bonus_list":bonus_list,'lst_user_data':lst_user_data})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})


class DeleteBonusDetails(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            id = request.data.get("pk_bint_id")
            rst_bonus_paid = BonusPaid.objects.filter(fk_bonus_id = id).values()
            if rst_bonus_paid:
                return Response({"status":0,'reason':'Can not delete this Bonus'})
            BonusDetails.objects.filter(pk_bint_id = id).update(int_status = -1)
            return Response({"status":1})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})


class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            conn = engine.connect()
            int_bonus_id = request.data.get('intBonusId',5)
            dct_bonus = BonusDetails.objects.filter(pk_bint_id = int_bonus_id).values("pk_bint_id","dbl_gross_from","dbl_gross_to","fk_dept__vchr_name","fk_desig__vchr_name","fk_religion__vchr_name","fk_dept_id","fk_desig_id","fk_religion_id", "int_year","dbl_bonus_percent",'int_bonus_over_type','int_consider_months','int_eligibility_months','vchr_bonus_name','json_employee').first()
            dct_data={}
            json_employee=dct_bonus['json_employee']
            if not json_employee:
                str_query = "SELECT ud.user_ptr_id FROM  auth_user au JOIN user_details ud ON ud.user_ptr_id = au.id LEFT JOIN department dept ON dept.pk_bint_id = ud.fk_department_id LEFT JOIN job_position desig ON desig.pk_bint_id = ud.fk_desig_id LEFT JOIN religion_caste re ON re.pk_bint_id = ud.fk_religion_id WHERE au.is_active = TRUE {0}"
                str_filter=''
                if dct_bonus['fk_dept_id']:
                    str_filter += ' AND dept.pk_bint_id = '+str(dct_bonus['fk_dept_id'])
                if dct_bonus['fk_desig_id']:
                    str_filter += ' AND desig.pk_bint_id = '+str(dct_bonus['fk_desig_id'])
                if dct_bonus['fk_religion_id']:
                    str_filter += ' AND re.pk_bint_id = '+str(dct_bonus['fk_religion_id'])
                str_query = str_query.format(str_filter)
                rst_data = conn.execute(str_query).fetchall()
                json_employee=[]
                for dct_item in rst_data:
                    json_employee.append(dct_item[0])
            lst_data=[]
            dct_bonus_paid = BonusPaid.objects.filter(fk_bonus_id = dct_bonus['pk_bint_id']).values('json_paid')
            lst_paid_emp=[]
            if dct_bonus_paid:
                for dct_paid in dct_bonus_paid[0]['json_paid']:
                    lst_paid_emp += dct_paid.keys()
            today = datetime.today()
            dat_eligible = today - relativedelta(months=dct_bonus['int_eligibility_months'])
            lst_user = SalaryDetails.objects.filter(int_status=1,fk_employee__user_ptr_id__in=json_employee,fk_employee__dbl_gross__gte=dct_bonus['dbl_gross_from'],fk_employee__dbl_gross__lte=dct_bonus['dbl_gross_to'],fk_employee_id__dat_doj__lte=dat_eligible).exclude(fk_employee__user_ptr_id__in=lst_paid_emp).annotate(fullname=Concat('fk_employee__first_name', Value(' '),'fk_employee__vchr_middle_name', Value(' ') ,'fk_employee__last_name')).values('fk_employee__dbl_gross',
                                                            'fk_employee__vchr_employee_code','fullname','fk_employee__user_ptr_id','fk_employee__int_act_status',
                                                            'fk_employee__fk_branch__vchr_name','fk_employee__fk_desig__vchr_name','dbl_bp','json_allowance')

            for dct_user in lst_user:
                dct_data={}
                dct_data['intEmpId']=dct_user['fk_employee__user_ptr_id']
                dct_data['strEmpCode']=dct_user['fk_employee__vchr_employee_code']
                dct_data['strEmpName']=dct_user['fullname']
                dct_data['strBranch']=dct_user['fk_employee__fk_branch__vchr_name']
                dct_data['fltAmount']=0
                dct_data['strDesig'] =dct_user['fk_employee__fk_desig__vchr_name']
                dct_data['intStatus'] =dct_user['fk_employee__int_act_status']
                if dct_bonus['int_bonus_over_type']==1:
                    dct_data['fltAmount']=round((dct_user['fk_employee__dbl_gross']*dct_bonus['dbl_bonus_percent'])/100,0)
                elif dct_bonus['int_bonus_over_type']==2:
                    dct_data['fltAmount']=round((dct_user['dbl_bp']*dct_bonus['dbl_bonus_percent'])/100,0)
                elif dct_bonus['int_bonus_over_type']==3:
                    dbl_tot_allowances = dct_user['json_allowance'].get('PF',0)+dct_user['json_allowance'].get('ESI',0)+dct_user['json_allowance'].get('WWF',0)+dct_user['json_allowance'].get('Gratuity',0)
                    dbl_monthly_ctc = round(dct_user['fk_employee__dbl_gross']+dbl_tot_allowances, 0)
                    dct_data['fltAmount']=round((dbl_monthly_ctc*dct_bonus['dbl_bonus_percent'])/100,0)


                lst_data.append(dct_data)


            conn.close()
            return Response({"status":1,'data':lst_data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})
    def put(self,request):
        try:
            if request.data.get('lstHoldEmp'):
                BonusDetails.objects.filter(pk_bint_id = request.data.get('intBonusId')).update(json_hold=request.data.get('lstHoldEmp'))
            ins_bonus_paid = BonusPaid.objects.create( fk_bonus_id = request.data.get('intBonusId'),
                                                        json_paid= request.data.get('lstReleasedEmp'),
                                                        dat_paid=request.data.get('datRelease'),fk_created_id = request.user.id,
                                                        dat_created = datetime.now())
            ins_bonus_paid.save()
            return Response({"status":1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})


class BonusPaidList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try :

            dat_start = datetime.strptime(request.data.get('date_From'),'%d-%m-%Y')
            dat_end = datetime.strptime(request.data.get('date_To'),'%d-%m-%Y')
            ins_bonus_paid = BonusPaid.objects.filter(dat_paid__gte = dat_start, dat_paid__lte = dat_end).values("json_paid","fk_bonus_id__vchr_bonus_name")
            lst_emp_bonus = []
            if ins_bonus_paid:
                for dct_bonus_paid in ins_bonus_paid :
                    for dct_json_paid in dct_bonus_paid['json_paid']:
                        tpl_data = list(dct_json_paid.items())[0]
                        ins_emp = UserDetails.objects.filter(user_ptr_id = int(tpl_data[0]))

                        if request.data.get("intDepartmentId"):
                            ins_emp = ins_emp.filter(fk_department_id = request.data.get("intDepartmentId"))
                        if request.data.get("intBranchId"):
                            ins_emp = ins_emp.filter(fk_branch_id = request.data.get("intBranchId"))
                        if request.data.get("intDesignationId"):
                            ins_emp = ins_emp.filter(fk_desig_id = request.data.get("intDesignationId"))

                        if ins_emp:
                            ins_emp = ins_emp.annotate(strFullName=Concat('first_name', Value(' '), Case(When(vchr_middle_name = None, then=F('last_name')), default=Concat('vchr_middle_name', Value(' '), 'last_name'), output_field = CharField()), output_field = CharField())).values("vchr_employee_code","strFullName","fk_branch_id","fk_desig_id","fk_department_id","fk_branch_id__vchr_name","fk_department_id__vchr_name","fk_desig_id__vchr_name","vchr_acc_no")[0]
                            ins_emp["intAmount"] = tpl_data[1]
                            ins_emp["strBonusName"] = dct_bonus_paid["fk_bonus_id__vchr_bonus_name"]
                            lst_emp_bonus.append(ins_emp)
                return Response({"status":1,"data":lst_emp_bonus})
            else:
                return Response({"status":0})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':e})
