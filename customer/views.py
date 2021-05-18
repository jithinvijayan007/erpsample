from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from POS import ins_logger
from customer.models import CustomerDetails,SalesCustomerDetails
from django.db.models import Q
from POS import ins_logger
import sys, os
# Create your views here.
from datetime import datetime,timedelta
from invoice.models import PartialInvoice

from states.models import Location,States
from POS import settings
import requests
from random import randint
import requests
from django.db.models.functions import Concat,Coalesce

from receipt.models import ReceiptInvoiceMatching,Receipt
from invoice.models import Bank
from sales_return.models import SalesReturn
from invoice.models import SalesMaster,SalesDetails
from django.db.models import CharField, Case, Value, When,Sum,F,IntegerField,Count
from customer.models import CustomerDetails,SalesCustomerDetails, CustomerOccasionsModel, CustomerRating
from payment.models import Payment
from item_category.models import Item
from branch.models import Branch
from operator import itemgetter
from django.db import transaction

from .models import CustomerRating
import math 
from django.db.models import Avg

from django.http import JsonResponse

# ===========================================
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import and_,func ,cast,DATE,case,distinct,Date
def Session():
    from aldjemy.core import get_engine
    engine=get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()

SalesReturnSA = SalesReturn.sa
SalesDetailsSA = SalesDetails.sa
SalesMasterSA = SalesMaster.sa
ReceiptInvoiceMatchingSA = ReceiptInvoiceMatching.sa
CustomerDetailsSA = CustomerDetails.sa
SalesCustomerDetailsSA = SalesCustomerDetails.sa
PaymentSA = Payment.sa
ReceiptSA = Receipt.sa
BankSA = Bank.sa
BranchSA = Branch.sa
ItemSA = Item.sa
# ===========================================


class EditCustomer(APIView):
    """docstring for ."""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            
            int_cust_id = request.data.get('cust_id')
            vchr_email = request.data.get('str_email',None)
            str_address = request.data.get('txt_address',None)
            str_gst_no = request.data.get('gst_no',None)
            int_location_id = request.data.get('location_id',None)
            int_state_id = request.data.get('state_id',None)
            int_mobile_num = request.data.get('mob_no',None)
            str_first_name = request.data.get('first_name',None)
            str_last_name = request.data.get('last_name',None)
            int_old_mobile_num = request.data.get('old_mobno',None)
            str_full_name = str_first_name

            ins_customer_duplicate = list(CustomerDetails.objects.filter(int_mobile = int_mobile_num).values('pk_bint_id').exclude(pk_bint_id = int_cust_id))

            if ins_customer_duplicate:
                return Response({'status':'0','message':'Customer already exist'})

            if request.data.get('cust_id'):
                CustomerDetails.objects.filter(pk_bint_id = int_cust_id).update(vchr_name = str_full_name,
                                                                vchr_email = vchr_email,
                                                                txt_address = str_address,
                                                                vchr_gst_no = str_gst_no,
                                                                fk_location_id = int_location_id,
                                                                fk_state_id = int_state_id,
                                                                int_mobile = int_mobile_num)
                ins_customer=CustomerDetails.objects.get(pk_bint_id = int_cust_id)
                ins_sales_customer = SalesCustomerDetails.objects.create(
                                                     fk_customer_id = ins_customer.pk_bint_id,
                                                     dat_created = datetime.now(),
                                                     fk_created_id = request.user.id,
                                                     vchr_name = ins_customer.vchr_name,
                                                     vchr_email = ins_customer.vchr_email,
                                                     int_mobile = ins_customer.int_mobile,
                                                     fk_state_id = ins_customer.fk_state_id,
                                                     int_loyalty_points = ins_customer.int_loyalty_points,
                                                     int_redeem_point = ins_customer.int_redeem_point,
                                                     dbl_purchase_amount = ins_customer.dbl_purchase_amount,
                                                     vchr_loyalty_card_number = ins_customer.vchr_loyalty_card_number,
                                                     txt_address = ins_customer.txt_address,
                                                     vchr_gst_no = ins_customer.vchr_gst_no,
                                                     int_otp_number = ins_customer.int_otp_number,
                                                     fk_location_id = ins_customer.fk_location_id,
                                                     fk_loyalty_id = ins_customer.fk_loyalty_id,
                                                     vchr_code = ins_customer.vchr_code,
                                                     int_cust_type = ins_customer.int_cust_type
                                                    )



            else:
                return Response({'status':'0','message':'No Data'})
            # ins_customer = CustomerDetails.objects.filter(pk_bint_id=request.data.get('intCustId')).values('pk_bint_id','vchr_name','vchr_email','int_mobile','txt_address','vchr_gst_no','fk_location_id','fk_state_id','fk_location__vchr_name','fk_state__vchr_name').first()
            dct_data = {}
            dct_data['strLocation']=''
            dct_data['strState']=''
            dct_data['intCustId'] = ins_customer.pk_bint_id
            dct_data['intSalesCustId'] = ins_sales_customer.pk_bint_id
            dct_data['strCustName'] = ins_customer.vchr_name
            dct_data['intCustType'] = ins_customer.int_cust_type
            dct_data['strCustEmail'] = ins_customer.vchr_email
            dct_data['intContactNo'] = ins_customer.int_mobile
            dct_data['txtAddress'] = ins_customer.txt_address
            dct_data['strGSTNo'] = ins_customer.vchr_gst_no
            dct_data['intLocation'] = ins_customer.fk_location_id
            if dct_data['intLocation']:
                dct_data['strLocation'] = ins_customer.fk_location.vchr_name
            dct_data['intState'] = ins_customer.fk_state_id
            if dct_data['intState']:
                dct_data['strState'] = ins_customer.fk_state.vchr_name

            # dct_pos = {}
            # print("location ",dct_data['intLocation'])
            # if dct_data['intLocation']:
            #     dct_pos=dict(Location.objects.filter(pk_bint_id=dct_data['intLocation']).values('fk_state__vchr_name','fk_state__vchr_code','vchr_district','vchr_pin_code','vchr_name').first())
            # url =settings.BI_HOSTNAME + "/customer/customer_update/"
            # dct_pos.update(dct_data)
            # dct_pos['user_name'] = request.user.username

            # res_data = requests.post(url,json=dct_pos)
            # if res_data.json().get('status')=='1':
            #     pass
            # else:
            #     raise ValueError('Something happened in BI')

            # if request.user.userdetails.fk_branch.fk_states_id != ins_customer['fk_state_id']:
            #     bln_igst = True
            # dct_data['blnIGST'] = bln_igst


            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})


class CustomerTypeHead(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            str_search_term = request.data.get('term',-1)
            lst_customer = []
            if str_search_term != -1:
                ins_customer = CustomerDetails.objects.filter(Q(vchr_name__icontains=str_search_term) | Q(int_mobile__icontains=str_search_term)).values('pk_bint_id','vchr_name','int_mobile','int_cust_type')
                if ins_customer:
                    for itr_item in ins_customer:
                        if itr_item['int_cust_type'] == 1:
                            vchr_customer_type = 'Co'
                        elif itr_item['int_cust_type'] == 2:
                            vchr_customer_type = 'Cr'
                        elif itr_item['int_cust_type'] == 3:
                            vchr_customer_type = 'Sz'
                        else:
                            vchr_customer_type = 'Ca'
                        dct_customer = {}
                        dct_customer['name'] = vchr_customer_type + ' - ' + itr_item['vchr_name'] + ' - ' + str(itr_item['int_mobile'])
                        dct_customer['id'] = itr_item['pk_bint_id']
                        dct_customer['phone'] = itr_item['int_mobile']
                        lst_customer.append(dct_customer)
                return Response({'status':1,'data':lst_customer})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})

class CustomerView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            #import pdb; pdb.set_trace()
            int_customer_id  = request.data.get('customerId')
            # int_customer_id  = 2
            ins_cutomer = CustomerDetails.objects.filter(pk_bint_id = int_customer_id).values('vchr_name','vchr_email','int_mobile','txt_address',
                                                                                            'vchr_gst_no','fk_location__vchr_name',
                                                                                            'fk_location__vchr_district',
                                                                                            'fk_state__vchr_name','fk_loyalty__vchr_card_name',
                                                                                            'fk_location_id','vchr_loyalty_card_number','fk_state_id','pk_bint_id')

            dct_customer = {}
            dct_customer['first_name'] =  ins_cutomer[0]['vchr_name']
            #dct_customer['last_name'] = lst_full_name[1]
            dct_customer['mob_no'] = ins_cutomer[0]['int_mobile']
            dct_customer['str_email'] = ins_cutomer[0]['vchr_email']
            dct_customer['txt_address'] = ins_cutomer[0]['txt_address']
            dct_customer['gst_no'] = ins_cutomer[0]['vchr_gst_no']
            dct_customer['location'] = ins_cutomer[0]['fk_location__vchr_name']
            dct_customer['location_id'] = ins_cutomer[0]['fk_location_id']
            dct_customer['state'] = ins_cutomer[0]['fk_state__vchr_name']
            dct_customer['state_id'] = ins_cutomer[0]['fk_state_id']
            dct_customer['loyalty_card_name'] = ins_cutomer[0]['fk_loyalty__vchr_card_name']
            dct_customer['loyalty_card_number'] = ins_cutomer[0]['vchr_loyalty_card_number']
            dct_customer['cust_id'] = ins_cutomer[0]['pk_bint_id']

            return Response({'status':1,'dct_customer':dct_customer})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})


class UpdateCustomer(APIView):
    """docstring for ."""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            # if request.data.get('intCustId'):
                # CustomerDetails.objects.filter(pk_bint_id=request.data.get('intCustId')).update(vchr_email = request.data.get('strEmail',None),
                #                                                 txt_address = request.data.get('strAddress',None),
                #                                                 vchr_gst_no = request.data.get('strGSTNo',None),
                #                                                 fk_location_id = request.data.get('intCityId',None),
                #                                                 fk_state_id = request.data.get('intStateId',None))
# ===========================================================================================================================================
            # if SalesCustomerDetails.objects.filter(pk_bint_id = 1):
            if CustomerDetails.objects.filter(pk_bint_id = request.data.get('intCustId')):
                    # int_customer_id = SalesCustomerDetails.objects.filter(pk_bint_id = 1).values('fk_customer_id').first()['fk_customer_id']
                    # int_customer_id = SalesCustomerDetails.objects.filter(pk_bint_id = request.data.get('intCustId')).values('fk_customer_id').first()['fk_customer_id']
                    # ins_customer = CustomerDetails.objects.get(pk_bint_id = int_customer_id)
                    #import pdb; pdb.set_trace()
                    ins_customer = CustomerDetails.objects.get(pk_bint_id = request.data.get('intCustId'))
                    # import pdb; pdb.set_trace()
                    int_edit_count=(ins_customer.int_edit_count or 0)
                    ins_customer.vchr_name = request.data.get('strName',None)
                    ins_customer.vchr_email = request.data.get('strEmail',None)
                    ins_customer.txt_address = request.data.get('strAddress',None)
                    ins_customer.vchr_gst_no = request.data.get('strGSTNo',None)
                    ins_customer.fk_location_id = request.data.get('intCityId',None)
                    ins_customer.fk_state_id = request.data.get('intStateId',None)
                    ins_customer.int_edit_count=int_edit_count+1
                    ins_customer.save()
                    ins_sales_customer = SalesCustomerDetails.objects.create(
                                                         fk_customer_id = ins_customer.pk_bint_id,
                                                         dat_created = datetime.now(),
                                                         fk_created_id = request.user.id,
                                                         vchr_name = ins_customer.vchr_name,
                                                         vchr_email = ins_customer.vchr_email,
                                                         int_mobile = ins_customer.int_mobile,
                                                         fk_state_id = ins_customer.fk_state_id,
                                                         int_loyalty_points = ins_customer.int_loyalty_points,
                                                         int_redeem_point = ins_customer.int_redeem_point,
                                                         dbl_purchase_amount = ins_customer.dbl_purchase_amount,
                                                         vchr_loyalty_card_number = ins_customer.vchr_loyalty_card_number,
                                                         txt_address = ins_customer.txt_address,
                                                         vchr_gst_no = ins_customer.vchr_gst_no,
                                                         int_otp_number = ins_customer.int_otp_number,
                                                         fk_location_id = ins_customer.fk_location_id,
                                                         fk_loyalty_id = ins_customer.fk_loyalty_id,
                                                         vchr_code = ins_customer.vchr_code,
                                                         int_cust_type = ins_customer.int_cust_type
                                                        )
                    # sales_customer_details id update in partial_invoice table
                    if(request.data.get('intPartialId')):
                        ins_partial_inv = PartialInvoice.objects.get(pk_bint_id = request.data.get('intPartialId'))
                        dct_json = ins_partial_inv.json_data
                        dct_json['int_sales_cust_id'] = ins_sales_customer.pk_bint_id
                        ins_partial_inv.json_data = dct_json
                        ins_partial_inv.save()

                    dct_data = {}
                    dct_data['strLocation']=''
                    dct_data['strState']=''
                    dct_data['intCustId'] = ins_customer.pk_bint_id
                    dct_data['intSalesCustId'] = ins_sales_customer.pk_bint_id
                    dct_data['strCustName'] = ins_customer.vchr_name
                    dct_data['intCustType'] = ins_customer.int_cust_type
                    dct_data['strCustEmail'] = ins_customer.vchr_email
                    dct_data['intContactNo'] = ins_customer.int_mobile
                    dct_data['txtAddress'] = ins_customer.txt_address
                    dct_data['strGSTNo'] = ins_customer.vchr_gst_no
                    dct_data['intLocation'] = ins_customer.fk_location_id
                    if dct_data['intLocation']:
                        dct_data['strLocation'] = ins_customer.fk_location.vchr_name
                    dct_data['intState'] = ins_customer.fk_state_id
                    if dct_data['intState']:
                        dct_data['strState'] = ins_customer.fk_state.vchr_name

                    dct_pos = {}
                    print("location ",dct_data['intLocation'])
                    if dct_data['intLocation']:
                        dct_pos=dict(Location.objects.filter(pk_bint_id=dct_data['intLocation']).values('fk_state__vchr_name','fk_state__vchr_code','vchr_district','vchr_pin_code','vchr_name').first())
                    # url =settings.BI_HOSTNAME + "/customer/customer_update/"
                    #commened for o2force
                    dct_pos.update(dct_data)
                    dct_pos['user_name'] = request.user.username

                    # res_data = requests.post(url,json=dct_pos)
                    # if res_data.json().get('status')=='1':
                    #     pass
                    # else:
                    #     raise ValueError('Something happened in BI')

                    dct_data['blnIGST']=False

                    if request.user.userdetails.fk_branch.fk_states_id != ins_customer.fk_state_id:
                        dct_data['blnIGST'] = True

                    return Response({'status':1,'data':dct_data})
            else:
                return Response({'status':'0','message':'No Data'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})
    # ===========================================================================================================================================}

        #     else:
        #         return Response({'status':'0','message':'No Data'})
        #     ins_customer = CustomerDetails.objects.filter(pk_bint_id=request.data.get('intCustId')).values('pk_bint_id','vchr_name','vchr_email','int_mobile','txt_address','vchr_gst_no','fk_location_id','fk_state_id','fk_location__vchr_name','fk_state__vchr_name').first()
        #     dct_data = {}
        #     dct_data['intCustId'] = ins_customer['pk_bint_id']
        #     dct_data['strCustName'] = ins_customer['vchr_name']
        #     dct_data['strCustEmail'] = ins_customer['vchr_email']
        #     dct_data['intContactNo'] = ins_customer['int_mobile']
        #     dct_data['txtAddress'] = ins_customer['txt_address']
        #     dct_data['strGSTNo'] = ins_customer['vchr_gst_no']
        #     dct_data['intLocation'] = ins_customer['fk_location_id']
        #     dct_data['strLocation'] = ins_customer['fk_location__vchr_name']
        #     dct_data['intState'] = ins_customer['fk_state_id']
        #     dct_data['strState'] = ins_customer['fk_state__vchr_name']
        #     bln_igst = False
        #     if request.user.userdetails.fk_branch.fk_states_id != ins_customer['fk_state_id']:
        #         bln_igst = True
        #     dct_data['blnIGST'] = bln_igst
        #     return Response({'status':1,'data':dct_data})
        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
        #     return Response({'status':'0','message':str(e)})


class GenerateOtp(APIView):
    """OTP GENERATE"""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            str_otp=randint(1000, 9999)
            ins_customer=SalesCustomerDetails.objects.filter(pk_bint_id = request.data.get('int_sales_cust_id'))
            ins_cust_master=ins_customer[0].fk_customer
            ins_cust_master.vchr_otp=str_otp
            ins_cust_master.dat_exp=datetime.now()+timedelta(seconds=90)
            ins_cust_master.save()
            rsp_request=requests.get("https://app.smsbits.in/api/users?id=OTg0NjY2OTk1NQ&senderid=myGsms&to="+str(ins_customer[0].int_mobile)+"&msg=Dear Customer,Your OTP for change customer details is "+str(str_otp)+" .&port=TA")
            if rsp_request.status_code==200:
            # if True:
                return Response({'status':1})
            else:
                return Response({'status':0,'message':'No SMS API'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})


class UpdateCustomerInvoice(APIView):
    """docstring for ."""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            if SalesCustomerDetails.objects.filter(pk_bint_id = request.data.get('intCustId')):

                    ins_customer = SalesCustomerDetails.objects.get(pk_bint_id = request.data.get('intCustId'))
                    ins_customer.vchr_name = request.data.get('strName',None)
                    ins_customer.vchr_email = request.data.get('strEmail',None)
                    ins_customer.txt_address = request.data.get('strAddress',None)
                    ins_customer.vchr_gst_no = request.data.get('strGSTNo',None)
                    ins_customer.fk_location_id = request.data.get('intCityId',None)
                    ins_customer.fk_state_id = request.data.get('intStateId',None)
                    ins_customer.save()
                    dct_data={}
                    dct_data['intContactNo']=ins_customer.int_mobile
                    dct_data['strName']=ins_customer.vchr_name
                    dct_data['strEmail']=ins_customer.vchr_email
                    dct_data['strAddress']=ins_customer.txt_address
                    dct_data['strGSTNo']=ins_customer.vchr_gst_no
                    dct_data['intCityId']=ins_customer.fk_location_id
                    dct_data['intStateId']=ins_customer.fk_state_id
                    if dct_data['intCityId']:
                        dct_data['strCity'] = ins_customer.fk_location.vchr_name
                    if dct_data['intStateId']:
                        dct_data['strState'] = ins_customer.fk_state.vchr_name



                    return Response({'status':1,'data':dct_data})
            else:
                return Response({'status':'0','message':'No Data'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})


class VarifyOtp(APIView):
    """OTP Varification"""
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            ins_customer=SalesCustomerDetails.objects.filter(pk_bint_id = request.data.get('int_sales_cust_id'),fk_customer__dat_exp__gte=datetime.now(),fk_customer__vchr_otp=request.data['str_otp'])
            if ins_customer:
                return Response({'status':1,'message':'varified'})
            else:
                return Response({'status':0,'message':'not varified'})
            # rsp_request=requests.get("https://app.smsbits.in/api/users?id=OTg0NjY2OTk1NQ&senderid=myGsms&to="+str(ins_customer[0].int_mobile)+"&msg=Dear Customer,Your OTP for change customer details is "+str(str_otp)+" .&port=TA")
            # if rsp_request.status_code==200:
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})

class CustomerHistory(APIView):
    """
    To list all receipt,payment,sales,sales return  details of a customer
    param : customer id
    return : list of customer data about receipt,payment,sales,sales return
    """
    permission_classes = [AllowAny]
    def post(self,request):
        try:


            int_cust_id = request.data.get('id')

            lst_data = []
            lst_receipt = []
            lst_payment = []
            lst_sales = []
            lst_sales_return = []
            lst_customer_hystory = []


            session = Session()
            # Receipt
            bln_receipt = False
            # import pdb; pdb.set_trace()
            rst_receipt = session.query(func.DATE(ReceiptSA.dat_created).label("date"),func.sum(func.coalesce(ReceiptSA.dbl_amount,0)).label('amount'),BankSA.vchr_name,ReceiptSA.vchr_receipt_num,ReceiptSA.pk_bint_id,BranchSA.vchr_code)\
                                 .join(BankSA,BankSA.pk_bint_id == ReceiptSA.fk_bank_id)\
                                 .join(BranchSA,BranchSA.pk_bint_id == ReceiptSA.fk_branch_id)\
                                 .filter(ReceiptSA.fk_customer_id == int_cust_id)
            if request.user.userdetails.fk_branch.int_type not in [2,3] or request.user.userdetails.fk_group.vchr_name.upper() != 'ADMIN':
                 rst_receipt = rst_receipt.filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_receipt=rst_receipt.group_by('date',BankSA.vchr_name,ReceiptSA.vchr_receipt_num,BranchSA.vchr_code,ReceiptSA.pk_bint_id).all()

            if rst_receipt:
                bln_receipt = True
                lst_receipt = [{'date':datetime.strftime(item.date,'%d-%m-%Y'),'details':'Paid Advance amount '+str(round(item.amount,2)),'vchr_bank':item.vchr_name,'vchr_receipt_num':item.vchr_receipt_num,'vchr_branch_code':item.vchr_code,'int_receipt_id':item.pk_bint_id,'bln_receipt':bln_receipt} for item in  rst_receipt]
            # Payment
            rst_payment = session.query(func.DATE(ReceiptInvoiceMatchingSA.dat_created).label("date"),func.sum(func.coalesce(ReceiptInvoiceMatchingSA.dbl_amount,0)).label('amount'),func.array_agg(distinct(ReceiptSA.vchr_receipt_num)).label('receipt_no'),func.array_agg(distinct(ReceiptSA.pk_bint_id)).label('int_id'))\
                                 .join(PaymentSA,PaymentSA.pk_bint_id == ReceiptInvoiceMatchingSA.fk_payment_id)\
                                 .join(ReceiptSA,ReceiptSA.pk_bint_id == ReceiptInvoiceMatchingSA.fk_receipt_id)\
                                 .filter(PaymentSA.fk_payee_id == int_cust_id,PaymentSA.int_payee_type == 1)
            if request.user.userdetails.fk_branch.int_type not in [2,3] or request.user.userdetails.fk_group.vchr_name.upper() != 'ADMIN':
                rst_payment = rst_payment.filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id,PaymentSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_payment=rst_payment.group_by('date').all()
            if rst_payment:
                bln_receipt = False
                lst_payment = [{'bln_receipt':bln_receipt,'bln_receipt_view':True,'bln_invoice_view':False,'bln_return_view':False,'lst_doc_num':item.receipt_no,'lst_receipt_id':item.int_id,'date':datetime.strftime(item.date,'%d-%m-%Y'),'details':'Advance refund  amount '+str(round(item.amount,2))+' of receipt no : '} for item in rst_payment]
            # Sales
            rst_sales = session.query(func.DATE(SalesMasterSA.dat_created).label("date"),func.sum(func.coalesce(SalesDetailsSA.dbl_selling_price,0)).label('amount'),func.array_agg(ItemSA.vchr_name).label('item'),func.array_agg(distinct(SalesMasterSA.vchr_invoice_num)).label('invoice_no'),func.array_agg(distinct(SalesMasterSA.pk_bint_id)).label('int_id'))\
                               .join(SalesDetailsSA,SalesDetailsSA.fk_master_id == SalesMasterSA.pk_bint_id)\
                               .join(SalesCustomerDetailsSA,SalesCustomerDetailsSA.pk_bint_id == SalesMasterSA.fk_customer_id)\
                               .join(ItemSA,ItemSA.pk_bint_id == SalesDetailsSA.fk_item_id)\
                               .filter(SalesCustomerDetailsSA.fk_customer_id == int_cust_id,SalesDetailsSA.int_sales_status==1)
            if request.user.userdetails.fk_branch.int_type not in [2,3] or request.user.userdetails.fk_group.vchr_name.upper() != 'ADMIN':
                rst_sales = rst_sales.filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_sales = rst_sales.group_by('date').all()
            if rst_sales:
                bln_receipt = False
                lst_sales = [{'bln_receipt':bln_receipt,'lst_sales_id':item.int_id,'lst_doc_num':item.invoice_no,'bln_receipt_view':False,'bln_return_view':False,'bln_invoice_view':True,'date':datetime.strftime(item.date,'%d-%m-%Y'),'details':'Purchased '+str(','.join(set(item.item)))+' worth '+str(round(item.amount,2))+' of invoice no : '}for item in rst_sales]
            # Sales Return
            rst_sales_return = session.query(func.DATE(SalesReturnSA.dat_returned).label('date'),func.sum(func.coalesce((SalesDetailsSA.dbl_selling_price)*(-1))).label('amount'),func.array_agg(ItemSA.vchr_name).label('item'),func.array_agg(distinct(SalesMasterSA.vchr_invoice_num)).label('invoice_no'),func.array_agg(distinct(SalesMasterSA.pk_bint_id)).label('int_id'))\
                               .join(SalesMasterSA,SalesMasterSA.pk_bint_id == SalesReturnSA.fk_sales_id)\
                               .join(SalesDetailsSA,SalesDetailsSA.fk_master_id == SalesMasterSA.pk_bint_id)\
                               .join(SalesCustomerDetailsSA,SalesCustomerDetailsSA.pk_bint_id == SalesMasterSA.fk_customer_id)\
                               .join(ItemSA,ItemSA.pk_bint_id == SalesDetailsSA.fk_item_id)\
                               .filter(SalesCustomerDetailsSA.fk_customer_id == int_cust_id,SalesDetailsSA.int_sales_status == 0)
            if request.user.userdetails.fk_branch.int_type not in [2,3] or request.user.userdetails.fk_group.vchr_name.upper() != 'ADMIN':
                rst_sales_return = rst_sales_return.filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_sales_return = rst_sales_return.group_by('date').all()

            # rst_sales_return = rst_sales_return.all()
            if rst_sales_return:
                bln_receipt = False
                lst_sales_return = [{'bln_receipt':bln_receipt,'lst_return_id':item.int_id,'lst_doc_num':item.invoice_no,'bln_receipt_view':False,'bln_return_view':True,'date':datetime.strftime(item.date,'%d-%m-%Y'),'details':'Returned '+str(','.join(set(item.item)))+' worth '+str(round((item.amount),2))+' of invoice no : '}for item in rst_sales_return]
            # changes occured in costomer details

            lst_cust_details = list( SalesCustomerDetails.objects.filter(fk_customer__pk_bint_id = int_cust_id).annotate(str_name=Concat('fk_created_id__user_ptr_id__first_name', Value(' '), 'fk_created_id__user_ptr_id__last_name')).values('pk_bint_id','dat_created','vchr_name','vchr_email','int_mobile','fk_state_id','fk_state__vchr_name','fk_location_id','fk_location__vchr_name','int_cust_type','str_name' ).order_by('pk_bint_id'))
            dct_temp_cust = lst_cust_details[0]
            lst_cust_details.pop(0)
            dct_cust_hystory = {}
            lst_cust_type = ['Normal Customer','Credit Customer','unknown','unknown','unknown']

            if lst_cust_details :

                for inst_cust in lst_cust_details :
                    date_created = datetime.strftime(inst_cust['dat_created'],'%d-%m-%Y')
                    if date_created not in dct_cust_hystory.keys():
                        dct_cust_hystory[date_created] = ''
                    if dct_temp_cust['vchr_name'] != inst_cust['vchr_name']:
                        string_temp = 'Name Changed from ' + str(dct_temp_cust['vchr_name']) + ' to '+ str(inst_cust['vchr_name']) +' by ' +str(inst_cust['str_name'])+ '. '
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp
                    if dct_temp_cust['vchr_email'] != inst_cust['vchr_email']:
                        string_temp = 'Email changed from ' +  str(dct_temp_cust['vchr_email']) + ' to '+ str(inst_cust['vchr_email']) +' by ' +str(inst_cust['str_name'])+ '.'
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp
                    if dct_temp_cust['int_mobile'] != inst_cust['int_mobile']:
                        string_temp = 'Mobile Number changed from ' +  str(dct_temp_cust['int_mobile']) + ' to '+ str(inst_cust['int_mobile']) +' by ' +str(inst_cust['str_name'])+ '. '
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp
                    if dct_temp_cust['fk_state_id'] != inst_cust['fk_state_id']:
                        string_temp = 'State changed from ' +  str(dct_temp_cust['fk_state__vchr_name']) + ' to '+ str(inst_cust['fk_state__vchr_name']) +' by ' +str(inst_cust['str_name'])+ '. '
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp
                    if dct_temp_cust['fk_location_id'] != inst_cust['fk_location_id']:
                        string_temp = 'Location changed from ' +  str(dct_temp_cust['fk_location__vchr_name']) + ' to '+ str(inst_cust['fk_location__vchr_name']) +' by ' +str(inst_cust['str_name'])+ '. '
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp
                    if dct_temp_cust['int_cust_type'] != inst_cust['int_cust_type']:
                        cust_type_before = lst_cust_type[int(dct_temp_cust['int_cust_type'])]
                        cust_type_after = lst_cust_type[int(inst_cust['int_cust_type'])]
                        string_temp = 'Type of Customer changed from ' + cust_type_before + ' to '+cust_type_after   +' by ' +str(inst_cust['str_name'])+'. '
                        dct_cust_hystory[date_created] = str(dct_cust_hystory[date_created]) + string_temp

                    dct_temp_cust = inst_cust
                    # import pdb; pdb.set_trace()


            dct_trial = {}
            for inst_dct_cust in dct_cust_hystory:
                dct_trial['date']= inst_dct_cust
                dct_trial['details'] =  dct_cust_hystory[inst_dct_cust]
                lst_customer_hystory.append(dct_trial)

            lst_data = lst_receipt+lst_payment+lst_sales+lst_sales_return+lst_customer_hystory
            rst_data = sorted(lst_data, key = lambda i: i['date'])
            session.close()
            return Response({'status':1,'lst_data':rst_data})

        except Exception as e:
            session.close()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})





class AddCustomerPOS(APIView):
    permission_classes = [IsAuthenticated]
    def post (self,request):
        try:
            str_search_term = request.data.get('term',-1)
            if str_search_term != -1:
                ins_customer=SalesCustomerDetails.objects.filter(int_mobile__icontains=str_search_term).order_by('-pk_bint_id').first()
                lst_data=[]
                dct_data={}

            if ins_customer:
                dct_data['intCustId'] = ins_customer.fk_customer_id
                dct_data['intSalesCustId'] = ins_customer.pk_bint_id
                dct_data['strCustName'] = ins_customer.vchr_name
                dct_data['strCustEmail'] = ins_customer.vchr_email
                dct_data['intContactNo'] = ins_customer.int_mobile
                dct_data['txtAddress'] = ins_customer.txt_address
                dct_data['strGSTNo'] = ins_customer.vchr_gst_no
                dct_data['intCityId'] = ins_customer.fk_location_id
                dct_data['int_cust_type'] = ins_customer.int_cust_type
                if dct_data['intCityId']:
                    dct_data['strLocation'] = ins_customer.fk_location.vchr_name
                dct_data['intStateId'] = ins_customer.fk_state_id
                if dct_data['intStateId']:
                    dct_data['strState'] = ins_customer.fk_state.vchr_name
                bln_igst = False
                if request.user.userdetails.fk_branch.fk_states_id != ins_customer.fk_state_id:
                    bln_igst = True
                    dct_data['blnIGST'] = bln_igst
                lst_data.append(dct_data)
            else:
                pass


            return Response({'status':1,'data':lst_data})


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})
#
    def put (self,request):
        try:

            str_cust_name = request.data.get('strName')
            str_cust_email = request.data.get('strEmail',None)
            int_cust_mob = request.data.get('intMob')
            ins_state = None
            if request.data.get('strStateCode'):
                ins_state = States.objects.filter(vchr_name__iexact = request.data.get('strState')).first()
            if not ins_state :
                ins_state =  States.objects.filter(pk_bint_id=request.data.get('intStateId')).first()
            # ins_district = None
            # if request.data.get('strDistrict'):
            #     ins_district = District.objects.filter(vchr_name = request.data.get('strDistrict')).first()
            #     if not ins_district:
            #         ins_district = District.objects.create(vchr_name = request.data.get('strDistrict'),fk_state=ins_state)
            #     if not ins_state:
            #         ins_state = ins_district.fk_state
            ins_location = None
            if request.data.get('strCity'):
                ins_location = Location.objects.filter(vchr_name__contains=request.data.get('strCity',None),vchr_pin_code=request.data.get('strPinCode',None)).first()
                if not ins_location:
                    ins_location = Location.objects.create(vchr_name=request.data.get('strCity',None),vchr_pin_code=request.data.get('strPinCode',None))
                if not ins_state:
                    ins_state = ins_location.fk_state

            ins_dup_cus = CustomerDetails.objects.filter(int_mobile = int_cust_mob).values()
            if ins_dup_cus:
                return Response({'status':0,'reason':'Customer Already Exists'})
            ins_customer = CustomerDetails.objects.create(
                                                            vchr_name = str_cust_name,
                                                            vchr_email = str_cust_email,
                                                            int_mobile = int_cust_mob,
                                                            vchr_gst_no = request.data.get('strGSTNo',None),
                                                            txt_address = request.data.get('strAddress',None),
                                                            fk_location = ins_location,
                                                            fk_state = ins_state,
                                                            int_edit_count=0,
                                                            int_cust_type=4
                                                         )



            # ========================================================================================================
            ins_sales_customer = SalesCustomerDetails.objects.create(
                                                    fk_customer_id = ins_customer.pk_bint_id,
                                                    dat_created = datetime.now(),
                                                    fk_created_id = request.user.id,
                                                    vchr_name = str_cust_name,
                                                    vchr_email = str_cust_email,
                                                    int_mobile = int_cust_mob,
                                                    vchr_gst_no = request.data.get('strGSTNo',None),
                                                    txt_address = request.data.get('strAddress',None),
                                                    fk_location = ins_location,
                                                    fk_state = ins_state,
                                                    int_cust_type=4
                                                 )

            dct_data = {}
            dct_data['strLocation']=''
            dct_data['strState']=''
            dct_data['intCustId'] = ins_customer.pk_bint_id
            dct_data['intSalesCustId'] = ins_sales_customer.pk_bint_id
            dct_data['strCustName'] = ins_customer.vchr_name
            dct_data['strCustEmail'] = ins_customer.vchr_email
            dct_data['intContactNo'] = ins_customer.int_mobile
            dct_data['txtAddress'] = ins_customer.txt_address
            dct_data['strGSTNo'] = ins_customer.vchr_gst_no
            dct_data['intCityId'] = ins_customer.fk_location_id
            dct_data['int_cust_type'] = ins_sales_customer.int_cust_type
            if dct_data['intCityId']:
                dct_data['strLocation'] = ins_customer.fk_location.vchr_name
            dct_data['intStateId'] = ins_customer.fk_state_id
            if dct_data['intStateId']:
                dct_data['strState'] = ins_customer.fk_state.vchr_name
            dct_data['blnIGST'] = False
            if request.user.userdetails.fk_branch.fk_states_id != ins_customer.fk_state_id:
                dct_data['blnIGST'] = True
            dct_pos=dict(Location.objects.filter(pk_bint_id=dct_data['intCityId']).values('fk_state__vchr_name','fk_state__vchr_code','vchr_district','vchr_pin_code','vchr_name').first())
            url =settings.BI_HOSTNAME + "/customer/customer_update/"
            dct_pos.update(dct_data)
            dct_pos['user_name'] = request.user.username

            res_data = requests.post(url,json=dct_pos)
            if res_data.json().get('status')=='1':
                pass
            else:
                raise ValueError('Something happened in BI')

            return Response({'status':1,'data':dct_data})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})

            return Response({'result':0,'reason':e})


class AddCustomerSalesReturn (APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:

            with transaction.atomic():

                str_cust_name = request.data.get('strName')
                str_cust_email = request.data.get('strEmail',None)
                int_cust_mob = request.data.get('intMob')
                ins_state = None
                ins_customer = CustomerDetails.objects.filter(int_mobile = int_cust_mob)
                if ins_customer :
                    return Response({"status": 0 , "data": "failed" })

                else :
                    if request.data.get('strStateCode'):
                        ins_state = States.objects.filter(vchr_name__iexact = request.data.get('strState')).all().first()

                    if not ins_state :
                        ins_state =  States.objects.filter(pk_bint_id=request.data.get('intStateId')).all().first()

                    ins_location = None
                    if request.data.get('strCity'):
                        ins_location = Location.objects.filter(vchr_name__contains=request.data.get('strCity',None),vchr_pin_code=request.data.get('strPinCode',None)).first()
                        if not ins_location:
                            ins_location = Location.objects.create(vchr_name=request.data.get('strCity',None),vchr_pin_code=request.data.get('strPinCode',None))
                        if not ins_state:
                            ins_state = ins_location.fk_state

                    ins_customer = CustomerDetails(
                                                    vchr_name = str_cust_name,
                                                    vchr_email = str_cust_email,
                                                    int_mobile = int_cust_mob,
                                                    vchr_gst_no = request.data.get('strGSTNo',None),
                                                    txt_address = request.data.get('strAddress',None),
                                                    fk_location = ins_location,
                                                    fk_state = ins_state,
                                                    int_edit_count=0,
                                                    int_cust_type=4
                                                 )
                    ins_customer.save()

                    ins_sales_customer = SalesCustomerDetails(
                                                            fk_customer_id = ins_customer.pk_bint_id,
                                                            dat_created = datetime.now(),
                                                            fk_created_id = request.user.id,
                                                            vchr_name = str_cust_name,
                                                            vchr_email = str_cust_email,
                                                            int_mobile = int_cust_mob,
                                                            vchr_gst_no = request.data.get('strGSTNo',None),
                                                            txt_address = request.data.get('strAddress',None),
                                                            fk_location = ins_location,
                                                            fk_state = ins_state,
                                                            int_cust_type=4
                                                         )
                    ins_sales_customer.save()

                    # dct_data = {}
                    # dct_data[""] =
                    # dct_data[""] =
                    # dct_data[""] =
                    # dct_data[""] =
                    # dct_data[""] =
                    # dct_data[""] =

                    lst_name = str_cust_name.split(" ")
                    fname = lst_name[0]
                    lname = " "
                    if len(lst_name) >= 2 :
                        lname = lst_name[1]
                    dct_data = {}
                    dct_data["fname"] = fname
                    dct_data["lname"] = lname
                    dct_data["salutation"] = ""
                    dct_data["username"] = request.user.username
                    dct_data["alternateMail"] = None
                    dct_data["alternateMobile"] = None
                    dct_data["contactSrc"] = None
                    dct_data["customerType"] = None
                    dct_data["smsAccess"] = None
                    dct_data["locationId"] = None
                    # dct_data["contactSrc"] = None
                    # dct_data["contactSrc"] = None
                    dct_data["email"] = str_cust_email
                    dct_data["mobile"] = int_cust_mob
                    dct_data["gst"] = request.data.get('strGSTNo',None)
                    dct_data["txt_address"] = request.data.get('strAddress',None)
                    dct_data["fk_location_id"] = ins_location.vchr_pin_code
                    dct_data["stateName"] = ins_state.vchr_name
                    dct_data["creditLimit"] =  None,

                    dct_data["fk_created_id"] = request.user.id
                    dct_data["blnPOS"] = True
                    url = settings.BI_HOSTNAME + "/customer/customer_add_pos/"
                    res_data = requests.post(url,json = dct_data)
                    if res_data.json().get("data") == "Success":
                        return Response({"status": 1 , "data": "saved","sales_cust_id" : ins_customer.pk_bint_id })
                    else :
                        raise ValueError('Something happened in BI')
                        return JsonResponse({'status': 'Failed','data':res_data.json().get('message',res_data.json())})
                return Response({"status" : 0 , "data": "failed-may be an issue with BI SUITE "})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})

            return Response({'result':0,'reason':e})


class getSelectedCustomerList(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):

        try:
            # import pdb;pdb.set_trace()
            lst_customerlist = list(CustomerDetails.objects.filter(pk_bint_id=request.data['id']).values('pk_bint_id','int_mobile','vchr_email','vchr_name','cust_salutation','fk_location_id','fk_location_id__vchr_name','fk_state_id','fk_state_id__vchr_name','cust_smsaccess') )
            # 'cust_alternatemobile','cust_alternatemail','cust_contactsrc','cust_customertype','cust_smsaccess','vchr_gst_no','dbl_credit_amount'
            # return Response({'status':'0'})
            # for d in lst_customerlist:
            #     d['name']=d['vchr_name']
            lst_customer_occassions  = list(CustomerOccasionsModel.objects.filter( int_cust_id =request.data['id']).values('pk_bint_id','vchr_occasion_name','dat_occasion_date'))

            rst_customer_rating = CustomerRating.objects.filter(fk_customer = request.data['id']).values('pk_bint_id','vchr_feedback','dbl_rating','fk_customer','fk_user').aggregate(Avg('dbl_rating'))
            if(rst_customer_rating['dbl_rating__avg'] != None):
                int_rating = math.floor(rst_customer_rating['dbl_rating__avg'])
            else:
                int_rating = 0
            return JsonResponse({'cust_list':lst_customerlist,'cust_occasions':lst_customer_occassions,'cust_rating':int_rating})

        except Exception as e:
            # print(e)
            return Response({'status':'1'})

# class getSelectedCustomerList(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):

#         try:
#             import pdb;pdb.set_trace()
#             lst_customerlist = list(CustomerDetails.objects.filter(pk_bint_id=request.data['id']).values('pk_bint_id','cust_mobile','cust_email','cust_salutation','cust_fname','cust_lname','cust_alternatemobile','cust_alternatemail','cust_contactsrc','cust_customertype','cust_smsaccess','fk_location_id','fk_location_id__vchr_name','fk_state_id','fk_state_id__vchr_name','vchr_gst_no','dbl_credit_amount') )
#             # return Response({'status':'0'})
#             # for d in lst_customerlist:
#             #     d['name']=d['cust_fname']+' '+d['cust_lname']
#             lst_customer_occassions  = list(CustomerOccasionsModel.objects.filter( cust_id =request.data['id']).values('pk_bint_id','occasion_name','occasion_date'))

#             rst_customer_rating = CustomerRating.objects.filter(fk_customer = request.data['id']).values('pk_bint_id','vchr_feedback','dbl_rating','fk_customer','fk_user').aggregate(Avg('dbl_rating'))
#             if(rst_customer_rating['dbl_rating__avg'] != None):
#                 int_rating = math.floor(rst_customer_rating['dbl_rating__avg'])
#             else:
#                 int_rating = 0
#             return JsonResponse({'cust_list':lst_customerlist,'cust_occasions':lst_customer_occassions,'cust_rating':int_rating})

#         except Exception as e:
#             # print(e)
#             return Response({'status':'1'})


class getCustomerList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            # import pdb;pdb.set_trace()

            int_company = int(request.GET.get('id'))
            if int_company:
                # company_id
                lst_customerlist = list(CustomerDetails.objects.filter().values('pk_bint_id','int_mobile','vchr_email','cust_salutation','vchr_name','fk_location_id__vchr_name').order_by('-pk_bint_id') )
            else:
                lst_customerlist = list(CustomerDetails.objects.filter().values('pk_bint_id','int_mobile','vchr_email','cust_salutation','vchr_name','fk_location_id__vchr_name').order_by('-pk_bint_id') )
            # return Response({'status':'0'})
            # for d in lst_customerlist:
            #     # d['name']=d['cust_fname']+' '+d['cust_lname']
            #     d['name']=d['vchr_name']
            return JsonResponse({'lst_cust':lst_customerlist})
        except Exception as e:
            return Response({'status':'1'})