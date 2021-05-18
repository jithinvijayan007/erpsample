from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from branch.models import Branch
from rest_framework.response import Response
from datetime import date
from django.db.models import Q
# from POS import ins_logger
from POS import ins_logger
import sys, os
from category.models import OtherCategory
import logging
from django.conf import settings
from error_logg import er_logger

# Create your views here.

class BranchApi(APIView):
    """
    to add and list and view branch details
    """
    permission_classes = [AllowAny]
    def get(self,request):
        """
        to get branch list and view details
        parameter:branchId(for view)
        return:branch lists/branch details
        """
        try:
            int_branch_id = request.GET.get('branchId',None)
            int_status = request.GET.get('activestatus',None)

            if not int_branch_id :
                rst_branch=Branch.objects.filter().values('pk_bint_id','vchr_code','vchr_mygcare_no','vchr_name','vchr_address','vchr_email','vchr_phone','fk_category_id','fk_category__vchr_name','int_status','fk_states_id','fk_states_id__vchr_name','flt_size','int_price_template','dbl_stock_request_amount','int_stock_request_qty').exclude(int_status = -1).order_by('-pk_bint_id')

                if int_status :
                    rst_branch =rst_branch.filter(int_status = int(int_status))

                lst_branch = []

                if rst_branch:
                    lst_branch = list(rst_branch)
                return Response({'status':1,'lst_branch':lst_branch})

            else:
                rst_branch=Branch.objects.filter(pk_bint_id=int_branch_id).values('pk_bint_id','vchr_mygcare_no','vchr_code','vchr_name','vchr_address','vchr_email','vchr_phone','bint_stock_limit','vchr_ip','flt_latitude','flt_longitude','dat_inauguration','tim_inauguration','vchr_inaugurated_by','fk_category_id','fk_category__vchr_name','int_type','int_status','fk_states_id','fk_states_id__vchr_name','flt_size','int_price_template','dbl_stock_request_amount','int_stock_request_qty').exclude(int_status = -1).first()

                return Response({'status':1,'lst_branch':rst_branch})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            # ins_logger.logger.error(e, extra={'details':traceback.format_exc(),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'message':str(e)})
    def post(self,request):
        """
        Add branch details
        parameter:branch code,branch name,address,email,phone
        response:return success status
        """
        try:
            vchr_code = request.data.get('strCode')
            vchr_name = request.data.get('strName')
            vchr_address = request.data.get('strAddress')
            vchr_email = request.data.get('strEmail')
            vchr_phone = request.data.get('intContact')
            int_myg_care_num = request.data.get('intMygCareNo')
            bint_stock_limit  = request.data.get('strStockLimit')
            vchr_ip = request.data.get('intStaticIp')
            flt_size = request.data.get('fltSize')
            flt_latitude = request.data.get('intLatitude')
            flt_longitude = request.data.get('intLongitude')
            dat_inauguration = request.data.get('datInagtnDate')
            tim_inauguration = request.data.get('intInagtnTime')
            vchr_inaugurated_by = request.data.get('strIngtnBy')
            fk_category = request.data.get('intCategory')
            int_type = int(request.data.get('intType'))
            int_price_template = request.data.get('intPriceTemplate')
            fk_states_id = request.data.get('stateId')
            int_stk_qty=request.data.get('intStockRqstQty')
            int_stk_amt=request.data.get('intStockRqstAmt')
            int_pin_code=request.data.get('intPincode')
            fk_hierarchy = request.data.get('intHierarchy')
            # print(fk_hierarchy)

            if Branch.objects.filter(Q(vchr_code=vchr_code) | Q(vchr_name = vchr_name)).exists():
                return Response({'status':'0','message':'Branch Aleady exists'})

            Branch.objects.create(vchr_code=vchr_code,
                                  vchr_name= vchr_name,
                                  vchr_address = vchr_address,
                                  vchr_email = vchr_email,
                                  vchr_phone = vchr_phone,
                                  vchr_mygcare_no = str(int_myg_care_num) if int_myg_care_num else "" ,
                                  bint_stock_limit  = bint_stock_limit,
                                  vchr_ip = vchr_ip,
                                  flt_size = flt_size,
                                  flt_latitude = flt_latitude,
                                  flt_longitude = flt_longitude,
                                  dat_inauguration = dat_inauguration,
                                  tim_inauguration = tim_inauguration,
                                  vchr_inaugurated_by = vchr_inaugurated_by,
                                  fk_category_id = fk_category,
                                  int_type = int_type,
                                  int_status = 0,
                                  fk_states_id = fk_states_id,
                                  int_price_template = int_price_template,
                                  dbl_stock_request_amount=int_stk_amt,
                                  int_stock_request_qty=int_stk_qty,
                                  int_pincode=int_pin_code,
                                  fk_hierarchy_data_id = fk_hierarchy
                                )
            return Response({'status':'1'})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
             # ins_logger.logger.error(e, extra={'details':traceback.format_exc(),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'0','message':str(e)})

    def put(self,request):
        """
        to update branch details
        prameter:branch id,and other branch details
        response:return success message
        """
        try:
            #import pdb; pdb.set_trace()
            vchr_code = request.data.get('strCode')
            vchr_name = request.data.get('strName')
            vchr_address = request.data.get('strAddress')
            vchr_email = request.data.get('strEmail')
            vchr_phone = request.data.get('intContact')
            int_myg_care_num = request.data.get('intMygCareNo')
            bint_stock_limit  = request.data.get('strStockLimit')
            vchr_ip = request.data.get('intStaticIp')
            flt_size = request.data.get('fltSize')
            flt_latitude = request.data.get('intLatitude')
            flt_longitude = request.data.get('intLongitude')
            dat_inauguration = request.data.get('datInagtnDate')
            tim_inauguration = request.data.get('intInagtnTime')
            vchr_inaugurated_by = request.data.get('strIngtnBy')
            fk_category = request.data.get('intCategory')
            int_type = int(request.data.get('intType'))
            int_branch_id = request.data.get('branchId')
            int_status = request.data.get('int_status',None)
            fk_states_id = request.data.get('stateId')
            int_price_template = request.data.get('intPriceTemplate')
            int_stk_qty=request.data.get('intStockRqstQty')
            int_stk_amt=request.data.get('intStockRqstAmt')
            if Branch.objects.filter(Q(vchr_code=vchr_code) | Q(vchr_name=vchr_name)).exclude(pk_bint_id=int_branch_id).exists():
                return Response({'status':'duplicate','message':'Branch already exists'})

            if int_status != None:
                ins_branch = Branch.objects.filter(pk_bint_id=int_branch_id).update(
                    vchr_code=vchr_code,
                    vchr_name= vchr_name,
                    vchr_address = vchr_address,
                    vchr_email = vchr_email,
                    vchr_phone = vchr_phone,
                    vchr_mygcare_no = str(int_myg_care_num) if int_myg_care_num else "" ,
                    bint_stock_limit  = bint_stock_limit,
                    vchr_ip = vchr_ip,
                    flt_size = flt_size,
                    flt_latitude = flt_latitude,
                    flt_longitude = flt_longitude,
                    dat_inauguration = dat_inauguration,
                    tim_inauguration = tim_inauguration,
                    vchr_inaugurated_by = vchr_inaugurated_by,
                    fk_category_id = fk_category,
                    int_type = int_type,
                    int_status = int(int_status),
                    dat_close=date.today(),
                    fk_states_id = fk_states_id,
                    int_price_template =int_price_template,
                    dbl_stock_request_amount=int_stk_amt,
                    int_stock_request_qty=int_stk_qty
                )

            else:
                ins_branch = Branch.objects.filter(pk_bint_id=int_branch_id).update(
                    vchr_code=vchr_code,
                    vchr_name= vchr_name,
                    vchr_address = vchr_address,
                    vchr_email = vchr_email,
                    vchr_phone = vchr_phone,
                    vchr_mygcare_no = str(int_myg_care_num) if int_myg_care_num else "" ,
                    bint_stock_limit  = bint_stock_limit,
                    vchr_ip = vchr_ip,
                    flt_size = flt_size,
                    flt_latitude = flt_latitude,
                    flt_longitude = flt_longitude,
                    dat_inauguration = dat_inauguration,
                    tim_inauguration = tim_inauguration,
                    vchr_inaugurated_by = vchr_inaugurated_by,
                    fk_category_id = fk_category,
                    int_type = int_type,
                    fk_states_id = fk_states_id,
                    int_price_template =int_price_template,
                    dbl_stock_request_amount=int_stk_amt,
                    int_stock_request_qty=int_stk_qty
                )
            return Response({'status':'1'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
             #ins_logger.logger.error(e, extra={'details':traceback.format_exc(),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'0','message':str(e)})

    def patch(self,request):
        try:
            # delete
            # import pdb;pdb.set_trace()
            int_branch_id = request.data.get('intId')
            if not Branch.objects.filter(pk_bint_id=int_branch_id).exists():
                return Response({'status':'0','message':'Branch not found'})
            Branch.objects.filter(pk_bint_id=int_branch_id).update(int_status = -1,dat_close=date.today())
            return Response({'status':'1'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
             #ins_logger.logger.error(e, extra={'details':traceback.format_exc(),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'0','message':str(e)})



class BranchTypeHead(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            str_search_term = request.data.get('term',-1)
            lst_branchs = []
            if str_search_term != -1:
                ins_brand = Branch.objects.filter((Q(vchr_name__icontains=str_search_term) | Q(vchr_code__icontains=str_search_term))&Q(int_status=0)).values('pk_bint_id','vchr_name','vchr_code')
                if ins_brand:
                    for itr_item in ins_brand:
                        dct_brands = {}
                        dct_brands['name'] = itr_item['vchr_name']
                        dct_brands['id'] = itr_item['pk_bint_id']
                        lst_branchs.append(dct_brands)
                return Response({'status':1,'data':lst_branchs})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})

            return Response({'result':0,'reason':str(e)})



class BranchCategoryList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            # import pdb; pdb.set_trace()
            lst_category =[]
            ins_category = OtherCategory.objects.filter(int_status = 3).values('pk_bint_id','vchr_name')
            if ins_category:
                for itr_item in ins_category:
                    dct_category = {}
                    dct_category['vchr_category'] = itr_item['vchr_name']
                    dct_category['id'] = itr_item['pk_bint_id']
                    lst_category.append(dct_category)
            return Response({'status':1,'data':lst_category})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            # details = ('user : user_id:' + str(request.user.id),'details : line no: ' + str(exc_tb.tb_lineno))
            # em = er_logger(str(e),details)
            return Response({'result':0,'reason':str(e)})
