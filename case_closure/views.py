
# Create your views here.
from datetime import datetime,date, timedelta
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from sqlalchemy import and_,func ,cast,DATE,case,distinct,Date,Time
from sqlalchemy.orm import sessionmaker,aliased
from django.http import JsonResponse
from django.conf import settings
import json

from .models import CaseClosureMaster,CaseClosureDetails
from day_closure.models import DayClosureDetails
from invoice.models import SalesMaster,SalesDetails
from branch.models import Branch
from userdetails.models import UserDetails as Userdetails
from django.contrib.auth.models import User as AuthUser
from payment.models import Payment
from receipt.models import Receipt
from invoice.models import PaymentDetails

from django.db.models.functions import TruncDay
from django.db.models import Sum


CaseClosureMasterSA = CaseClosureMaster.sa
CaseClosureDetailsSA = CaseClosureDetails.sa
SalesMasterSA = SalesMaster.sa
SalesDetailsSA = SalesDetails.sa
BranchSA = Branch.sa
AuthUserSA = AuthUser.sa
UserdetailsSA = Userdetails.sa

PaymentSA = Payment.sa
ReceiptSA = Receipt.sa


def Session():
    from aldjemy.core import get_engine
    engine=get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()

class CaseClosureNotification(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            if request.GET.get('bln_preload'):
                bln_preload=False
            else:
                bln_preload=True
            lst_notes = list(CaseClosureMaster.objects.values('pk_bint_id','vchr_name'))

            #=================================================================
            # ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id,dat_time__startswith=(datetime.today() - timedelta(days=1)).date()).values('dat_time',
            #                                                                             'total_amount',
            #                                                                             'json_dayclosure'
            #                                                                             ).order_by('-pk_bint_id').first()
            #
            # if ins_last_dayclosure:
            #     dct_data = {}
            #     dct_data['dat_created'] = ins_last_dayclosure['dat_time']
            #     dct_data['dbl_case_closure'] = ins_last_dayclosure['total_amount']
            #     dct_data['json_data'] = ins_last_dayclosure['json_dayclosure']
            #     return Response({'status':2, 'data' : 'Caseclosure closed. Showing last day_closure data','dct_data' : dct_data,'lst_notes':lst_notes,'bln_preload':bln_preload})






            ins_closure_last_closed = CaseClosureDetails.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_created__startswith=datetime.now().date()).values('pk_bint_id','dat_created','dbl_total_amount','json_case_closure','int_status','vchr_remark').order_by('-pk_bint_id').first()

            if ins_closure_last_closed :
                # if datetime.strftime(ins_closure_last_closed['dat_created'],'%Y-%m-%d') !=  (datetime.strftime(date.today(),'%Y-%m-%d')):
                #     ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
                #                                                                                 'total_amount',
                #                                                                                 'json_dayclosure'
                #                                                                                 ).order_by('-pk_bint_id').first()
                #     if ins_last_dayclosure:
                #         dct_data = {}
                #         dct_data['dat_created'] = ins_last_dayclosure['dat_time']
                #         dct_data['dbl_case_closure'] = ins_last_dayclosure['total_amount']
                #         dct_data['json_data'] = ins_last_dayclosure['json_dayclosure']
                #
                #         return Response({'status':2, 'data' : 'Caseclosure closed. Showing last day_closure data','dct_data' : dct_data,'lst_notes':lst_notes,'bln_preload':bln_preload})
                #


                dct_data = {}
                dct_data['int_id'] = ins_closure_last_closed['pk_bint_id']
                dct_data['int_status'] = ins_closure_last_closed['int_status']
                dct_data['dbl_case_closure'] = ins_closure_last_closed['dbl_total_amount']
                dct_data['json_data'] = ins_closure_last_closed['json_case_closure']
                dct_data['str_remarks'] =ins_closure_last_closed['vchr_remark']
                dct_data['dat_created'] = ins_closure_last_closed['dat_created']


                return Response({'status':1, 'dct_data' : dct_data,'lst_notes':lst_notes,'bln_preload':bln_preload})

            return Response({'status':0,'lst_notes':lst_notes})
        except Exception as e:
            return Response({'status':'failed','data':str(e)})



            #------------------------------------------------------------



            #
            # ins_closure_last_closed = CaseClosureDetails.objects.filter(int_status = 0).values('pk_bint_id','dat_created','dbl_total_amount','json_case_closure','int_status','vchr_remark').order_by('-pk_bint_id').first()
            #





        #     if ins_closure_last_closed :
        #
        #         if datetime.strftime(ins_closure_last_closed['dat_created'],'%Y-%m-%d') !=  (datetime.strftime(date.today(),'%Y-%m-%d')):
        #             ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1).values('dat_time',
        #                                                                                         'total_amount',
        #                                                                                         'json_dayclosure'
        #                                                                                         ).order_by('-pk_bint_id').first()
        #             if ins_last_dayclosure:
        #                 dct_data = {}
        #                 dct_data['dat_created'] = ins_last_dayclosure['dat_time']
        #                 dct_data['dbl_case_closure'] = ins_last_dayclosure['total_amount']
        #                 dct_data['json_data'] = ins_last_dayclosure['json_dayclosure']
        #
        #                 return Response({'status':2, 'data' : 'Caseclosure closed. Showing last day_closure data','dct_data' : dct_data,'lst_notes':lst_notes})
        #             else:
        #                 return Response({'status':0, 'data' : 'No Data','lst_notes':lst_notes})
        #
        #         dct_data = {}
        #         dct_data['int_id'] = ins_closure_last_closed['pk_bint_id']
        #         dct_data['int_status'] = ins_closure_last_closed['int_status']
        #         dct_data['dbl_case_closure'] = ins_closure_last_closed['dbl_total_amount']
        #         dct_data['json_data'] = ins_closure_last_closed['json_case_closure']
        #         dct_data['str_remarks'] =ins_closure_last_closed['vchr_remark']
        #         dct_data['dat_created'] = ins_closure_last_closed['dat_created']
        #
        #
        #         return Response({'status':1, 'dct_data' : dct_data,'lst_notes':lst_notes})
        #     else:
        #         return Response({'status':0,'lst_notes':lst_notes})
        # except Exception as e:
        #     return Response({'status':'failed','data':str(e)})
        #


    # def post(self,request):
    #     try:
    #         """verify last case_closure"""
    #
    #         if request.data.get('check_verify') == 'confirm':
    #
    #
    #             ins_caseclosure_confirm = CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).values('dbl_total_amount',
    #                                                                                                                     'json_case_closure',
    #                                                                                                                     'vchr_remark')
    #
    #             # ins_caseclosure_open = CaseClosureDetails.objects.create(fk_created_id = request.user.id,
    #             #                                                         dat_created = datetime.now(),
    #             #                                                         dbl_total_amount = ins_caseclosure_confirm.first()['dbl_total_amount'],
    #             #                                                         int_status = 0,
    #             #                                                         json_case_closure = json.dumps(ins_caseclosure_confirm.first()['json_case_closure']),
    #             #                                                         fk_branch_id = request.user.userdetails.fk_branch_id,
    #             #                                                         vchr_remark = ins_caseclosure_confirm.first()['vchr_remark'] or "" )
    #
    #
    #             CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update(
    #                                                                             fk_updated_id =  request.user.id,
    #                                                                             dat_updated = datetime.now(),
    #                                                                             int_status = 2
    #                                                                                 )
    #
    #         elif request.data.get('check_verify') == 'modified':
    #
    #             ins_caseclosure_deny = CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).values('dbl_total_amount',
    #                                                                                                                     'json_case_closure',
    #                                                                                                                     'vchr_remark')
    #             ins_caseclosure_open = CaseClosureDetails.objects.create(fk_created_id = request.user.id,
    #                                                                     dat_created = datetime.now(),
    #                                                                     dbl_total_amount = request.data.get('grandTot'),
    #                                                                     int_status = 2,
    #                                                                     json_case_closure = json.dumps(request.data.get('lstData')),
    #                                                                     fk_branch_id = request.user.userdetails.fk_branch_id)
    #
    #             CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update (
    #                                                                                     fk_updated_id =  request.user.id,
    #                                                                                     dat_updated = datetime.now(),
    #                                                                                     int_status = 3,
    #                                                                                     vchr_remark =  request.data.get('str_remarks'))
    #
    #
    #         return Response({'status':1})
    #     except Exception as e:
    #         return Response({'status':'failed','data':str(e)})



class CaseClosureAdd(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
           # ins_caseclosure_closed = CaseClosureDetails.objects.filter(fk_created_id = request.user.id,int_status = 1,dat_updated__date =  date.today())
            #
            # if ins_caseclosure_closed:
            #     ins_caseclosure_closed_id = ins_caseclosure_closed.order_by('-pk_bint_id').values('pk_bint_id').first()['pk_bint_id']
            #
            #     ins_caseclosure_closed.filter(pk_bint_id = ins_caseclosure_closed_id).update(
                                                                                    # fk_updated_id =  request.user.id,
                                                                                    # dat_updated = datetime.now(),
                                                                                    # int_status = 2,
                                                                                    # dbl_total_amount = request.data.get('grandTot'),
                                                                                    # json_case_closure = json.dumps(request.data.get('lstData')),
                                                                                    # vchr_remark =  request.data.get('str_remarks'))
            if request.data.get('check_verify')=='verified' and not request.data.get('bln_preload'):
                CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update(
                                                                                fk_updated_id =  request.user.id,
                                                                                dat_updated = datetime.now(),
                                                                                int_status = 2
                                                                                    )
            else:
                if request.data.get('check_verify')=='modified' and not request.data.get('bln_preload'):
                    ins_case_closure=CaseClosureDetails.objects.filter(dat_created__startswith=datetime.now().date(),fk_branch_id=request.user.userdetails.fk_branch_id,int_status=2).exclude(pk_bint_id=request.data.get('id')).last()
                else:
                    ins_case_closure=CaseClosureDetails.objects.filter(dat_created__startswith=datetime.now().date(),fk_branch_id=request.user.userdetails.fk_branch_id,int_status = 2).last()

                total_amount = 0
                dat_now=datetime.strftime(datetime.now(),'%Y-%m-%d')

                if ins_case_closure:
                    int_payment_amt=Payment.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_created__gte=ins_case_closure.dat_created,int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    # int_sales_amt=SalesDetails.objects.filter(fk_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_master__dat_created__startswith=datetime.now().date()).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    int_sales_amt=PaymentDetails.objects.filter(int_fop=1,fk_sales_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_sales_master__dat_created__gte=ins_case_closure.dat_created).aggregate(Sum('dbl_receved_amt')).get('dbl_receved_amt__sum') or 0

                    int_receipt_amt=Receipt.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_issue__gte=ins_case_closure.dat_created,int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    int_case_closure_amt=ins_case_closure.dbl_total_amount
                    total_amount=int_sales_amt+int_receipt_amt+int_case_closure_amt-int_payment_amt
                else:
                    int_payment_amt=Payment.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_created__startswith=datetime.now().date(),int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    # int_sales_amt=SalesDetails.objects.filter(fk_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_master__dat_created__startswith=datetime.now().date()).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    int_sales_amt=PaymentDetails.objects.filter(int_fop=1,fk_sales_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_sales_master__dat_created__startswith=datetime.now().date()).aggregate(Sum('dbl_receved_amt')).get('dbl_receved_amt__sum') or 0

                    int_receipt_amt=Receipt.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_issue__startswith=datetime.now().date(),int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0

                    # int_payment_amt=Payment.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_created__startswith=datetime.now().date(),dat_created__lte=datetime.now(),int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    # # int_sales_amt=SalesDetails.objects.filter(fk_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_master__dat_created__startswith=datetime.now().date(),fk_master__dat_created__lte=datetime.now()).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    # int_sales_amt=PaymentDetails.objects.filter(int_fop=1,fk_sales_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_sales_master__dat_created__gte=ins_case_closure.dat_created).aggregate(Sum('dbl_receved_amt')).get('dbl_receved_amt__sum') or 0
                    #
                    # int_receipt_amt=Receipt.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_issue__startswith=datetime.now().date(),dat_issue__lte=datetime.now(),int_fop = 1).aggregate(Sum('dbl_amount')).get('dbl_amount__sum') or 0
                    ins_last_dayclosure = DayClosureDetails.objects.filter(int_closed = 1,fk_branch_id=request.user.userdetails.fk_branch_id).values('dat_time',
                                                                                                'total_amount',
                                                                                                'json_dayclosure'
                                                                                                ).order_by('-pk_bint_id').first()
                    if ins_last_dayclosure:

                        total_amount = round((ins_last_dayclosure.get('total_amount') or 0)+int_sales_amt + int_receipt_amt  - int_payment_amt)
                    else:
                        total_amount = int_sales_amt + int_receipt_amt  - int_payment_amt


                amount =  total_amount - request.data.get('grandTot')
                if request.data.get('bln_preload') or not request.data.get('id'):
                    ins_caseclosure_pending =  CaseClosureDetails.objects.create(
                                                                                fk_created_id = request.user.id,
                                                                                dat_created = datetime.now(),
                                                                                dbl_total_amount = request.data.get('grandTot'),
                                                                                int_status = 1,
                                                                                json_case_closure = json.dumps(request.data.get('lstData')),
                                                                                fk_branch_id = request.user.userdetails.fk_branch_id,
                                                                                vchr_remark =  request.data.get('str_remarks'),
                                                                                amount_status=amount)

                else:
                    ins_caseclosure_pending = CaseClosureDetails.objects.create(fk_created_id = request.user.id,
                                                                            dat_created = datetime.now(),
                                                                            dbl_total_amount = request.data.get('grandTot'),
                                                                            int_status = 1,
                                                                            json_case_closure = json.dumps(request.data.get('lstData')),
                                                                            fk_branch_id = request.user.userdetails.fk_branch_id,
                                                                            amount_status=amount,
                                                                            vchr_remark =  request.data.get('str_remarks'))
                    CaseClosureDetails.objects.filter(pk_bint_id = request.data.get('id')).update (
                                                                                            fk_updated_id =  request.user.id,
                                                                                            dat_updated = datetime.now(),
                                                                                            int_status = 3,
                                                                                            vchr_remark =  request.data.get('str_remarks'))

                if amount!=0:

                    return Response({'status':2,'dct_data':{'amount':amount}})
                else:
                        ins_caseclosure_pending.int_status=2
                        ins_caseclosure_pending.save()

            return Response({'status':1})

        except Exception as e:
            return Response({'status':0,'data':str(e)})


class CaseClosureList(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """List day closure"""
        try:
            date_from = request.data.get('datFrom')
            date_to = request.data.get('datTo')
            session=Session()
            rst_dayclosure_details = CaseClosureDetails.objects.filter(int_status=2,dat_created__date__lte  = date_to,fk_branch_id=request.user.userdetails.fk_branch_id,dat_created__date__gte = date_from ).extra(select ={'dat_created_new' :"to_char(case_closure_details.dat_created,'DD/MM/YYYY')",'dat_updated_new' :"to_char(case_closure_details.dat_updated,'DD/MM/YYYY')"}).values('pk_bint_id','dat_created','dat_created_new','dat_updated_new','dat_updated','dbl_total_amount',
                                                                                'json_case_closure','vchr_remark',
                                                                                'fk_created__first_name','int_status',
                                                                                'fk_created__last_name',
                                                                                'fk_updated__first_name',
                                                                                'fk_updated__last_name',
                                                                                'fk_branch__vchr_name','amount_status').order_by('-dat_created')
            if rst_dayclosure_details :
                if date_to:
                    rst_dayclosure_details = rst_dayclosure_details

                # if vchr_status == 'confirmed':
                #     rst_dayclosure_details = rst_dayclosure_details.filter(int_status = 1)
                #
                # elif vchr_status == 'confirmed':
                #     rst_dayclosure_details = rst_dayclosure_details.filter(int_status = 2)
                rst_dayclosure_details=list(rst_dayclosure_details)
                # ins_payment=Payment.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_payment__lte  = date_to,dat_payment__gte = date_from,int_fop = 1)
                # ins_sales=SalesDetails.objects.filter(fk_master__fk_branch_id=request.user.userdetails.fk_branch_id,fk_master__dat_invoice__lte  = date_to,fk_master__dat_invoice__gte = date_from)
                # ins_receipt=Receipt.objects.filter(fk_branch_id=request.user.userdetails.fk_branch_id,dat_issue=datetime.now().date(),int_fop = 1,dat_issue__lte  = date_to,dat_issue__gte = date_from)
                # sum_prev_payment=0
                # sum_prev_sales=0
                # sum_prev_receipt=0
                #
                # for data in rst_dayclosure_details:
                #     sum_now_payment = 0
                #     sum_now_sales = 0
                #     sum_now_receipt= 0
                #     if ins_payment.filter(dat_payment__lte=data['dat_created']).exists():
                #         sum_now_payment=(ins_payment.filter(dat_payment__lte=data['dat_created']).aggregate(Sum('dbl_amount'))).get('dbl_amount__sum')
                #     if ins_sales.filter(fk_master__dat_invoice__lte=data['dat_created']).exists():
                #         sum_now_sales=(ins_sales.filter(fk_master__dat_invoice__lte=data['dat_created']).aggregate(Sum('dbl_amount'))).get('dbl_amount__sum')
                #     if ins_receipt.filter(dat_issue__lte=data['dat_created']).exists():
                #         sum_now_receipt=(ins_receipt.filter(dat_issue__lte=data['dat_created']).aggregate(Sum('dbl_amount'))).get('dbl_amount__sum')
                #
                #     payment_amount=sum_now_payment-sum_prev_payment
                #     sales_amount=sum_now_sales-sum_prev_sales
                #     receipt_amount=sum_now_receipt-sum_prev_receipt
                #
                #     sum_prev_payment = sum_now_payment
                #     sum_prev_sales = sum_now_sales
                #     sum_prev_receipt = sum_now_payment
                #
                #
                #
                #     total_amount = 0
                #
                #     total_amount = round(sales_amount + receipt_amount  - payment_amount)
                #
                #     amount =  total_amount - data['dbl_total_amount']
                #     data['amount_status']= amount
                session.close()
                return Response({'status':1,'lst_dayclosure_details':rst_dayclosure_details})
            session.close()
            return Response({'status':0})


        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})
