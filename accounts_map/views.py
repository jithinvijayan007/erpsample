from rest_framework import generics
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from sap_api.models import ChartOfAccounts
from accounts_map.models import AccountsMap
import sys, os
from POS import ins_logger
from django.db.models import Q

from day_closure.models import DayClosureMaster

from tool_settings.models import Tools
import json

class ChartOfAccountsTypehead(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            str_search_term = request.data.get('term',-1)
            lst_coa = []
            if str_search_term != -1:
                ins_coa = ChartOfAccounts.objects.filter(Q(vchr_acc_code__icontains=str_search_term) | Q(vchr_acc_name__icontains=str_search_term)).values('vchr_acc_code','vchr_acc_name','vchr_acc_type','pk_bint_id')
                if ins_coa:
                    for itr_item in ins_coa:
                        dct_coa = {}
                        dct_coa['code'] = itr_item['vchr_acc_code']
                        dct_coa['name'] = itr_item['vchr_acc_name']
                        dct_coa['id'] = itr_item['pk_bint_id']

                        lst_coa.append(dct_coa)
                return Response({'status':1,'data':lst_coa})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})
class CategoryTypehead(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request): 
        try:
            str_search_term = request.data.get('term',-1)
            lst_category=['invoice','advance payment','expense','contra','refund','satff','incentive','prebooking','others']
            if str_search_term != -1:
                lst_give=[{"name":data}  for data in lst_category if str_search_term.lower() in data ]
                return Response({'status':1,'data':lst_give})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})

class AccountsMapView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            ins_account_map=AccountsMap(vchr_module_name=request.data.get('vchr_module_name'),
                                        vchr_category=request.data.get('vchr_category'),
                                        fk_coa_id=request.data.get('int_chart_of_acc'),
                                        int_status=0,
                                        int_type=request.data.get('int_type'),
                                        fk_branch_id=request.data.get('int_branch_id'))
            ins_account_map.save()
            return Response({'status':1})

        except Exception as e:
            exc_type,exc_obj,exc_tb=sys.exc_info()
            ins_logger.logger.error(e,extra={'user':'user_id:'+str(request.user.id),'details':'line no:'+str(exc_tb.tb_lineno)})
            return Response ({'result':0,'reason':e})
    def put(self,request):
        try:
            lst_account_map=list(AccountsMap.objects.filter(pk_bint_id=request.data.get('intAccountId')).values('pk_bint_id','vchr_module_name','vchr_category','fk_coa__vchr_acc_name','fk_coa__pk_bint_id','fk_coa__vchr_acc_code','int_status','int_type','fk_branch__vchr_name','fk_branch__pk_bint_id'))
            if request.data.get('blnEdit'):
                ins_account_map=AccountsMap.objects.filter(pk_bint_id=request.data.get('intAccountId')).update(int_status=-1)
                ins_account_map=AccountsMap()
                ins_account_map.vchr_module_name=request.data.get('vchr_module_name')
                ins_account_map.vchr_category=request.data.get('vchr_category')
                ins_account_map.fk_coa_id=request.data.get('int_chart_of_acc')
                ins_account_map.int_status=1
                ins_account_map.int_type=request.data.get('int_type')
                ins_account_map.fk_branch_id=request.data.get('int_branch_id')
                ins_account_map.save()
                return Response({'status':1})

            if request.data.get('blnDelete'):

                ins_account_map=AccountsMap.objects.filter(pk_bint_id=request.data.get('intAccountId')).update(int_status=-1)
                return Response({'status':1})

            return Response({'status':1,'lst_account_map':lst_account_map})

        except Exception as e:
            exc_type,exc_obj,exc_tb=sys.exc_info()
            ins_logger.logger.error(e,extra={'user':'user_id:'+str(request.user.id),'details':'line no:'+str(exc_tb.tb_lineno)})
            return Response ({'result':0,'reason':e})
    def get(self,request):
        try:
            lst_account_map=list(AccountsMap.objects.filter(int_status__in=[0,1]).values('pk_bint_id','vchr_module_name','vchr_category','fk_coa__vchr_acc_name','fk_coa__vchr_acc_code','int_status','int_type','fk_branch__vchr_name'))
            return Response({'status':1,'lst_account_map':lst_account_map})
        except Exception as e:
            exc_type,exc_obj,exc_tb=sys.exc_info()
            ins_logger.logger.error(e,extra={'user':'user_id:'+str(request.user.id),'details':'line no:'+str(exc_tb.tb_lineno)})
            return Response ({'result':0,'reason':e})



class AdditionsTypeahead(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):

            try:

                str_search_term = request.data.get('term',-1)
                lst_category = []
                if str_search_term != -1:
                    ins_category =AccountsMap.objects.filter(Q(vchr_module_name__icontains='addition') | Q(vchr_module_name__icontains='deduction'),vchr_category__icontains=str_search_term).values('vchr_category','vchr_module_name')
                    if ins_category:
                        for itr_item in ins_category:
                            dct_category={}
                            dct_category['name'] = itr_item['vchr_category']
                            dct_category['tool_name'] = itr_item['vchr_module_name']
                            lst_category.append(dct_category)
                    return Response({'status':1,'data':lst_category})

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                return Response({'result':0,'reason':e})
# #
class AddAdditionstoTools(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
            try:

                ins_tools=Tools.objects.filter(vchr_tool_name__icontains='addition').first()
                if not ins_tools:
                    ins_tools=Tools()
                    ins_tool.vchr_tool_name='ADDITIONS'
                    ins_tool.vchr_tool_code='ADDITIONS'

                lst_branch=request.data.get('lst_branch')
                lst_additions=request.data.get('lst_additions')

                json_data={}

                for addition in lst_additions:

                    json_data[addition]=lst_branch

                json_data=json.dumps(json_data)
                if  ins_tools.json_data:
                    ins_tools.json_data=ins_tools.json_data.extend(json_data)
                ins_tools.int_status=0
                ins_tools.save()
                return Reponse({'status':1})
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                return Response({'result':0,'reason':e})
# #
