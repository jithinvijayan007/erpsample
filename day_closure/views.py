from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import HttpResponse
from django.http import JsonResponse

from sqlalchemy.orm import sessionmaker,aliased
from sqlalchemy import and_,func ,cast,DATE,case,distinct,Date
from aldjemy.core import get_engine
from .models import DayClosureMaster,DayClosureDetails,DayClosureNotTally
from invoice.models import SalesMaster,SalesDetails
import json
import datetime
from userdetails.models import UserDetails as Userdetails
from django.contrib.auth.models import User as AuthUser

import pdfkit
import base64
from os import remove
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
from Crypto.Cipher import AES
import binascii
from django.db import transaction
from branch.models import Branch
from django.contrib.auth.models import User as AuthUser
from userdetails.models import UserDetails as Userdetails
from payment.models import Payment
from receipt.models import Receipt

from invoice.models import PaymentDetails
import sys, os
from POS import ins_logger
from aldjemy.core import get_engine
from POS.dftosql import Savedftosql
# from datetime import datetime
from django.db.models import F, Q, Value, Case, When, CharField, Sum
from django.db.models.functions import Concat


DayClosureMasterSA = DayClosureMaster.sa
DayClosureDetailsSA = DayClosureDetails.sa
DayClosureNotTallySA = DayClosureNotTally.sa
SalesMasterSA = SalesMaster.sa
SalesDetailsSA = SalesDetails.sa
BranchSA = Branch.sa
AuthUserSA = AuthUser.sa
UserdetailsSA = Userdetails.sa
PaymentSA = Payment.sa
ReceiptSA = Receipt.sa
PaymentDetailsSA=PaymentDetails.sa

sqlalobj = Savedftosql('','')
engine = sqlalobj.engine
engine = get_engine()
def Session():
    _Session = sessionmaker(bind = engine)
    return _Session()

# Create your views here.
class DayClosureList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            """listing day_closure """
            session=Session()
            rst_list_dayclosure = session.query(DayClosureMasterSA.pk_bint_id.label('master_id'),\
                                        DayClosureMasterSA.vchr_name.label('note'))\
                                        .filter(DayClosureMasterSA.bln_active == True)\
                                        .order_by('master_id')
            lst_dayclosure = []
            for ins_dayclosure in rst_list_dayclosure:
                dct_dayclosure = {}
                dct_dayclosure['master_id'] = ins_dayclosure.master_id
                dct_dayclosure['note'] = ins_dayclosure.note
                lst_dayclosure.append(dct_dayclosure)

            rst_dayclosure_last_closed = session.query(DayClosureDetailsSA.pk_bint_id.label('id'),\
                                                    func.DATE(DayClosureDetailsSA.dat_time).label('dat'),\
                                                    DayClosureDetailsSA.total_amount.label('total_amount'),\
                                                    DayClosureDetailsSA.int_closed.label('int_status'),\
                                                    DayClosureDetailsSA.json_dayclosure.label('json_data'))\
                                                    .filter(DayClosureDetailsSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                                                    .order_by(DayClosureDetailsSA.pk_bint_id.desc())
            """verifying last days dayclosure"""
            # import pdb; pdb.set_trace()
            lst_verify = []
            if rst_dayclosure_last_closed.all() :
                rst_dayclosure_last_closed = rst_dayclosure_last_closed.first()
                if rst_dayclosure_last_closed.int_status in [1,2]:
                    if datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d') == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'):
                        return Response({'status':1, 'message' : 'Dayclosure Allready Added...',"blnStatus":True})
                #     else:
                #         dct_verify = {}
                #         dct_verify['total_amount'] = rst_dayclosure_last_closed.total_amount
                #         dct_verify['id'] = rst_dayclosure_last_closed.id
                #         dct_verify['dat'] = datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%d-%m-%Y')
                #         lst_verify.append(dct_verify)

                #         session.close()
                #         return Response({'status':1, 'lst_verify' : lst_verify ,'lst_dayclosure' : lst_dayclosure  })

                # elif rst_dayclosure_last_closed.int_status == 2 or rst_dayclosure_last_closed.int_status == 3 or rst_dayclosure_last_closed.int_status == 4:
                #     # if datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d') == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'):

                #     # rst_total_amount =session.query(func.sum(func.coalesce(SalesMasterSA.dbl_total_amt,0).label('total_amount')))\
                #     #                     .filter(func.DATE(SalesMasterSA.dat_invoice) == datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d'))\
                #     #                     .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)

                #     rst_total_amount =session.query(func.sum(func.coalesce(PaymentDetailsSA.dbl_receved_amt,0).label('total_amount')))\
                #                         .join(SalesMasterSA,PaymentDetailsSA.fk_sales_master_id==SalesMasterSA.pk_bint_id)\
                #                         .filter(PaymentDetailsSA.int_fop==1)\
                #                         .filter(func.DATE(SalesMasterSA.dat_created) == datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d'))\
                #                         .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)

                #     rst_payment_amount = session.query(func.sum(func.coalesce(PaymentSA.dbl_amount,0).label('total_amount')))\
                #                         .filter(func.DATE(PaymentSA.dat_payment) == datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d'))\
                #                         .filter(PaymentSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                #                         .filter(PaymentSA.int_fop == 1,PaymentSA.int_doc_status==0)

                #     rst_receipt_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                #                         .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d'))\
                #                         .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                #                         .filter(ReceiptSA.int_fop == 1,ReceiptSA.fk_sales_return ==None)
                #     # rst_sales_return_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                #     #                     .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d'))\
                #     #                     .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                #     #                     .filter(ReceiptSA.int_fop == 1,ReceiptSA.vchr_remarks.ilike('sales return amount'))

                #     ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
                #                                                                                 'total_amount',
                #                                                                                 'json_dayclosure'
                #                                                                                 ).order_by('-pk_bint_id').first()

                #     rst_remarks = DayClosureNotTally.objects.filter(fk_day_closure_details_id = rst_dayclosure_last_closed.id).values('vchr_remark').order_by('-pk_bint_id').first()
                #     str_remarks = ""
                #     if rst_remarks:
                #         str_remarks =  rst_remarks['vchr_remark']

                #     sales_amount = 0
                #     payment_amount = 0
                #     receipt_amount = 0
                #     return_amount = 0
                #     if rst_total_amount.all():
                #         if rst_total_amount[0][0]:
                #             sales_amount = rst_total_amount[0][0]

                #     if rst_payment_amount.all():
                #         if rst_payment_amount[0][0]:
                #             payment_amount = rst_payment_amount[0][0]

                #     if rst_receipt_amount.all():
                #         if rst_receipt_amount[0][0]:
                #             receipt_amount = rst_receipt_amount[0][0]
                #     # if rst_sales_return_amount.all():
                #     #     if rst_sales_return_amount[0][0]:
                #     #         return_amount = rst_sales_return_amount[0][0]


                #     total_amount = 0
                #     if  ins_last_dayclosure:
                #          total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount - return_amount)
                #     else:
                #          total_amount = round(sales_amount + receipt_amount  - payment_amount- return_amount)

                #     amount =  total_amount - rst_dayclosure_last_closed.total_amount

                #     dct_data = {}
                #     dct_data['amount'] = amount
                #     dct_data['lst_dayclosure'] = lst_dayclosure
                #     dct_data['id'] = rst_dayclosure_last_closed.id
                #     dct_data['json_data'] = rst_dayclosure_last_closed.json_data
                #     dct_data['str_remarks'] = str_remarks
                #     dct_data['dat_time'] = datetime.datetime.strftime(rst_dayclosure_last_closed.dat,'%Y-%m-%d')
                #     dct_data['request_mail'] = False
                #     dct_data['int_status'] = rst_dayclosure_last_closed.int_status

                #     if rst_dayclosure_last_closed.int_status == 3 or rst_dayclosure_last_closed.int_status == 4:
                #         dct_data['request_mail'] = True

                #     session.close()
                #     return Response({'status':2, 'data' : 'Amount not tally', 'dct_data' : dct_data })

            # print(rst_dayclosure_last_closed.all())
            session.close()
            return Response({'status':1, 'lst_dayclosure' : lst_dayclosure , 'lst_verify' : None,"blnStatus":False})

        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})

    def post(self,request):
        try:
            session=Session()
            # import pdb; pdb.set_trace()
            # """verify last days day_closure"""
            # if request.data.get('check_verify'):
            #     rst_verify_details = session.query(DayClosureDetailsSA.json_dayclosure.label('json_data'),\
            #                                         DayClosureDetailsSA.total_amount.label('total_amount'))\
            #                                     .filter(DayClosureDetailsSA.pk_bint_id == request.data.get('id')).first()._asdict()
            #     ins_dayclosure_details = DayClosureDetails()
            #     ins_dayclosure_details.fk_staff_id = request.user.id
            #     ins_dayclosure_details.dat_time = datetime.datetime.now()
            #     ins_dayclosure_details.total_amount = rst_verify_details['total_amount']
            #     ins_dayclosure_details.int_closed = 0
            #     ins_dayclosure_details.json_dayclosure = json.dumps(rst_verify_details['json_data'])
            #     ins_dayclosure_details.fk_branch_id = request.user.userdetails.fk_branch_id
            #     ins_dayclosure_details.save()

            # if request.data.get('make_tally'):
            #     """make tally by respective staff"""
            #     rst_date_detail = session.query(DayClosureDetailsSA.dat_time.label('dat_time'))\
            #                                     .filter(DayClosureDetailsSA.pk_bint_id == request.data.get('id')).first()

            #     # rst_total_amount =session.query(func.sum(func.coalesce(SalesMasterSA.dbl_total_amt,0).label('total_amount')))\
            #     #                             .filter(func.DATE(SalesMasterSA.dat_invoice) == datetime.datetime.strftime(rst_date_detail.dat_time,'%Y-%m-%d'))\
            #     #                             .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            #     rst_total_amount =session.query(func.sum(func.coalesce(PaymentDetailsSA.dbl_receved_amt,0).label('total_amount')))\
            #                         .join(SalesMasterSA,PaymentDetailsSA.fk_sales_master_id==SalesMasterSA.pk_bint_id)\
            #                         .filter(PaymentDetailsSA.int_fop==1)\
            #                         .filter(func.DATE(SalesMasterSA.dat_created) ==datetime.datetime.strftime(rst_date_detail.dat_time,'%Y-%m-%d'))\
            #                         .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)

            #     rst_payment_amount = session.query(func.sum(func.coalesce(PaymentSA.dbl_amount,0).label('total_amount')))\
            #                         .filter(func.DATE(PaymentSA.dat_payment) == datetime.datetime.strftime(rst_date_detail.dat_time,'%Y-%m-%d'))\
            #                         .filter(PaymentSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
            #                         .filter(PaymentSA.int_fop == 1,PaymentSA.int_doc_status==0)

            #     rst_receipt_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
            #                         .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(rst_date_detail.dat_time,'%Y-%m-%d'))\
            #                         .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
            #                         .filter(ReceiptSA.int_fop == 1,ReceiptSA.fk_sales_return ==None)
            #     # rst_sales_return_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
            #     #                     .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(rst_date_detail.dat_time,'%Y-%m-%d'))\
            #     #                     .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
            #     #                     .filter(ReceiptSA.int_fop == 1,ReceiptSA.vchr_remarks.ilike('sales return amount'))
            #     ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
            #                                                                                 'total_amount',
            #                                                                                 'json_dayclosure'
            #                                                                                 ).order_by('-pk_bint_id').first()

            #     sales_amount = 0
            #     payment_amount = 0
            #     receipt_amount = 0
            #     return_amount = 0
            #     if rst_total_amount.all():
            #         if rst_total_amount[0][0]:
            #             sales_amount = rst_total_amount[0][0]

            #     if rst_payment_amount.all():
            #         if rst_payment_amount[0][0]:
            #             payment_amount = rst_payment_amount[0][0]

            #     if rst_receipt_amount.all():
            #         if rst_receipt_amount[0][0]:
            #             receipt_amount = rst_receipt_amount[0][0]

            #     # if rst_sales_return_amount.all():
            #     #     if rst_sales_return_amount[0][0]:
            #     #         return_amount = rst_sales_return_amount[0][0]


            #     total_amount = 0
            #     if  ins_last_dayclosure:
            #          total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount - return_amount)
            #     else:
            #          total_amount = round(sales_amount + receipt_amount  - payment_amount- return_amount)

            #     # total_amount = 0
            #     #
            #     # if  ins_last_dayclosure:
            #     #      total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount)
            #     # else:
            #     #      total_amount = round(sales_amount + receipt_amount  - payment_amount)

            #     # if total_amount == request.data.get('grandTot') :
            #     if total_amount == request.data.get('grandTot') :
            #         """if amount tally"""
            #         ins_update = DayClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update(\
            #                     fk_staff_id = request.user.id,\
            #                     dat_time = rst_date_detail.dat_time,\
            #                     total_amount = request.data.get('grandTot'),\
            #                     int_closed = 1,\
            #                     json_dayclosure = json.dumps(request.data.get('lstData')),\
            #                     fk_branch_id = request.user.userdetails.fk_branch_id)


            #         # ins_tally_id = DayClosureNotTally.objects.filter(fk_day_closure_details_id = request.data.get('id')).values('pk_bint_id').order_by('-pk_bint_id').first()['pk_bint_id']
            #         # ins_tally_update = DayClosureNotTally.objects.filter(pk_bint_id = ins_tally_id ).update(int_status = 2)
            #         ins_dayclosure_not_tally = DayClosureNotTally()
            #         ins_dayclosure_not_tally.fk_day_closure_details_id = request.data.get('id')
            #         ins_dayclosure_not_tally.dat_time = datetime.datetime.now()
            #         ins_dayclosure_not_tally.fk_staff_id = request.user.id
            #         ins_dayclosure_not_tally.total_amount = request.data.get('grandTot')
            #         ins_dayclosure_not_tally.json_dayclosure = json.dumps(request.data.get('lstData'))
            #         ins_dayclosure_not_tally.int_status = 2
            #         ins_dayclosure_not_tally.fk_branch_id = request.user.userdetails.fk_branch_id
            #         ins_dayclosure_not_tally.vchr_remark = request.data.get('str_remarks')
            #         ins_dayclosure_not_tally.save()


            #     else:
            #         """if amount not tally"""
            #         ins_update = DayClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update(\
            #                     fk_staff_id = request.user.id,\
            #                     dat_time = rst_date_detail.dat_time,\
            #                     total_amount = request.data.get('grandTot'),\
            #                     json_dayclosure = json.dumps(request.data.get('lstData')),\
            #                     fk_branch_id = request.user.userdetails.fk_branch_id)

            #         ins_dayclosure_not_tally = DayClosureNotTally()
            #         ins_dayclosure_not_tally.fk_day_closure_details_id = request.data.get('id')
            #         ins_dayclosure_not_tally.dat_time = datetime.datetime.now()
            #         ins_dayclosure_not_tally.fk_staff_id = request.user.id
            #         ins_dayclosure_not_tally.total_amount = request.data.get('grandTot')
            #         ins_dayclosure_not_tally.json_dayclosure = json.dumps(request.data.get('lstData'))
            #         ins_dayclosure_not_tally.int_status = 1
            #         ins_dayclosure_not_tally.fk_branch_id = request.user.userdetails.fk_branch_id
            #         ins_dayclosure_not_tally.vchr_remark = request.data.get('str_remarks')
            #         ins_dayclosure_not_tally.save()

            #         amount = round(total_amount) - request.data.get('grandTot')
            #         json_data = request.data.get('lstData')
            #         session.close()
            #         return Response({'status':0, 'data' : " Amount doesnot tally" ,"amount" : amount , "id" : ins_dayclosure_not_tally.fk_day_closure_details_id, 'json_data' :json_data })


            # else:
            # import pdb; pdb.set_trace()
            """checking if the entered amount is tallied with sales amount"""
            # rst_total_amount =session.query(func.sum(func.coalesce(SalesMasterSA.dbl_total_amt,0).label('total_amount')))\
            #                             .filter(func.DATE(SalesMasterSA.dat_invoice) == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))\
            #                             .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            #
            rst_total_amount =session.query(func.sum(func.coalesce(PaymentDetailsSA.dbl_receved_amt,0).label('total_amount')))\
                                .join(SalesMasterSA,PaymentDetailsSA.fk_sales_master_id==SalesMasterSA.pk_bint_id)\
                                .filter(PaymentDetailsSA.int_fop==1)\
                                .filter(func.DATE(SalesMasterSA.dat_created) == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))\
                                .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)

            rst_payment_amount = session.query(func.sum(func.coalesce(PaymentSA.dbl_amount,0).label('total_amount')))\
                                .filter(func.DATE(PaymentSA.dat_payment) == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))\
                                .filter(PaymentSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                                .filter(PaymentSA.int_fop == 1,PaymentSA.int_doc_status==0)

            rst_receipt_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                                .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))\
                                .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                                .filter(ReceiptSA.int_fop == 1,ReceiptSA.fk_sales_return ==None)
            # rst_sales_return_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
            #                     .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))\
            #                     .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
            #                     .filter(ReceiptSA.int_fop == 1,ReceiptSA.vchr_remarks.ilike('sales return amount'))
            ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
                                                                                        'total_amount',
                                                                                        'json_dayclosure'
                                                                                        ).order_by('-pk_bint_id').first()


            sales_amount = 0
            payment_amount = 0
            receipt_amount = 0
            return_amount=0
            if rst_total_amount.all():
                if rst_total_amount[0][0]:
                    sales_amount = rst_total_amount[0][0]

            if rst_payment_amount.all():
                if rst_payment_amount[0][0]:
                    payment_amount = rst_payment_amount[0][0]

            if rst_receipt_amount.all():
                if rst_receipt_amount[0][0]:
                    receipt_amount = rst_receipt_amount[0][0]

            # if rst_sales_return_amount.all():
            #     if rst_sales_return_amount[0][0]:
            #         return_amount = rst_sales_return_amount[0][0]


            total_amount = 0
            if  ins_last_dayclosure:
                    total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount - return_amount)
            else:
                    total_amount = round(sales_amount + receipt_amount  - payment_amount- return_amount)

            # total_amount = 0
            #
            # if  ins_last_dayclosure:
            #      total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount)
            # else:
            #      total_amount = round(sales_amount + receipt_amount  - payment_amount)

            if total_amount == request.data.get('grandTot') :
                """if amount tally"""
                ins_dayclosure_details = DayClosureDetails()
                ins_dayclosure_details.fk_staff_id = request.user.id
                ins_dayclosure_details.dat_time = datetime.datetime.now()
                ins_dayclosure_details.total_amount = request.data.get('grandTot')
                ins_dayclosure_details.int_closed = 1
                ins_dayclosure_details.json_dayclosure = json.dumps(request.data.get('lstData'))
                ins_dayclosure_details.fk_branch_id = request.user.userdetails.fk_branch_id
                ins_dayclosure_details.save()
                ins_dayclosure_details.save()

            
            else:
                """if amount not tally"""
                ins_dayclosure_details = DayClosureDetails()
                ins_dayclosure_details.fk_staff_id = request.user.id
                ins_dayclosure_details.dat_time = datetime.datetime.now()
                ins_dayclosure_details.total_amount = request.data.get('grandTot')
                ins_dayclosure_details.int_closed = 2
                ins_dayclosure_details.json_dayclosure = json.dumps(request.data.get('lstData'))
                ins_dayclosure_details.fk_branch_id = request.user.userdetails.fk_branch_id
                ins_dayclosure_details.save()

                ins_dayclosure_not_tally = DayClosureNotTally()
                ins_dayclosure_not_tally.fk_day_closure_details_id = ins_dayclosure_details.pk_bint_id
                ins_dayclosure_not_tally.dat_time = datetime.datetime.now()
                ins_dayclosure_not_tally.fk_staff_id = request.user.id
                ins_dayclosure_not_tally.total_amount = request.data.get('grandTot')
                ins_dayclosure_not_tally.json_dayclosure = json.dumps(request.data.get('lstData'))
                ins_dayclosure_not_tally.int_status = 1
                ins_dayclosure_not_tally.fk_branch_id = request.user.userdetails.fk_branch_id
                ins_dayclosure_not_tally.vchr_remark = request.data.get('str_remarks')
                ins_dayclosure_not_tally.save()

                amount = round(total_amount) - request.data.get('grandTot')
                str_message = ''
                if amount < 0:
                    str_message = "Amount Not Tally RS:"+str(abs(amount))+" Excess, Please Check The Sales Report.."
                else:
                    str_message = "Amount Not Tally RS:"+str(abs(amount))+" Short, Please Check The Sales Report.."

                json_data = request.data.get('lstData')
                session.close()
                return Response({'status':1, 'message' : str_message  ,"amount" : amount , "id" : ins_dayclosure_details.pk_bint_id ,'json_data' :json_data})

                # print(request.data)
            session.close()
            return Response({'status':1})
        except Exception as e:
            session.close()
            return Response({'status':0,'message':str(e)})


class RequestMail(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """request day closure through mail"""
        try:
            # import pdb; pdb.set_trace()
            day_closure_id = request.data.get('id')
            session=Session()

            lst_not_tally_details = DayClosureDetails.objects.filter(pk_bint_id = day_closure_id).values('pk_bint_id','fk_branch_id','dat_time','total_amount','fk_branch__vchr_name','fk_staff_id','json_dayclosure').first()
            ins_mail_details = Userdetails.objects.filter(fk_group__vchr_name = "HO").values('user_ptr_id','first_name','email','last_name').first()

            # rst_total_amount = session.query(func.sum(func.coalesce(SalesMasterSA.dbl_total_amt,0).label('total_amount')))\
            #                                 .filter(func.DATE(SalesMasterSA.dat_invoice) == lst_not_tally_details['dat_time'])\
            #                                 .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_total_amount =session.query(func.sum(func.coalesce(PaymentDetailsSA.dbl_receved_amt,0).label('total_amount')))\
                                .join(SalesMasterSA,PaymentDetailsSA.fk_sales_master_id==SalesMasterSA.pk_bint_id)\
                                .filter(PaymentDetailsSA.int_fop==1)\
                                .filter(func.DATE(SalesMasterSA.dat_created) == datetime.datetime.strftime(lst_not_tally_details['dat_time'],"%Y-%m-%d"))\
                                .filter(SalesMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
            rst_payment_amount = session.query(func.sum(func.coalesce(PaymentSA.dbl_amount,0).label('total_amount')))\
                                .filter(func.DATE(PaymentSA.dat_payment) ==  datetime.datetime.strftime(lst_not_tally_details['dat_time'],"%Y-%m-%d"))\
                                .filter(PaymentSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                                .filter(PaymentSA.int_fop == 1,PaymentSA.int_doc_status==0)

            rst_receipt_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                                .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(lst_not_tally_details['dat_time'],'%Y-%m-%d'))\
                                .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                                .filter(ReceiptSA.int_fop == 1,ReceiptSA.fk_sales_return ==None)
            # rst_sales_return_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
            #                     .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(lst_not_tally_details['dat_time'],'%Y-%m-%d'))\
            #                     .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
            #                     .filter(ReceiptSA.int_fop == 1,ReceiptSA.vchr_remarks.ilike('sales return amount'))
            ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
                                                                                        'total_amount',
                                                                                        'json_dayclosure'
                                                                                        ).order_by('-pk_bint_id').first()


            sales_amount = 0
            payment_amount = 0
            receipt_amount = 0
            return_amount=0
            if rst_total_amount.all():
                if rst_total_amount[0][0]:
                    sales_amount = rst_total_amount[0][0]

            if rst_payment_amount.all():
                if rst_payment_amount[0][0]:
                    payment_amount = rst_payment_amount[0][0]

            if rst_receipt_amount.all():
                if rst_receipt_amount[0][0]:
                    receipt_amount = rst_receipt_amount[0][0]
            # if rst_sales_return_amount.all():
            #     if rst_sales_return_amount[0][0]:
            #         return_amount = rst_sales_return_amount[0][0]


            total_amount = 0
            if  ins_last_dayclosure:
                 total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount - return_amount)
            else:
                 total_amount = round(sales_amount + receipt_amount  - payment_amount- return_amount)


            # total_amount = 0
            # if  ins_last_dayclosure:
            #      total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount)
            # else:
            #      total_amount = round(sales_amount + receipt_amount  - payment_amount)

            total_amount = total_amount - lst_not_tally_details['total_amount']

            if total_amount < 0:
                str_closure = "greater"
            else:
                str_closure = "lesser"

            int_not_tally_id = lst_not_tally_details['pk_bint_id']
            vchr_branch_name = lst_not_tally_details['fk_branch__vchr_name']
            dat_time = lst_not_tally_details['dat_time']
            total_amount = total_amount
            branch_id = lst_not_tally_details['fk_branch_id']
            mail_id = ins_mail_details['email']
            str_name = ins_mail_details['first_name'] + " " + ins_mail_details['last_name']

            obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
            ciphertext = obj.encrypt("aprove:"+str(int_not_tally_id))
            encoded_data = binascii.hexlify(ciphertext).decode('ascii')
            str_approve = encoded_data

            obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
            ciphertext = obj.encrypt("reject:"+str(int_not_tally_id))
            encoded_data = binascii.hexlify(ciphertext).decode('ascii')
            str_reject = encoded_data


            HOSTNAME = settings.HOSTNAME

            html_content = '''Dear '''+str(str_name).title()+''',<br>'''
            html_content += '''<br>'''+str(vchr_branch_name).title()+''', day closure is not closed on '''+ str(datetime.datetime.strftime(dat_time,"%d-%m-%Y"))+''' with '''+str(abs(total_amount))+''' amount '''+str(str_closure)+''' than the sales'''
            approveurl = HOSTNAME+"/dayclosure/approve_mail/"+str_approve
            rejecturl = HOSTNAME+"/dayclosure/approve_mail/"+str_reject
            html_content = html_content +  '''<br><button style="border:none; cursor: pointer; font-weight: 600;background:#1e8dcc;padding: 5px 10PX;border-radius: 5px;margin-top:8px;margin-right:10px;"><a style="color: #fff;text-decoration: none;" target ='_blank' href="'''+approveurl+'''">Approve</a>
            </button>
             <button style="border:none; cursor: pointer; font-weight: 600;background: #d64747;padding: 5px 10px;border-radius: 5px;margin-top:8px;"><a style="color: #fff;text-decoration: none;" target ='_blank' href="'''+rejecturl+'''">Reject</a></button>'''

            """mail"""
            to = [mail_id]
            #import pdb;pdb.set_trace()
            #to=['nikhil@travidux.com']
            server = smtplib.SMTP('smtp.pepipost.com', 587)
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("shafeer","Tdx@9846100662")
            # server.login("mygoal@myg.in","mygoal@2019")
            msg = MIMEMultipart()
            msg['Subject'] = "Day Closure Closed not properly"
            msg['To']=to[0]
            msgAlternative = MIMEMultipart('alternative')
            msg.attach(msgAlternative)

            str_html = """<b> <i></i></b><br>"""+html_content+"""<br>"""

            msgText = MIMEText(str_html, 'html')
            msgAlternative.attach(msgText)

            # msgImage = MIMEApplication(open(filename, "rb").read(), _subtype="txt")
            # # fp.close()
            # msgImage.add_header('Content-Disposition','attachment', filename=filename)
            # msg.attach(msgImage)
            server.sendmail("info@enquirytrack.com", to, msg.as_string())
            # server.sendmail("mygoal@myg.in",to,msg.as_string())
            server.quit()
            # remove(filename)


            ins_update = DayClosureDetails.objects.filter(pk_bint_id = day_closure_id).update(int_closed = 3)

            ins_dayclosure_not_tally = DayClosureNotTally()
            ins_dayclosure_not_tally.fk_day_closure_details_id = day_closure_id
            ins_dayclosure_not_tally.fk_staff_id = request.user.id
            ins_dayclosure_not_tally.int_status = 1
            ins_dayclosure_not_tally.total_amount = lst_not_tally_details['total_amount']
            ins_dayclosure_not_tally.json_dayclosure = json.dumps(lst_not_tally_details['json_dayclosure'])
            ins_dayclosure_not_tally.fk_branch_id = request.user.userdetails.fk_branch_id
            ins_dayclosure_not_tally.fk_approve_id = ins_mail_details['user_ptr_id']
            ins_dayclosure_not_tally.save()

            session.close()
            return Response({'status':1})
        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})


class ApproveMail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, hash=None):
        """Approve/Reject day Closure through mail"""
        try:
            with transaction.atomic():
                session=Session()
                if hash:
                    # import pdb; pdb.set_trace()
                    obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
                    encoded_data = hash.encode('ascii')
                    decoded_data = binascii.unhexlify(encoded_data)
                    str_key = obj.decrypt(decoded_data).decode('ascii')
                    str_check = str(str_key[:6])
                    int_details_id = int(str_key[7:])

                    ins_approve = 0
                    ins_approve_tally = 0
                    ins_reject_tally = 0

                    if str_check == "aprove":
                        ins_approve = DayClosureDetails.objects.filter(pk_bint_id = int_details_id).update(int_closed = 1)
                        int_not_tally_id = DayClosureNotTally.objects.filter(fk_day_closure_details_id = int_details_id).order_by('-pk_bint_id').values('pk_bint_id').first()['pk_bint_id']
                        ins_approve_tally = DayClosureNotTally.objects.filter(pk_bint_id = int_not_tally_id).update(dat_time = datetime.datetime.now(), int_status = 3)

                        rst_verify_details = session.query(DayClosureNotTallySA.json_dayclosure.label('json_data'),\
                                                            DayClosureNotTallySA.total_amount.label('total_amount'),\
                                                            DayClosureNotTallySA.fk_staff_id.label('fk_staff_id'),\
                                                            DayClosureNotTallySA.fk_branch_id.label('fk_branch_id'))\
                                                        .filter(DayClosureNotTallySA.pk_bint_id == int_not_tally_id).first()._asdict()

                        ins_dayclosure_details = DayClosureDetails()
                        ins_dayclosure_details.fk_staff_id = rst_verify_details['fk_staff_id']
                        ins_dayclosure_details.dat_time = datetime.datetime.now()
                        ins_dayclosure_details.total_amount = rst_verify_details['total_amount']
                        ins_dayclosure_details.int_closed = 0
                        ins_dayclosure_details.json_dayclosure = json.dumps(rst_verify_details['json_data'])
                        ins_dayclosure_details.fk_branch_id = rst_verify_details['fk_branch_id']
                        ins_dayclosure_details.save()

                    elif str_check == "reject":
                        ins_reject = DayClosureDetails.objects.filter(pk_bint_id = int_details_id).update(int_closed = 4)
                        int_not_tally_id = DayClosureNotTally.objects.filter(fk_day_closure_details_id = int_details_id).order_by('-pk_bint_id').values('pk_bint_id').first()['pk_bint_id']
                        ins_reject_tally = DayClosureNotTally.objects.filter(pk_bint_id = int_not_tally_id).update(dat_time = datetime.datetime.now(),int_status = 4)

                    if ins_approve and ins_approve_tally:
                        vchr_statusmsg = 'approved'
                    elif ins_reject_tally:
                        vchr_statusmsg = 'rejected'
                    else:
                        session.close()
                        return render(request,template_name = 'error.html')
                    session.close()
                    return render(request,template_name = 'success.html')
                else:
                    session.close()
                    return render(request,template_name = 'invalid.html')
        except Exception as e:
            session.close()
            return JsonResponse({'error':'error'})


class ListDayClosure(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """List day closure"""
        try:

            date_from = request.data.get('datFrom')
            date_to = request.data.get('datTo')
            session=Session()
            # import pdb; pdb.set_trace()
            rst_dayclosure_details = session.query(DayClosureDetailsSA.pk_bint_id.label('id'),\
                                                    # func.DATE(DayClosureDetailsSA.dat_time).label('dat'),\
                                                    DayClosureDetailsSA.dat_time.label('dat'),\
                                                    DayClosureDetailsSA.total_amount.label('total_amount'),\
                                                    DayClosureDetailsSA.int_closed.label('int_status'),\
                                                    DayClosureDetailsSA.fk_staff_id.label('staff_id'),\
                                                    DayClosureDetailsSA.fk_branch_id.label('branch_id'),\
                                                    DayClosureDetailsSA.json_dayclosure.label('json_data'),\
                                                    func.concat(AuthUserSA.first_name+' '+AuthUserSA.last_name).label('staff_name'),\
                                                    BranchSA.vchr_name.label('branch_name'))\
                                                    .join(BranchSA,BranchSA.pk_bint_id == DayClosureDetailsSA.fk_branch_id)\
                                                    .join(UserdetailsSA,UserdetailsSA.user_ptr_id == DayClosureDetailsSA.fk_staff_id)\
                                                    .join(AuthUserSA,AuthUserSA.id == UserdetailsSA.user_ptr_id)\
                                                    .filter(DayClosureDetailsSA.int_closed.in_([2,3,4]))\
                                                    .filter(func.DATE(DayClosureDetailsSA.dat_time) >= datetime.datetime.strptime(date_from,'%Y-%m-%d'))\
                                                    .filter(func.DATE(DayClosureDetailsSA.dat_time) <= datetime.datetime.strptime(date_to,'%Y-%m-%d'))\
                                                    .order_by(DayClosureDetailsSA.pk_bint_id.desc())

            lst_details =[]
            if request.user.userdetails.fk_group.vchr_name in ['ho','HO','admin','ADMIN']:
                pass
            else:
                rst_dayclosure_details=rst_dayclosure_details.filter(DayClosureDetailsSA.fk_branch_id==request.user.userdetails.fk_branch_id)
            for ins_details in rst_dayclosure_details.all():
                dct_details = {}
                ins_details = ins_details._asdict()
                dct_details['id'] = ins_details['id']
                dct_details['dat_time'] = datetime.datetime.strftime(ins_details['dat'],"%d-%m-%Y")
                dct_details['time'] = datetime.datetime.strftime(ins_details['dat'],'%H:%M %p')
                dct_details['staff_id'] = ins_details['staff_id']
                dct_details['staff_name'] = ins_details['staff_name']
                dct_details['json_data'] = ins_details['json_data']
                dct_details['branch_name'] = ins_details['branch_name']
                dct_details['int_status'] = ins_details['int_status']
                dct_details['total_amount'] = ins_details['total_amount']

                # rst_total_amount = session.query(func.sum(func.coalesce(SalesMasterSA.dbl_total_amt,0).label('total_amount')))\
                #                                 .filter(func.DATE(SalesMasterSA.dat_invoice) == ins_details['dat'])\
                #                                 .filter(SalesMasterSA.fk_branch_id == ins_details['branch_id'])
                rst_total_amount =session.query(func.sum(func.coalesce(PaymentDetailsSA.dbl_receved_amt,0).label('total_amount')))\
                                    .join(SalesMasterSA,PaymentDetailsSA.fk_sales_master_id==SalesMasterSA.pk_bint_id)\
                                    .filter(PaymentDetailsSA.int_fop==1)\
                                    .filter(func.DATE(SalesMasterSA.dat_created) == datetime.datetime.strftime(ins_details['dat'] ,"%Y-%m-%d"))\
                                    .filter(SalesMasterSA.fk_branch_id == ins_details['branch_id'])
                rst_payment_amount = session.query(func.sum(func.coalesce(PaymentSA.dbl_amount,0).label('total_amount')))\
                                    .filter(func.DATE(PaymentSA.dat_payment) == datetime.datetime.strftime(ins_details['dat'] ,"%Y-%m-%d"))\
                                    .filter(PaymentSA.fk_branch_id == ins_details['branch_id'])\
                                    .filter(PaymentSA.int_fop == 1,PaymentSA.int_doc_status==0)

                rst_receipt_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                                    .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(ins_details['dat'],'%Y-%m-%d'))\
                                    .filter(ReceiptSA.fk_branch_id == ins_details['branch_id'])\
                                    .filter(ReceiptSA.int_fop == 1,ReceiptSA.fk_sales_return ==None)
                                    # .filter(ReceiptSA.int_fop == 1,~ReceiptSA.vchr_remarks.ilike('sales return amount'))

                # rst_sales_return_amount = session.query(func.sum(func.coalesce(ReceiptSA.dbl_amount,0).label('total_amount')))\
                #                     .filter(func.DATE(ReceiptSA.dat_issue) == datetime.datetime.strftime(ins_details['dat'],'%Y-%m-%d'))\
                #                     .filter(ReceiptSA.fk_branch_id == request.user.userdetails.fk_branch_id)\
                #                     .filter(ReceiptSA.int_fop == 1,ReceiptSA.vchr_remarks.ilike('sales return amount'))
                ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=ins_details['branch_id']).values('dat_time',
                                                                                            'total_amount',
                                                                                            'json_dayclosure'
                                                                                            ).order_by('-pk_bint_id').first()

                sales_amount = 0
                payment_amount = 0
                receipt_amount = 0
                return_amount=0
                if rst_total_amount.all():
                    if rst_total_amount[0][0]:
                        sales_amount = rst_total_amount[0][0]

                if rst_payment_amount.all():
                    if rst_payment_amount[0][0]:
                        payment_amount = rst_payment_amount[0][0]

                if rst_receipt_amount.all():
                    if rst_receipt_amount[0][0]:
                        receipt_amount = rst_receipt_amount[0][0]

                # if rst_sales_return_amount.all():
                #     if rst_sales_return_amount[0][0]:
                #         return_amount = rst_sales_return_amount[0][0]


                total_amount = 0
                if ins_last_dayclosure:
                    total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount)

                    # total_amount = round(ins_last_dayclosure.get('total_amount')+sales_amount + receipt_amount  - payment_amount - return_amount)
                else:
                    total_amount = round(sales_amount + receipt_amount  - payment_amount)

                    # total_amount = round(sales_amount + receipt_amount  - payment_amount -return_amount)

                dct_details['amount_status'] = total_amount - ins_details['total_amount']

                lst_details.append(dct_details)


            session.close()
            return Response({'status':1 , 'data':lst_details})
        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})


    def put(self, request):
        """approve day closure that is not clossed from UI"""
        try:
            # import pdb; pdb.set_trace()
            if request.data.get('id'):
                int_details_id = request.data.get('id')
                str_check = request.data.get('check')
                with transaction.atomic():
                    session=Session()
                    if str_check == "approve":
                        ins_approve = DayClosureDetails.objects.filter(pk_bint_id = int_details_id).update(int_closed = 1)
                        int_not_tally_id = DayClosureNotTally.objects.filter(fk_day_closure_details_id = int_details_id).order_by('-pk_bint_id').values('pk_bint_id').first()['pk_bint_id']
                        ins_approve_tally = DayClosureNotTally.objects.filter(pk_bint_id = int_not_tally_id).update(dat_time = datetime.datetime.now(), int_status = 3, fk_approve_id = request.user.id)

                        rst_verify_details = session.query(DayClosureNotTallySA.json_dayclosure.label('json_data'),\
                                                            DayClosureNotTallySA.total_amount.label('total_amount'),\
                                                            DayClosureNotTallySA.fk_staff_id.label('fk_staff_id'),\
                                                            DayClosureNotTallySA.fk_branch_id.label('fk_branch_id'))\
                                                        .filter(DayClosureNotTallySA.pk_bint_id == int_not_tally_id).first()._asdict()

                        ins_dayclosure_details = DayClosureDetails()
                        ins_dayclosure_details.fk_staff_id = rst_verify_details['fk_staff_id']
                        ins_dayclosure_details.dat_time = datetime.datetime.now()
                        ins_dayclosure_details.total_amount = rst_verify_details['total_amount']
                        ins_dayclosure_details.int_closed = 0
                        ins_dayclosure_details.json_dayclosure = json.dumps(rst_verify_details['json_data'])
                        ins_dayclosure_details.fk_branch_id = rst_verify_details['fk_branch_id']
                        ins_dayclosure_details.save()


                    elif str_check == "reject":
                        ins_reject = DayClosureDetails.objects.filter(pk_bint_id = int_details_id).update(int_closed = 4)
                        int_not_tally_id = DayClosureNotTally.objects.filter(fk_day_closure_details_id = int_details_id).order_by('-pk_bint_id').values('pk_bint_id').first()['pk_bint_id']
                        ins_reject_tally = DayClosureNotTally.objects.filter(pk_bint_id = int_not_tally_id).update(dat_time = datetime.datetime.now(), int_status = 4, fk_approve_id = request.user.id)

            session.close()
            return Response({'status':1 , 'data':"success"})
        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})

class DayClosureReport(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            dat_to = request.data.get("datTo")  if request.data.get("datTo") else None
            dat_from = request.data.get("datFrom")  if request.data.get("datFrom") else None
            int_branch = request.data.get("intBranchId")
            ins_closure = DayClosureDetails.objects.filter(fk_branch_id = int_branch,int_closed = 1).annotate(fullname=Concat('fk_staff__first_name', Value(' '), 'fk_staff__last_name')).values('dat_time','fk_branch__vchr_name','fullname','total_amount')
            if dat_to and dat_from:
                ins_closure =  ins_closure.filter(dat_time__date__gte = dat_from,dat_time__date__lte = dat_to)
            lst_data = []
            for data in ins_closure:
                dct_data = {}
                if data['dat_time']:
                    dct_data['date'] =  datetime.datetime.strftime(data['dat_time'],'%d-%m-%Y')
                    ins_first = SalesMaster.objects.filter(fk_branch_id = int_branch,dat_invoice = data['dat_time']).values('dat_created').first()
                    ins_last = SalesMaster.objects.filter(fk_branch_id = int_branch,dat_invoice = data['dat_time']).values('dat_created').last()
                    if ins_first:
                        dct_data['timeFirst'] =  datetime.datetime.strftime(ins_first['dat_created'],'%I:%M %p')
                        dct_data['timeLast'] = datetime.datetime.strftime(ins_last['dat_created'],'%I:%M %p')
                    dct_data['time'] = datetime.datetime.strftime(data['dat_time'],'%I:%M %p')
                dct_data['strClosedEmp'] =(data['fullname']).title()
                dct_data['strBranch'] = data['fk_branch__vchr_name']
                dct_data['intTotal'] = data['total_amount']
                lst_data.append(dct_data)
            return Response({'status':1,'data':lst_data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','reason':str(e),'message':'Something went wrong'})
