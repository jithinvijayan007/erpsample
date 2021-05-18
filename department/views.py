from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from department.models import Department
from django.db.models import Q
from POS import ins_logger
import traceback
from hierarchy.models import Hierarchy
import sys, os

class AddDepartment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            """Add department"""
            ins_dup_department = Department.objects.filter((Q(vchr_code = request.data.get("strDepartmentCode")) | Q(vchr_name = request.data.get("strDepartment"))),int_status = 1)
            if ins_dup_department:
                return Response({'status':0,'message':'Department Already Exists'})

            ins_department = Department.objects.create(vchr_code = request.data.get("strDepartmentCode"),
                                                  vchr_name = request.data.get("strDepartment"),
                                                  int_status = 1,
                                                  fk_company_id = request.data.get("intCompanyId"))

            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def put(self,request):
        try:
            """Update Department"""

            int_department_id = request.data.get("intDepartmentId")
            str_code = request.data.get("strDepartmentCode")
            str_name = request.data.get("strDepartment")

            ins_dup_department = Department.objects.filter((Q(vchr_code = str_code) | Q(vchr_name = str_name)),int_status = 1).exclude(pk_bint_id = int_department_id)

            if ins_dup_department:
                return Response({'status':0,'message':'Department Already Exists'})

            ins_department = Department.objects.filter(pk_bint_id = int_department_id).update(vchr_code = request.data.get("strDepartmentCode"),
                                                                                      vchr_name = request.data.get("strDepartment"))
            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

    def patch(self,request):
        try:
            """Delete Department"""

            int_department_id = request.data.get("intDepartmentId")
            Department.objects.filter(pk_bint_id = int_department_id).update(int_status = -1)
            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})

class DepartmentList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            # import pdb; pdb.set_trace()
            """List Department"""
            # import pdb; pdb.set_trace()
            # int_company_id = request.user.userdetails.fk_company_id
            lst_department = list(Department.objects.filter(int_status = 1).values('pk_bint_id','vchr_code','vchr_name','fk_company_id').order_by('vchr_name'))
            lst_filter = Hierarchy.objects.all().values('vchr_name','pk_bint_id','int_level')
            return Response({'status':1,'lst_department':lst_department,'filter':lst_filter})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'reason':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})
