from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from datetime import datetime,timedelta,date

from branch_stock.models import BranchStockMaster,BranchStockDetails,BranchStockImeiDetails,NonSaleable
from internal_stock.models import StockTransfer,IstDetails,StockTransferImeiDetails,TransferHistory
from customer.models import CustomerDetails
from purchase.models import GrnDetails
from item_category.models import Item,TaxMaster,ItemCategory

from invoice.models import  SalesMaster, SalesDetails,GDPRange,PartialInvoice
from sales_return.models import SalesReturn

from POS import ins_logger
from django.db.models import FloatField, F,CharField, IntegerField, Case, Value, When,Sum
from operator import itemgetter
from django.contrib.postgres.fields import JSONField
from django.db.models import Value as V, DurationField
from django.db.models.expressions import CombinedExpression
from purchase.models import GrnDetails,GrnrDetails
from django.db import transaction
from POS import ins_logger
import sys, os
from django.db.models import Q
import json
from django.conf import settings
# ============================================
from branch.models import Branch
# ============================================
import itertools
import traceback
from django.http import JsonResponse

from sqlalchemy.orm.session import sessionmaker
from aldjemy.core import get_engine
from collections import OrderedDict
########################################
from OXYGEN_API.imei_available_check import Stock_Item_Checking
from sqlalchemy import and_,func ,cast,Date,case, literal_column,or_,MetaData,desc
Connection = sessionmaker()
engine = get_engine()
Connection.configure(bind=engine)


ItemsSA = Item.sa
IstDetailsSA = IstDetails.sa
BranchStockDetailsSA = BranchStockDetails.sa
StockTransferSA = StockTransfer.sa

########################################


def Session():
    _Session = sessionmaker(bind = engine)
    return _Session()


class BranchStockAPI(APIView):
    """
        Add Details to branch Stock and update int_status as 1(received) in Stock transfer
        param : int_stock_transfer_id,item Details
        return : Success
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            with transaction.atomic():
                int_stock_transfer_id = request.data.get('int_transfer_id')
                lst_item = request.data.get('lst_data')

                dct_item = request.data.get('dct_imei_data')  # {item_id:{imei_no:{'avl':true,'dmg':false}}}
                dct_batch = request.data.get('dct_batch_data') # {item_id:{batch_no:{'status':true/false,'qty':0}}}

                dct_dbl_tax = {}
                dct_dbl_tax['CGST'] = 0
                dct_dbl_tax['SGST'] = 0
                dct_dbl_tax['IGST'] = 0
                dbl_total_amount = 0
                dbl_total_tax = 0

                # To get branch id from stock transfer.
                int_branch_id = StockTransfer.objects.filter(pk_bint_id = int_stock_transfer_id).values_list('fk_to',flat =True).first()
                if not int_branch_id == request.user.userdetails.fk_branch_id:
                    return Response({'status':1,'message':'Branch not Match'})
                dat_acknowledge = datetime.now()
                # if BranchStockMaster.objects.filter(fk_transfer_id = int_stock_transfer_id):
                #     return Response({'status':0,'message':'Already Exist'})
                # ----------------------------------------------------------------------------------

                rst_data = StockTransferImeiDetails.objects.filter(fk_details_id__fk_transfer_id=int_stock_transfer_id).values('fk_details_id','jsn_imei','jsn_batch_no','fk_grn_details_id','fk_grn_details__jsn_tax','fk_grn_details__dbl_costprice','fk_grn_details__dbl_tax')
                # ----------------------------------------------------------------------------------
                '''CHECKING WHETHER stock has entered branch stock already'''
                ins_branch_stock_details_already=BranchStockDetails.objects.filter(fk_transfer_details_id__fk_transfer_id=int_stock_transfer_id).first()

                if ins_branch_stock_details_already:
                        return Response({'status':'0','message':'Already added'})

                ins_master = BranchStockMaster(
                                fk_branch_id = int_branch_id,
                                fk_created_id = request.user.id,
                                dat_stock = dat_acknowledge,
                                dbl_tax = dbl_total_tax,
                                dbl_amount = dbl_total_amount,
                                jsn_tax = dct_dbl_tax
                                )
                ins_master.save()

                lst_query_set = []
                for item in lst_item:
                    lst_available = []
                    lst_damaged = []
                    lst_imei = []
                    lst_batch = []
                    int_count = 0
                    int_item_id = item.get('item_id')
                    int_transfer_id  = item.get('int_transfer_details_id')
                    dct_item_imei = dct_item.get(str(int_transfer_id))  # dictionary of IMEIs for  item_id
                    dct_item_batch = dct_batch.get(str(int_transfer_id))  # dictionary of Batch NOs for item_id

                    if dct_item_batch:
                        for ins_batch in dct_item_batch:
                            if (dct_item_batch[ins_batch]['batch']):
                                int_count += dct_item_batch[ins_batch]['qty']
                                lst_batch.append(str(ins_batch))

                    if dct_item_imei:
                        for imei in dct_item_imei:
                            if (dct_item_imei[imei]['avl']):
                                lst_available.append(str(imei))
                            elif(dct_item_imei[imei]['dmg']):
                                lst_damaged.append(str(imei))

                    lst_imei = lst_available + lst_damaged

                    if len(lst_available): # if list of IMEI available then quantity is No of available , else sum of qty in batch
                        int_count = len(lst_available)

                    ins_details = BranchStockDetails(
                                                        fk_item_id = int_item_id ,
                                                        fk_master = ins_master,
                                                        int_qty = int_count,
                                                        int_received = int_count,
                                                        jsn_imei = {"imei":lst_imei},
                                                        jsn_imei_avail = {"imei":lst_available},
                                                        jsn_imei_dmgd = {"imei":lst_damaged},
                                                        jsn_batch_no = {"batch":lst_batch},
                                                        fk_transfer_details_id = item.get('int_transfer_details_id')
                                                    )
                    ins_details.save()
                    item.get('int_transfer_details_id')
    # ---------------------------------------------------------------------------------

                    # Checking available imei's fk_grn_id and added to BranchStockImeiDetails table
                    dct_data = {}
                    int_grn_id = 0
                    for item in rst_data: # All StockTransferImeiDetails data filter by stock_transfer_id
                        if item['fk_details_id'] == ins_details.fk_transfer_details_id :
                            dct_data[item['fk_grn_details_id']]= {}
                            dct_data[item['fk_grn_details_id']]['imei']=[]
                            dct_data[item['fk_grn_details_id']]['batch']=[]
                            if item['fk_grn_details__jsn_tax']:
                                dct_data[item['fk_grn_details_id']]['CGST'] = item['fk_grn_details__jsn_tax'].get('CGST') or 0
                                dct_data[item['fk_grn_details_id']]['SGST'] = item['fk_grn_details__jsn_tax'].get('SGST') or 0
                                dct_data[item['fk_grn_details_id']]['IGST'] = item['fk_grn_details__jsn_tax'].get('IGST') or 0
                            else:
                                dct_data[item['fk_grn_details_id']]['CGST'] = 0
                                dct_data[item['fk_grn_details_id']]['SGST'] = 0
                                dct_data[item['fk_grn_details_id']]['IGST'] = 0

                            dct_data[item['fk_grn_details_id']]['dbl_unitprice'] = item['fk_grn_details__dbl_costprice']
                            dct_data[item['fk_grn_details_id']]['dbl_tax'] = item['fk_grn_details__dbl_tax']

                            if item['jsn_imei']['imei']: # If the item has imei

                                for str_imei in item['jsn_imei']['imei']:
                                    if str_imei in lst_available:
                                        dct_data[item['fk_grn_details_id']]['imei'].append(str_imei) # imei append to dictionary with key of grn_id

                            # else:
                            #     int_grn_id = item['fk_grn_details_id']
                            if item['jsn_batch_no']['batch']:
                                for str_batch in item['jsn_batch_no']['batch']:
                                    if str_batch in lst_batch:
                                        dct_data[item['fk_grn_details_id']]['batch'].append(str_batch)

                    if dct_data:
                        for item in dct_data:

                            if not dct_data[item]['imei'] :
                                int_qty = int_count
                            else:
                                int_qty = len(dct_data[item]['imei'])

                            dct_dbl_tax['CGST'] += (dct_data[item]['CGST'] * int_qty)
                            dct_dbl_tax['SGST'] += (dct_data[item]['SGST'] * int_qty)
                            dct_dbl_tax['IGST'] += (dct_data[item]['IGST'] * int_qty)

                            dbl_total_amount += (dct_data[item]['dbl_unitprice'] * int_qty)
                            if not dct_data[item]['dbl_tax']:
                                dct_data[item]['dbl_tax'] = 0
                            dbl_total_tax += (dct_data[item]['dbl_tax'] * int_qty)


                            ins_imei = BranchStockImeiDetails(
                                                                fk_details = ins_details,
                                                                fk_grn_details_id = item,
                                                                jsn_imei = {"imei":dct_data[item]['imei']},
                                                                jsn_imei_reached = {"imei":dct_data[item]['imei']},
                                                                jsn_batch_no = {"batch":dct_data[item]['batch']},
                                                                jsn_batch_reached = {"batch":dct_data[item]['batch']},
                                                                int_qty = int_qty,
                                                                int_received = int_qty

                                                             )
                            ins_imei.save()

                    # else:
                    #
                    #     dct_dbl_tax['CGST'] += (dct_data[item]['CGST'] * int_qty)
                    #     dct_dbl_tax['SGST'] += (dct_data[item]['SGST'] * int_qty)
                    #     dct_dbl_tax['IGST'] += (dct_data[item]['IGST'] * int_qty)
                    #
                    #     dbl_total_amount += (dct_data[item]['dbl_unitprice'] * int_qty)
                    #     dbl_total_tax += (dct_data[item]['dbl_tax'] * int_qty)
                    #
                    #     ins_imei = BranchStockImeiDetails(
                    #                                             fk_details = ins_details,
                    #                                             fk_grn_details_id = int_grn_id,
                    #                                             jsn_imei = {"imei":[]},
                    #                                             jsn_batch_no = {"batch":lst_batch},
                    #                                             int_qty = int_count
                    #                                          )
                    #     ins_imei.save()
    # ---------------------------------------------------------------------------------

                # rst_amount = BranchStockImeiDetails.objects.filter(fk_details_id__fk_master_id=ins_master.pk_bint_id)\
                #                               .aggregate(tax = Sum(F('fk_grn_details_id__dbl_tax')*F('int_qty'),output_field = FloatField()),\
                #                                          total = Sum(F('fk_grn_details__dbl_costprice') * F('int_qty'),output_field = FloatField())\
                #                                          )

                ins_master.dbl_tax = dbl_total_tax
                ins_master.dbl_amount = dbl_total_amount
                ins_master.jsn_tax = dct_dbl_tax
                ins_master.save()

                # ---------------------------------------------------------------------------------
                if ins_master:
                    st_update = StockTransfer.objects.filter(pk_bint_id = int_stock_transfer_id).update(dat_acknowledge = dat_acknowledge,int_status=3)

                    ins_th_details = TransferHistory(
                                                        vchr_status = 'ACKNOWLEDGED',
                                                        fk_transfer_id = int_stock_transfer_id,
                                                        fk_created_id = request.user.id,
                                                        dat_created = datetime.now(),
                                                        fk_updated_id = request.user.id,
                                                        dat_updated = datetime.now(),
                                                        int_doc_status = 0,
                                                    )
                    ins_th_details.save()
                    if st_update:
                        return Response({'status':1})
                    else:
                        return Response({'status':0,'message':'Failed Branch Stock Add'})
                else:
                    return Response({'status':0,'message':'Failed stock transfer update'})


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})

class ListStockTransfer(APIView):
    """
        List of Transfered Stock in the current branch
        param : From  and To date
        return : int_transfer_id,dat_transfer,vchr_from,int_count
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            lst_data = []
            branch_id = request.user.userdetails.fk_branch_id
            dat_from = request.data.get('datFrom')
            dat_to = request.data.get('datTo')
            rst_data = IstDetails.objects.filter(fk_transfer_id__int_doc_status=0,fk_transfer_id__int_status__in = [2,5],fk_transfer_id__fk_to_id = branch_id ,fk_transfer_id__dat_transfer__date__gte=dat_from,fk_transfer_id__dat_transfer__date__lte=dat_to).values('fk_transfer_id','fk_transfer_id__fk_from_id__vchr_name','fk_transfer_id__dat_transfer').annotate(sum_qty = Sum('int_qty')).annotate(status=Case(When(fk_transfer_id__int_status=2,then=Value('RECEIVED')),When(fk_transfer_id__int_status=5,then=Value('PARTIALLY RECEIVED')),default=Value('PENDING'),output_field=CharField()))
            if request.user.userdetails.fk_group.vchr_name.upper() in ['SERVICE MANAGER','SERVICE ENGINEER']:
                rst_data = rst_data.filter(fk_transfer__fk_from__vchr_code__in = ['MCL3','MPL4','MCH'],fk_item__fk_product__vchr_name = 'SPARE')

            for item in rst_data:
                dct_data = {}
                dct_data['int_transfer_id'] = item['fk_transfer_id']
                dct_data['dat_transfer'] = datetime.strftime(item['fk_transfer_id__dat_transfer'],'%d-%m-%Y')
                dct_data['vchr_from'] = item['fk_transfer_id__fk_from_id__vchr_name']
                dct_data['int_count'] = item['sum_qty']
                dct_data['status'] = item['status']
                lst_data.append(dct_data)
            return Response({'status':1,'data':lst_data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})

    def get(self,request):
        """
        To get list of item to acknowledge by int_transfer_id
        param : int_transfer_id
        return : int_transfer_id,item_name,item_id,int_qty,txt_imei,int_purchase_details_id,dbl_unitprice,dbl_ppu
        """
        try:
            # import pdb; pdb.set_trace()
            branch_id = request.user.userdetails.fk_branch_id
            int_transfer_id = request.GET.get('int_transfer_id')
            rst_item = IstDetails.objects.filter(fk_transfer_id__int_doc_status=0,fk_transfer_id__int_status__in = [2,5],fk_transfer_id__fk_to_id = branch_id,fk_transfer_id = int_transfer_id).values('pk_bint_id','fk_item_id','fk_item_id__vchr_name','fk_item_id__vchr_item_code','int_qty','jsn_imei','jsn_batch_no')

            lst_data = []
            for item in rst_item:
                dct_data = {}
                dct_imei = item['jsn_imei']['imei']
                # dct_data['imei'] = [ j for i  in  dct_imei.keys() for j in dct_imei[i]]
                dct_data['imei'] = item['jsn_imei']['imei']
                dct_data['item_id'] = item['fk_item_id']
                dct_data['int_qty'] = item['int_qty']
                dct_data['int_transfer_details_id'] = item['pk_bint_id']
                dct_data['vchr_item_code'] = item['fk_item_id__vchr_item_code']
                dct_data['vchr_name'] = item['fk_item_id__vchr_name']
                dct_data['ack'] = 0
                dct_data['imei_avl'] = []
                dct_data['imei_dmg'] = []
                dct_data['avl_all'] = False
                dct_data['dmg_all'] = False
                dct_data['batch_all'] = False
                dct_data['batch_id'] = item['jsn_batch_no']['batch']
                lst_data.append(dct_data)

            return Response({'status':1,'data':lst_data})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})

class ListBranchStock(APIView):
    permission_classes = [AllowAny]
    """
    To list Stock details of items in a branch.
    param : branch_id,item_id
    return :list of item details
    """
    def post(self,request):
        try:
            lst_data = []
            int_branch_id = request.data.get('IntBranchId')
            int_item_id = request.data.get('IntItemId')

            int_product_id = request.data.get('IntProductId')
            int_brand_id = request.data.get('IntBrandId')

            int_item_group_id = request.data.get('IntItemGroupId')
            bln_packing_items = request.data.get('blnPackingItems',False)
            lst_packing_item_codes=['STY00064','STY00038','STY00054','STY00241','STY00240','STY00254','STY00255','STY00267','STY00269','STY00322','STY00042','STY00333','STY00043']
            lst_excluse=[]
            if request.user.userdetails.fk_branch.int_type==1 and request.user.userdetails.fk_branch.vchr_code!='AGY':
                lst_excluse = list(Branch.objects.filter(vchr_code__in=['3GH','VSP','WHO1','ROC','ECO','AGY']).values_list('pk_bint_id',flat=True))
            elif request.user.userdetails.fk_branch.vchr_code=='AGY':
                lst_excluse = list(Branch.objects.filter(vchr_code__in=['3GH','VSP','WHO1','ROC','ECO']).values_list('pk_bint_id',flat=True))
            # import pdb; pdb.set_trace()
            lst_data = BranchStockImeiDetails.objects.filter(fk_details__int_qty__gt=0).exclude(fk_details__fk_master__fk_branch_id__in=lst_excluse).values('pk_bint_id','fk_details__fk_item__fk_product_id', 'fk_details__fk_item__fk_brand_id', 'fk_details__fk_item_id', 'fk_details__fk_item_id__vchr_name', 'fk_details__fk_item_id__vchr_item_code', 'fk_details__fk_master_id__fk_branch_id', 'fk_details__fk_master_id__fk_branch_id__vchr_name', 'jsn_imei', 'jsn_batch_no') .annotate(total_qty = Sum('int_qty')) .annotate(branch_age = (datetime.now()-F('fk_details__fk_master__dat_stock')), item_age=(datetime.now()-F('fk_grn_details__fk_purchase__dat_purchase'))).order_by('-pk_bint_id')

            # lst_data = BranchStockImeiDetails.objects.filter(fk_details__int_qty__gt=0).values('fk_details__fk_item__fk_product_id', 'fk_details__fk_item__fk_brand_id', 'fk_details__fk_item_id', 'fk_details__fk_item_id__vchr_name', 'fk_details__fk_item_id__vchr_item_code', 'fk_details__fk_master_id__fk_branch_id', 'fk_details__fk_master_id__fk_branch_id__vchr_name', 'fk_details__jsn_imei_avail', 'fk_details__jsn_batch_no') .annotate(total_qty = Sum('fk_details__int_qty')) .annotate(branch_age = (datetime.now()-F('fk_details__fk_master__dat_stock')), item_age=(datetime.now()-F('fk_grn_details__fk_purchase__dat_purchase')))

            lst_grn_data=GrnDetails.objects.filter(int_avail__gt=0).exclude(fk_purchase__fk_branch_id__in=lst_excluse).values('fk_item__fk_product_id','fk_item__fk_brand_id','fk_item_id', 'fk_item_id__vchr_name', 'fk_item__vchr_item_code', 'fk_purchase__fk_branch_id', 'fk_purchase__fk_branch__vchr_name', 'jsn_imei_avail','jsn_imei', 'vchr_batch_no', 'int_avail') .annotate(item_age=(datetime.now()-F('fk_purchase__dat_purchase'))).order_by('-pk_bint_id')

            # import pdb; pdb.set_trace()
            if int_item_id:
                # lst_data = lst_data.filter(fk_item_id = int_item_id).values('fk_item_id','fk_item_id__vchr_name','fk_item_id__vchr_item_code','fk_master_id__fk_branch_id','fk_master_id__fk_branch_id__vchr_name','jsn_imei','jsn_batch_no').annotate(total_qty = Sum('int_qty')).annotate(age = (datetime.now()-F('fk_master__dat_stock')))
                lst_data = lst_data.filter(fk_details__fk_item_id = int_item_id)
                lst_grn_data = lst_grn_data.filter(fk_item_id = int_item_id)
            if int_branch_id:
                lst_data = lst_data.filter(fk_details__fk_master_id__fk_branch_id = int_branch_id)
                lst_grn_data = lst_grn_data.filter(fk_purchase__fk_branch_id = int_branch_id)
                # lst_data = lst_data.filter(fk_master_id__fk_branch_id = int_branch_id).values('fk_item_id','fk_item_id__vchr_name','fk_item_id__vchr_item_code','fk_master_id__fk_branch_id','fk_master_id__fk_branch_id__vchr_name','jsn_imei','jsn_batch_no').annotate(total_qty = Sum('int_qty')).annotate(age = (datetime.now()-F('fk_master__dat_stock')))
            if int_product_id:
                lst_data = lst_data.filter(fk_details__fk_item__fk_product_id = int_product_id)
                lst_grn_data = lst_grn_data.filter(fk_item__fk_product_id = int_product_id)
            # import pdb;pdb.set_trace()
            if int_brand_id:
                lst_data = lst_data.filter(fk_details__fk_item__fk_brand_id = int_brand_id)
                lst_grn_data = lst_grn_data.filter(fk_item__fk_brand_id = int_brand_id)

            if int_item_group_id:
                lst_data = lst_data.filter(fk_details__fk_item__fk_item_group_id = int_item_group_id)
                lst_grn_data = lst_grn_data.filter(fk_item__fk_item_group_id = int_item_group_id)
            if bln_packing_items:
                int_branch_id=request.user.userdetails.fk_branch_id
                lst_data = lst_data.filter(fk_details__fk_item_id__vchr_item_code__in = lst_packing_item_codes,fk_details__fk_master_id__fk_branch_id = int_branch_id)
                lst_grn_data = lst_grn_data.filter(fk_item_id__vchr_item_code__in = lst_packing_item_codes,fk_purchase__fk_branch_id = int_branch_id)
            # ===============================================================================================================================================================
            lst_datas=[]

            for data in lst_data:
                data['branch_age'] = data['branch_age'].days if data['branch_age'] else 0
                data['item_age'] = data['item_age'].days if data['item_age'] else 0
                dct_data=data

                dct_data['imei']=[]
                if data['jsn_batch_no']['batch']:
                    dct_data['imei'].extend([{'imei':data,'status':'available'} for data in data['jsn_batch_no']['batch']])
                if dct_data['jsn_imei']['imei']:
                    lst_imei = dct_data['jsn_imei']['imei']
                    #uncoment if frontexport  end data is coorect
                    ins_non_saleable = NonSaleable.objects.filter(fk_branch_id = data['fk_details__fk_master_id__fk_branch_id'],fk_item_id = data['fk_details__fk_item_id'] ,int_status=0).values('jsn_non_saleable').first()
                    if ins_non_saleable:
                        lst_all_imei = dct_data['jsn_imei']['imei']
                        lst_non_saleable_imei = ins_non_saleable.get('jsn_non_saleable',[])
                        lst_imei = list(set(lst_all_imei) -set(lst_non_saleable_imei))
                        data['total_qty'] = len(lst_imei)
                    dct_data['imei'].extend([{'imei':data,'status':'available'} for data in lst_imei])

                lst_datas.append(dct_data)
            for data in lst_grn_data:
                dct_item = {}
                bln_non_sal = False
                dct_item['branch_age']= data['item_age'].days if data['item_age'] else 0
                dct_item['item_age']= data['item_age'].days if data['item_age'] else 0
                dct_item['fk_details__fk_item_id']= data['fk_item_id']
                dct_item['fk_details__fk_item_id__vchr_item_code']= data['fk_item__vchr_item_code']
                dct_item['fk_details__fk_item_id__vchr_name']= data['fk_item_id__vchr_name']
                dct_item['fk_details__fk_master_id__fk_branch_id']= data['fk_purchase__fk_branch_id']
                dct_item['fk_details__jsn_batch_no']= {'batch': [data['vchr_batch_no']]}
                dct_item['fk_details__fk_master_id__fk_branch_id__vchr_name']= data['fk_purchase__fk_branch__vchr_name']

                dct_item['fk_details__fk_item__fk_product_id']= data['fk_item__fk_product_id']
                dct_item['fk_details__fk_item__fk_brand_id']= data['fk_item__fk_brand_id']

                if data['jsn_imei_avail']['imei_avail']:

                    lst_imei = data['jsn_imei_avail']['imei_avail']
                    ins_non_saleable = NonSaleable.objects.filter(fk_branch_id = dct_item['fk_details__fk_master_id__fk_branch_id'],fk_item_id = dct_item['fk_details__fk_item_id'] ,int_status=0).values('jsn_non_saleable').first()
                    if ins_non_saleable:
                        lst_all_imei =  data['jsn_imei_avail']['imei_avail']
                        lst_non_saleable_imei = ins_non_saleable.get('jsn_non_saleable',[])
                        lst_imei = list(set(lst_all_imei) -set(lst_non_saleable_imei))
                        data['total_qty'] = len(lst_imei)
                        bln_non_sal = True
                    dct_item['fk_details__jsn_imei']= {'imei':lst_imei}




                    dct_item['imei']= [{'imei': imei_data, 'status': 'available'} for imei_data in lst_imei]
                else:
                    dct_item['imei']= [{'imei':data['vchr_batch_no'],'status': 'available'}]
                # if data['vchr_batch_no']:
                #     dct_item['imei']= [{'imei':data['vchr_batch_no'],'status': 'available'}]
                # else:
                #     dct_item['imei']= [{'imei': imei_data, 'status': 'available'} for imei_data in data['jsn_imei_avail']['imei_avail']]


                    # dct_item['total_qty'] = len(data['jsn_imei_avail']['imei_avail']) if data['jsn_imei_avail']['imei_avail'] else 0#data['int_avail']
                # dct_item['fk_details__jsn_imei']= {'imei':data['jsn_imei_avail']['imei_avail']}
                if not bln_non_sal:
                    dct_item['total_qty'] = data['int_avail']
                lst_datas.append(dct_item)
            # ==================================================================================================================================================================
            """List of dictionary sorting base on key vlaue"""
            # lst_new = sorted(lst_datas, key=itemgetter('fk_details__fk_master_id__fk_branch_id__vchr_name', 'fk_details__fk_master_id__fk_branch_id','fk_details__fk_item_id__vchr_name'))
            lst_new = sorted(lst_datas, key=itemgetter('fk_details__fk_item__fk_product_id', 'fk_details__fk_item__fk_brand_id','fk_details__fk_item_id'))
            # lst_new = sorted(lst_datas, key = lambda i:(i['fk_details__fk_master_id__fk_branch_id__vchr_name'],i['fk_details__fk_master_id__fk_branch_id'],i['fk_details__fk_item_id__vchr_name']))
            lst_transfer = IstDetails.objects.filter(fk_transfer__int_status__in= [1,2]).exclude(fk_transfer__fk_to_id__in=lst_excluse).values('fk_item_id__vchr_item_code','fk_item__vchr_name','fk_transfer__fk_to__vchr_name','fk_item__fk_product_id','fk_item__fk_brand_id','fk_item_id').annotate(qty=Sum('int_qty'))

            if int_item_id:
                lst_transfer = lst_transfer.filter(fk_item_id = int_item_id)
            if int_product_id:
                lst_transfer = lst_transfer.filter(fk_item__fk_product_id = int_product_id)
            if int_brand_id:
                lst_transfer = lst_transfer.filter(fk_item__fk_brand_id = int_brand_id)
            if int_branch_id:
                lst_transfer = lst_transfer.filter(fk_transfer__fk_to_id =int_branch_id)
            if int_item_group_id:
                lst_transfer = lst_transfer.filter(fk_item__fk_item_group_id = int_item_group_id)
            if bln_packing_items:
                lst_transfer = lst_transfer.filter(fk_item_id__vchr_item_code__in = lst_packing_item_codes,fk_transfer__fk_to_id =int_branch_id)


            dct_transfer = {item['fk_item_id__vchr_item_code']:item for item in lst_transfer}

            lst_data = []
            dct_data = OrderedDict()
            for item in lst_new:
                if item['fk_details__fk_master_id__fk_branch_id__vchr_name'] and item['fk_details__fk_item_id__vchr_item_code']:
                    if item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code'] not in dct_data:
                        dct_data[item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code']] = item

                        dct_data[item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code']]['tranfer_count'] = 0
                        if item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code'] in dct_transfer:
                            dct_data[item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code']]['tranfer_count'] = item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+dct_transfer[item['fk_details__fk_item_id__vchr_item_code']]['qty']
                    else:
                        dct_data[item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code']]['total_qty'] += item['total_qty']
                        if item['imei']:
                            dct_data[item['fk_details__fk_master_id__fk_branch_id__vchr_name']+"-"+item['fk_details__fk_item_id__vchr_item_code']]['imei'].extend(item['imei'])
                    # if item['fk_details__jsn_imei_avail']['imei']:
                    #     dct_data[item['fk_details__fk_item_id__vchr_item_code']]['fk_details__jsn_imei_avail']['imei'].extend(item['fk_details__jsn_imei_avail']['imei'])

                    # if item['fk_details__fk_item_id__vchr_item_code'] in dct_transfer:
                    #     dct_data[item['fk_details__fk_item_id__vchr_item_code']]['tranfer_count'] += dct_transfer[item['fk_details__fk_item_id__vchr_item_code']]['qty']

            lst_stock = dct_data.keys()
            lst_transfer = dct_transfer.keys()

            for item_code in (lst_transfer-lst_stock):
                dct_data[item_code] = {}
                dct_data[item_code]['fk_details__fk_item_id__vchr_item_code'] = dct_transfer[item_code]['fk_item_id__vchr_item_code']
                dct_data[item_code]['fk_details__fk_item_id__vchr_name'] = dct_transfer[item_code]['fk_item__vchr_name']
                dct_data[item_code]['tranfer_count'] = dct_transfer[item_code]['qty']
                dct_data[item_code]['fk_details__fk_master_id__fk_branch_id__vchr_name'] = dct_transfer[item_code]['fk_transfer__fk_to__vchr_name']
                dct_data[item_code]['total_qty'] = 0
                dct_data[item_code]['imei'] = []
                dct_data[item_code]['fk_details__fk_item__fk_product_id']=  dct_transfer[item_code]['fk_item__fk_product_id']
                dct_data[item_code]['fk_details__fk_item__fk_brand_id']=  dct_transfer[item_code]['fk_item__fk_brand_id']
                dct_data[item_code]['fk_details__fk_item_id']= dct_transfer[item_code]['fk_item_id']
                dct_data[item_code]['fk_details__fk_master_id__fk_branch_id']= int_branch_id
            lst_data = [item for item in dct_data.values()]

            lst_new_data = sorted(lst_data, key=itemgetter('fk_details__fk_item__fk_product_id', 'fk_details__fk_item__fk_brand_id','fk_details__fk_item_id'))
            if bln_packing_items:
                lst_new_data= [data for data in lst_new_data if data['total_qty']!=0]
            return Response({'status':1,'data':lst_new,'lst_data':lst_new_data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})


class GetPriceForItemAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            """ if parallel run is true fetch data using apis insted of database """
            if settings.PARALLEL_RUN:
                vchr_branch_code = request.user.userdetails.fk_branch.vchr_code
                int_id = request.data.get('pk_bint_id')
                str_imei = request.data.get('strImei')
                str_item_code = request.data.get('itemCode')
                bln_avail = request.data.get('blnAvail')
                ins_item_data = Item.objects.get(pk_bint_id = int_id)
                dct_response = Stock_Item_Checking(vchr_branch_code,str_item_code,str_imei)
                if dct_response == 'Not Available':
                    return Response({'status':'0','data':'Out of Stock'})
                if ins_item_data:
                    ins_item_cat = ItemCategory.objects.get(pk_bint_id = ins_item_data.fk_item_category_id)
                    ins_tax_master = TaxMaster.objects.filter().values()

                    dct_tax_master = {data['vchr_name']:data['pk_bint_id'] for data in ins_tax_master}
                    dct_data ={}
                    dct_data['dblRate'] = ins_item_data.dbl_mop
                    dct_data['dblAmount'] = ins_item_data.dbl_mop
                    dct_data['dblMopAmount'] = ins_item_data.dbl_mop
                    dct_data['mrp'] = ins_item_data.dbl_mrp
                    dct_data['dblMarginAmount'] = 0
                    # ins_tax_master = TaxMaster.objects.all()
                    dct_data['dblSGSTPer'] = ins_item_cat.json_tax_master.get(str(dct_tax_master['SGST']),0)
                    dct_data['dblSGST'] = ins_item_data.dbl_mop*ins_item_cat.json_tax_master.get(str(dct_tax_master['SGST']),0)/100
                    dct_data['dblCGSTPer'] = ins_item_cat.json_tax_master.get(str(dct_tax_master['CGST']),0)
                    dct_data['dblCGST'] = ins_item_data.dbl_mop*ins_item_cat.json_tax_master.get(str(dct_tax_master['CGST']),0)/100
                    dct_data['dblIGSTPer'] = ins_item_cat.json_tax_master.get(str(dct_tax_master['IGST']),0)
                    dct_data['dblIGST'] = ins_item_data.dbl_mop*ins_item_cat.json_tax_master.get(str(dct_tax_master['IGST']),0)/100
                    return Response({'status':'1','data':dct_data})
                url = "dfa"
            conn = engine.connect()
            int_id = request.data.get('pk_bint_id')
            str_imei = request.data.get('strImei')
            str_item_code = request.data.get('itemCode')
            bln_avail = request.data.get('blnAvail')
            int_price_template = request.user.userdetails.fk_branch.int_price_template
            # import pdb; pdb.set_trace()
            if str_item_code == 'GDC00001' or str_item_code == 'GDC00002':
                bln_sales_flag=False
                dat_sale = datetime.now()
                if bln_avail:
                    rst_partial_invoice = PartialInvoice.objects.filter(Q(json_data__icontains='"'+str_imei+'"')|Q(json_data__icontains="'"+str_imei+"'"),Q(json_data__icontains='"'+str_item_code+'"')|Q(json_data__icontains="'"+str_item_code+"'"),int_status=1).values('json_data').first()
                    if rst_partial_invoice:
                        pass
                    else:
                        rst_sales_details=SalesDetails.objects.filter(fk_item_id__vchr_item_code=str_item_code,json_imei__contains=str_imei).values('fk_master_id','fk_item_id')
                        if rst_sales_details:
                            for  ins_sales_details in rst_sales_details:
                                bln_sales_flag=True
                                rst_sales_return=SalesReturn.objects.filter(jsn_imei__contains=str_imei,fk_item_id=ins_sales_details['fk_item_id'],fk_returned_id=ins_sales_details['fk_master_id'])
                                if rst_sales_return:
                                    bln_sales_flag=False


                else:
                    # import pdb; pdb.set_trace()
                    rst_sales_details=SalesDetails.objects.filter(fk_item_id__vchr_item_code=str_item_code,json_imei__contains=str_imei).values('fk_master_id','fk_item_id')
                    ins_saled=SalesDetails.objects.filter(json_imei__contains=str_imei).values('fk_master_id','int_sales_status').exclude(fk_item_id__vchr_item_code=str_item_code).last()
                    if not SalesDetails.objects.filter(json_imei__contains=str_imei).values('fk_master_id').exclude(fk_item_id__vchr_item_code=str_item_code).last():
                        return Response({'status':'0','data':'No enquiry found for the given IMEI!'})
                    elif ins_saled['int_sales_status'] == 0:
                        return Response({'status':'0','data':'No enquiry found for the given IMEI!'})
                    elif rst_sales_details:

                        for  ins_sales_details in rst_sales_details:
                            bln_sales_flag=True
                            rst_sales_return=SalesReturn.objects.filter(jsn_imei__contains=str_imei,fk_returned_id=ins_sales_details['fk_master_id'])
                            if rst_sales_return:
                                bln_sales_flag=False






                if bln_sales_flag:
                    if str_item_code == 'GDC00001':
                        return Response({'status':'0','data':'GDOT already invoiced for imei no: '+str(str_imei)})
                    else:
                        return Response({'status':'0','data':'GDEW already invoiced for imei no: '+str(str_imei)})
                else:
                    try:

                        if str_item_code == 'GDC00001':
                            int_type=1
                            int_exp_days = -2
                        if str_item_code == 'GDC00002':
                            int_type=2
                            int_exp_days = -90

                        rst_stock = BranchStockDetails.objects.filter(Q(jsn_imei__icontains='"'+str_imei+'"')|Q(jsn_imei__icontains="'"+str_imei+"'")).values('fk_item_id__dbl_mop').exclude(fk_item_id=int_id).first()
                        if rst_stock:
                            dbl_mrp = rst_stock['fk_item_id__dbl_mop']
                        else:
                            return Response({'status':'0','data':'no item Found with corresponding imei'})
                        rst_sales_details=SalesDetails.objects.filter(json_imei__contains=str_imei,int_sales_status=1).values('fk_master__dat_created').exclude(fk_item_id__vchr_item_code=str_item_code).last()
                        if rst_sales_details:
                            dat_sale=rst_sales_details['fk_master__dat_created']



                        if date.today()+timedelta(days=int_exp_days) <= dat_sale.date():
                            ins_gdp_range = GDPRange.objects.filter(dbl_from__lte =dbl_mrp,dbl_to__gte =dbl_mrp,int_type=int_type).values('dbl_amt').first()
                            if not ins_gdp_range:
                                return Response({'status':'0','data':'Amount is not Valid for this imei'})

                            ins_item = Item.objects.filter(pk_bint_id=int_id).values('fk_item_category_id').first()
                            ins_item_mrp = Item.objects.filter(pk_bint_id=int_id).values('dbl_mrp').first()
                            ins_item_category = ItemCategory.objects.filter(pk_bint_id=ins_item['fk_item_category_id']).values('json_tax_master').first()
                            dct_tax = {}
                            for ins_tax in TaxMaster.objects.filter(bln_active=True).values('pk_bint_id','vchr_name'):
                                dct_tax[ins_tax['vchr_name']] = str(ins_tax['pk_bint_id'])
                            dct_data = {}
                            if ins_item_category:
                                dct_data['dblRate'] = ins_gdp_range['dbl_amt']
                                dct_data['dblAmount'] = ins_gdp_range['dbl_amt']
                                dct_data['dblMopAmount'] = ins_gdp_range['dbl_amt']
                                dct_data['mrp'] = ins_gdp_range['dbl_amt']
                                dct_data['dblMarginAmount'] = 0
                                dct_data['dblSGSTPer'] = ins_item_category['json_tax_master'].get(dct_tax['SGST'],0)
                                dct_data['dblSGST'] =ins_gdp_range['dbl_amt']*ins_item_category['json_tax_master'].get(dct_tax['SGST'],0)/100
                                dct_data['dblCGSTPer'] = ins_item_category['json_tax_master'].get(dct_tax['CGST'],0)
                                dct_data['dblCGST'] = ins_gdp_range['dbl_amt']*ins_item_category['json_tax_master'].get(dct_tax['CGST'],0)/100
                                dct_data['dblIGSTPer'] = ins_item_category['json_tax_master'].get(dct_tax['IGST'],0)
                                dct_data['dblIGST'] =  ins_gdp_range['dbl_amt']*ins_item_category['json_tax_master'].get(dct_tax['IGST'],0)/100
                                if request.data.get("blnIGST"):
                                    dct_data['GST']=dct_data['dblIGSTPer']
                                else:
                                    dct_data['GST']=dct_data['dblSGSTPer']+dct_data['dblCGSTPer']
                            else:
                                return Response({'status':'0','data':'Out of Stock'})
                        else:
                            return Response({'status':'0','data':'Date has been expired for this imei to receive Service Protection'})

                        return JsonResponse({'status':'1','data':dct_data})
                    except Exception as e:
                        ins_logger.logger.error(e, extra={'details':traceback.format_exc(),'user': 'user_id:' + str(request.user.id)})
                        return Response({'status':'1', 'error':str(e)})
            if int_price_template == 0:
                str_filter = 'dbl_cost_amnt'
            elif int_price_template == 1:
                str_filter = 'dbl_dealer_amt'
            elif int_price_template == 2:
                str_filter = 'dbl_mop'
            elif int_price_template == 3:
                str_filter = 'dbl_my_amt'
            else:
                str_filter = 'dbl_mrp'
            if Item.objects.filter(pk_bint_id=int_id).values('fk_product__vchr_name') and Item.objects.filter(pk_bint_id=int_id).values('fk_product__vchr_name').first()['fk_product__vchr_name'] not in ['SERVICE']:
                query = "select case when dbl_price is null then dbl_mrp else dbl_price end, dbl_mrp, json_tax_master from(select itm.dbl_mrp, (select "+str_filter+" from price_list where int_status=1 and fk_item_id=itm.pk_bint_id and dat_efct_from<=current_date and int_status>=0 order by dat_efct_from desc limit 1) as dbl_price,cat.json_tax_master from item as itm join branch_stock_details as stkd on stkd.fk_item_id=itm.pk_bint_id join item_category as cat on cat.pk_bint_id=itm.fk_item_category_id left outer join branch_stock_master as stkm on stkm.pk_bint_id=stkd.fk_master_id where itm.pk_bint_id= " + str(int_id)+" and (jsn_imei_avail->'imei' ?| array['"+str_imei+"'] or jsn_batch_no->'batch' ?| array['"+str_imei+"']) and stkd.int_qty>0)as pr"
            else:
                query = "select case when dbl_price is null then dbl_mrp else dbl_price end, dbl_mrp, json_tax_master from(select itm.dbl_mrp, (select "+str_filter+" from price_list where int_status=1 and fk_item_id=itm.pk_bint_id and dat_efct_from<=current_date and int_status>=0 order by dat_efct_from desc limit 1) as dbl_price,cat.json_tax_master from item as itm join item_category as cat on cat.pk_bint_id=itm.fk_item_category_id where itm.pk_bint_id= " + str(int_id)+")as pr"
            ins_item_data = conn.execute(query).fetchall()
            dct_tax = {}
            for ins_tax in TaxMaster.objects.filter(bln_active=True).values('pk_bint_id','vchr_name'):
                dct_tax[ins_tax['vchr_name']] = str(ins_tax['pk_bint_id'])

            dct_data = {}
            if ins_item_data:
                dct_data['dblRate'] = ins_item_data[0].dbl_price
                dct_data['dblAmount'] = ins_item_data[0].dbl_price
                dct_data['dblMopAmount'] = ins_item_data[0].dbl_price
                dct_data['mrp'] = ins_item_data[0].dbl_mrp
                dct_data['dblMarginAmount'] = 0

                dct_data['dblSGSTPer'] = ins_item_data[0].json_tax_master.get(dct_tax['SGST'],0)
                dct_data['dblSGST'] = ins_item_data[0].dbl_price*ins_item_data[0].json_tax_master.get(dct_tax['SGST'],0)/100
                dct_data['dblCGSTPer'] = ins_item_data[0].json_tax_master.get(dct_tax['CGST'],0)
                dct_data['dblCGST'] = ins_item_data[0].dbl_price*ins_item_data[0].json_tax_master.get(dct_tax['CGST'],0)/100
                dct_data['dblIGSTPer'] = ins_item_data[0].json_tax_master.get(dct_tax['IGST'],0)
                dct_data['dblIGST'] = ins_item_data[0].dbl_price*ins_item_data[0].json_tax_master.get(dct_tax['IGST'],0)/100
                if request.data.get('blnIGST'):
                    dct_data['GST']=dct_data['dblIGSTPer']
                else:
                    dct_data['GST']=dct_data['dblSGSTPer']+dct_data['dblCGSTPer']
            else:
                return Response({'status':'0','data':'Out of Stock'})

            return Response({'status':'1','data':dct_data})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})



class ItemRestore(APIView):
    """
     Restore the item into grn_details/branch_stock_details if the item is not tranferredself.

    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            with transaction.atomic():
                # ================================================================================================================
                str_transfer_num = request.data.get('transferNum')
                int_item_id = request.data.get('itemId')
                lst_imei = request.data.get('availableImei') or []
                int_user_id = request.user.userdetails.user_ptr_id
                int_branch_id = request.user.userdetails.fk_branch.pk_bint_id

                if Branch.objects.filter(pk_bint_id = int_branch_id).values_list('int_type',flat=True).first() in [2,3]: # if transfer from head office
                    lst_added_imei = []
                    # ===== If item is transferred from branch_stock ====
                    lst_branch_stock = BranchStockDetails.objects.filter(fk_master_id__fk_branch_id = int_branch_id,jsn_imei__imei__has_any_keys = lst_imei)
                    if lst_branch_stock:
                        for ins_data in lst_branch_stock:
                            lst_not_transfered = list(set(ins_data.jsn_imei['imei']) & set(lst_imei))
                            lst_added_imei.extend(lst_not_transfered)
                            ins_data.jsn_imei_avail['imei'].extend(lst_not_transfered)
                            ins_data.int_qty = len(ins_data.jsn_imei_avail['imei'])
                            ins_data.save()
                            lst_branch_imei = BranchStockImeiDetails.objects.filter(fk_details_id = ins_data.pk_bint_id).values('pk_bint_id','fk_grn_details_id','fk_details_id','fk_details_id__jsn_imei','fk_grn_details_id__jsn_imei','fk_grn_details_id__jsn_imei','jsn_imei','fk_grn_details_id__dbl_ppu','fk_details__fk_item_id')
                            for ins_imei in lst_branch_imei:
                                lst_imei_not_transferred = list(set(ins_imei['fk_grn_details_id__jsn_imei']['imei']) & set(ins_imei['fk_details_id__jsn_imei']['imei']) & set(lst_imei))
                                ins_branch_imei_details = BranchStockImeiDetails.objects.filter(pk_bint_id = ins_imei['pk_bint_id']).first()
                                ins_branch_imei_details.jsn_imei['imei'].extend(lst_imei_not_transferred)
                                ins_branch_imei_details.int_qty = len(ins_branch_imei_details.jsn_imei['imei'])
                                ins_branch_imei_details.save()


                        ins_stocktransfer = IstDetails.objects.filter(fk_item_id = int_item_id,jsn_imei__imei__has_any_keys=lst_imei,fk_transfer_id__vchr_stktransfer_num = str_transfer_num).first()
                        lst_transfer_imei = ins_stocktransfer.jsn_imei['imei']
                        ins_stocktransfer.jsn_imei['imei'] = list(set(lst_transfer_imei)-set(lst_imei))
                        ins_stocktransfer.int_qty = ins_stocktransfer.int_qty-len(lst_imei)
                        ins_stocktransfer.save()
                    # ===== If item is transferred from grn_details ====
                    lst_data = StockTransferImeiDetails.objects.filter(fk_details_id__fk_transfer_id__vchr_stktransfer_num = str_transfer_num,fk_details_id__fk_item_id =int_item_id).values('fk_grn_details_id','pk_bint_id','fk_details_id','jsn_imei','fk_details_id__jsn_imei','fk_grn_details_id__jsn_imei','fk_details__fk_transfer__fk_from_id')
                    if  lst_data:
                        lst_imei = list(set(lst_imei)-set(lst_added_imei))
                        for dct_data in lst_data:
                            int_stocktransfer = dct_data['fk_details_id']
                            # add not_transfered imei to GrnDetails
                            ins_grn_details = GrnDetails.objects.filter(pk_bint_id = dct_data['fk_grn_details_id']).first()
                            lst_not_transfered = list(set( dct_data['fk_grn_details_id__jsn_imei']['imei']) & set(lst_imei))
                            ins_grn_details.jsn_imei_avail['imei_avail'].extend(lst_not_transfered)
                            ins_grn_details.int_avail = len(ins_grn_details.jsn_imei_avail['imei_avail'])
                            ins_grn_details.save()

                            # remove not_transfered imei from StockTransferImeiDetails
                            ins_stocktransferimei = StockTransferImeiDetails.objects.filter(pk_bint_id = dct_data['pk_bint_id']).first()
                            lst_imei_exist = ins_stocktransferimei.jsn_imei['imei']
                            ins_stocktransferimei.jsn_imei['imei'] = list(set(lst_imei_exist)-set(lst_imei))
                            ins_stocktransferimei.save()

                        # remove not_transfered imei from IstDetails
                        ins_stocktransfer = IstDetails.objects.filter(pk_bint_id = int_stocktransfer).first()
                        lst_transfer_imei = ins_stocktransfer.jsn_imei['imei']
                        ins_stocktransfer.jsn_imei['imei'] = list(set(lst_transfer_imei)-set(lst_imei))
                        ins_stocktransfer.int_qty = ins_stocktransfer.int_qty-len(lst_imei)
                        ins_stocktransfer.save()

                    return Response({'status':1,'message':'success'})


                else: # if tranfer from a branch

                    lst_branch_stock = BranchStockDetails.objects.filter(fk_master_id__fk_branch_id = int_branch_id,jsn_imei__imei__has_any_keys = lst_imei)
                    for ins_data in lst_branch_stock:
                        lst_not_transfered = list(set(ins_data.jsn_imei['imei']) & set(lst_imei))
                        ins_data.jsn_imei_avail['imei'].extend(lst_not_transfered)
                        ins_data.int_qty = len(ins_data.jsn_imei_avail['imei'])
                        ins_data.save()
                        lst_branch_imei = BranchStockImeiDetails.objects.filter(fk_details_id = ins_data.pk_bint_id).values('pk_bint_id','fk_grn_details_id','fk_details_id','fk_details_id__jsn_imei','fk_grn_details_id__jsn_imei','fk_grn_details_id__jsn_imei','jsn_imei','fk_grn_details_id__dbl_ppu','fk_details__fk_item_id')
                        for ins_imei in lst_branch_imei:
                            lst_imei_not_transferred = list(set(ins_imei['fk_grn_details_id__jsn_imei']['imei']) & set(ins_imei['fk_details_id__jsn_imei']['imei']) & set(lst_imei))
                            ins_branch_imei_details = BranchStockImeiDetails.objects.filter(pk_bint_id = ins_imei['pk_bint_id']).first()
                            ins_branch_imei_details.jsn_imei['imei'].extend(lst_imei_not_transferred)
                            ins_branch_imei_details.int_qty = len(ins_branch_imei_details.jsn_imei['imei'])
                            ins_branch_imei_details.save()


                    ins_stocktransfer = IstDetails.objects.filter(fk_item_id = int_item_id,jsn_imei__imei__has_any_keys=lst_imei,fk_transfer_id__vchr_stktransfer_num = str_transfer_num).first()
                    lst_transfer_imei = ins_stocktransfer.jsn_imei['imei']
                    ins_stocktransfer.jsn_imei['imei'] = list(set(lst_transfer_imei)-set(lst_imei))
                    ins_stocktransfer.int_qty = ins_stocktransfer.int_qty-len(lst_imei)
                    ins_stocktransfer.save()

                    return Response({'status':1,'message':'success'})
                return Response({'status':0,'message':'Error'})
            # ================================================================================================================

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})



class NonSaleableAPI(APIView):
    """
        Add items to Non Saleable with respect to IMEI and List of of items in saleabale and non saleable conditon.
        param : Item id ,list of Non Saleable IMEIs
        return : list of Saleable and Non Saleable IMEIs corresponds to the item.
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            bln_save = request.data.get('blnSave')
            int_item_id = request.data.get('intItemId')
            int_imei = request.data.get('strImei')
            int_branch_id = request.data.get('intBranchId')
            str_remarks = request.data.get('strRemarks')
            if not int_branch_id:
                int_branch_id = request.user.userdetails.fk_branch.pk_bint_id

            # ----------------------------------------Save Non-Saleable--------------------------------------------------------------------------------------
            if bln_save:
                with transaction.atomic():
                    lst_saleable = [item['imei'] for item in request.data.get('lst_saleable') or []]
                    lst_non_saleable = [item['imei'] for item in request.data.get('lst_non_saleable') or []]

                    # Instance of NonSaleable if the item and branch  exists in table , Then change status into not active(1),add updated user id and updated time.
                    ins_non_saleable = NonSaleable.objects.filter(fk_item_id = int_item_id,fk_branch_id = int_branch_id,int_status = 0).first()
                    if ins_non_saleable:
                        ins_non_saleable.dat_updated = datetime.now()
                        ins_non_saleable.fk_updated = request.user.userdetails
                        ins_non_saleable.int_status = 1  # Not active
                        ins_non_saleable.jsn_status_change = list(set(ins_non_saleable.jsn_non_saleable) & set(lst_saleable)) # List of IMEIs which is changed to salable
                        ins_non_saleable.vchr_remarks =str_remarks
                        ins_non_saleable.save()

                    ins_new_nonsaleable = NonSaleable(
                                                     fk_item_id = int_item_id,
                                                     fk_branch_id = int_branch_id,
                                                     dat_created = datetime.now(),
                                                     fk_created = request.user.userdetails,
                                                     int_status = 0, # active
                                                     jsn_non_saleable = lst_non_saleable, # List of Non Salable IMEIs
                                                     jsn_status_change = [],
                                                     vchr_remarks = str_remarks
                                                   )
                    ins_new_nonsaleable.save()

    # ---------------------------------List Salable and Non-Saleable-------------------------------------------------------------------------------------------------------------------
            dct_data = {'lst_non_saleable' :[],'lst_saleable' :[]}
            lst_non_saleable = []
            lst_saleable = []
            # To get list of IMEIs of an item in  current users's branch
            if int_imei:
                rst_branch_imei = BranchStockDetails.objects.filter(fk_item_id = int_item_id,fk_master__fk_branch_id = int_branch_id,jsn_imei_avail__icontains = int_imei).values('jsn_imei_avail')
                lst_imei = [item for item in list(itertools.chain.from_iterable([item['jsn_imei_avail']['imei'] for item in rst_branch_imei])) if int_imei in item]
                if int_imei in lst_imei:
                    lst_imei[lst_imei.index(int_imei)],lst_imei[0] = lst_imei[0],lst_imei[lst_imei.index(int_imei)]

            else:
                rst_branch_imei = BranchStockDetails.objects.filter(fk_item_id = int_item_id,fk_master__fk_branch_id = int_branch_id).values('jsn_imei_avail')
                lst_imei = list(itertools.chain.from_iterable([item['jsn_imei_avail']['imei'] for item in rst_branch_imei]))

            # To get list Non salable IMEIs of the item
            rst_non_saleable = NonSaleable.objects.filter(fk_item_id = int_item_id,int_status = 0,fk_branch_id = int_branch_id).values('jsn_non_saleable').first()
            if rst_non_saleable:
                lst_non_saleable = rst_non_saleable['jsn_non_saleable'] if rst_non_saleable['jsn_non_saleable'] else []

                if int_imei:
                    lst_similar = [item for item in lst_non_saleable if int_imei in item] # list of IMEIs similar to the input IMEI string
                    lst_other  = list(set(lst_non_saleable) - set(lst_similar))
                    lst_non_saleable = lst_similar+lst_other # list similar IMEI in front positions and then others
                    if int_imei in lst_non_saleable:
                        lst_non_saleable[lst_non_saleable.index(int_imei)],lst_non_saleable[0] = lst_non_saleable[0],lst_non_saleable[lst_non_saleable.index(int_imei)] # swap extact IMEI string in first index

                dct_data['lst_non_saleable'] = [{'imei':item,'blnSaleable':False} for item in lst_non_saleable]

            # list of Salable IMEI of the item
            lst_saleable = list(set(lst_imei)-set(lst_non_saleable))
            dct_data['lst_saleable'] = [{'imei':item,'blnSaleable':True} for item in lst_saleable]

            return Response({'status':1,'dct_data':dct_data})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':'0','message':str(e)})


class BranchItemStockAPI(APIView):

    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            # LG
            check_auth = request.META.get('REMOTE_ADDR')
            if check_auth not in ['94.237.66.244','94.237.77.193','149.28.131.169']:
                return Response({"status":0,"reason":"unauthorized access"})

            # int_auth = request.data.get('auth_key')
            # int_auth_key = '1122-3344-5566-7788'
            # if int_auth  != int_auth_key:
            #     return Response({"status":0,"reason":"authentication failed"})
            str_item_code = request.data.get('ITEM_CODE')
            # str_item_code = "AZRD09165"
            ins_item = Item.objects.filter(vchr_item_code = str_item_code).values('pk_bint_id').first()
            ins_branch=Branch.objects.filter(int_type__in=[1,2,3]).values('pk_bint_id','vchr_name')
            ins_data=BranchStockDetails.objects.filter(fk_item=ins_item['pk_bint_id']).values('fk_master__fk_branch__vchr_name','int_qty','fk_master__fk_branch')
            ins_grndata = GrnDetails.objects.filter(int_avail__gte=1,fk_item_id = ins_item['pk_bint_id']).values('fk_purchase_id__fk_branch__vchr_name','int_avail','fk_purchase_id__fk_branch')
            ins_transer=IstDetails.objects.filter(fk_item_id=ins_item['pk_bint_id'],fk_transfer__int_status=1).values('fk_item','int_qty','fk_transfer__fk_to')
            str_item_name=Item.objects.filter(pk_bint_id=ins_item['pk_bint_id']).values('vchr_name')[0]['vchr_name']


            lst_data=[]
            if ins_branch:
                if ins_grndata:
                    for data in ins_branch:
                        dict_item={}
                        ins_sealable_git=ins_transer.filter(fk_transfer__fk_to=data['pk_bint_id'])
                        ins_branch_grn_itemStock=ins_grndata.filter(fk_purchase_id__fk_branch=data['pk_bint_id']).values('int_avail')
                        ins_branch_itemStock=ins_data.filter(fk_master__fk_branch=data['pk_bint_id']).values('int_qty')
                        if ins_sealable_git:
                            for qty in ins_sealable_git:
                                if dict_item.get('SALEABLE_GIT') == None:
                                    dict_item['SALEABLE_GIT']=qty['int_qty']
                                else:
                                    dict_item['SALEABLE_GIT'] += qty['int_qty']
                        else:
                            dict_item['SALEABLE_GIT']=0
                        if ins_branch_grn_itemStock:
                            for qty in ins_branch_grn_itemStock:
                                if dict_item.get('SALEABLE_STOCK') == None:
                                    dict_item['SALEABLE_STOCK']=qty['int_avail']
                                else:
                                    dict_item['SALEABLE_STOCK'] += qty['int_avail']
                        else:
                            if dict_item.get('SALEABLE_STOCK') == None:
                                dict_item['SALEABLE_STOCK']=0

                        if ins_branch_itemStock:
                            for qty in ins_branch_itemStock:
                                if dict_item.get('SALEABLE_STOCK') == None:
                                    dict_item['SALEABLE_STOCK'] = qty['int_qty']
                                else:
                                    dict_item['SALEABLE_STOCK'] += qty['int_qty']

                        else:
                            if dict_item.get('SALEABLE_STOCK') == None:
                                dict_item['SALEABLE_STOCK']=0
                        dict_item['ITEM_CODE']=str_item_code
                        dict_item['ITEM_NAME']=str_item_name
                        dict_item['BRANCH_NAME']=data['vchr_name']
                        dict_item['SALEABLE_DC_GIT']=0
                        lst_data.append(dict_item)
                else:
                    for data in ins_branch:
                        dict_item={}
                        ins_sealable_git=ins_transer.filter(fk_transfer__fk_to=data['pk_bint_id'])
                        ins_branch_itemStock=ins_data.filter(fk_master__fk_branch=data['pk_bint_id']).values('int_qty')
                        if ins_sealable_git:
                            for qty in ins_sealable_git:
                                if dict_item.get('SALEABLE_GIT') == None:
                                    dict_item['SALEABLE_GIT']=qty['int_qty']
                                else:
                                    dict_item['SALEABLE_GIT'] += qty['int_qty']
                        else:
                            dict_item['SALEABLE_GIT']=0

                        if ins_branch_itemStock:
                            for qty in ins_branch_itemStock:
                                if dict_item.get('SALEABLE_STOCK') == None:
                                    dict_item['SALEABLE_STOCK'] = qty['int_qty']
                                else:
                                    dict_item['SALEABLE_STOCK'] += qty['int_qty']
                        else:
                            dict_item['SALEABLE_STOCK']=0

                        dict_item['ITEM_CODE']=str_item_code
                        dict_item['ITEM_NAME']=str_item_name
                        dict_item['BRANCH_NAME']=data['vchr_name']
                        dict_item['SALEABLE_DC_GIT']=0
                        lst_data.append(dict_item)
            else:
                return Response ({"status":1,"reason":"No Data.."})

            return Response ({"status":1,"data":lst_data})

        except Exception as e:
            print("Error",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({"status":0,"reason":e})



class BranchItemStockEcommerceAPI(APIView):

    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            current_time = datetime.now() - timedelta(minutes=10)
            str_item_code = json.loads(request.data.get('ITEM_CODE'))
            # str_item_code =['AZRD11196','AZRD11185','SPR23753']
            ins_item = Item.objects.filter(vchr_item_code__in=str_item_code).values_list('pk_bint_id',flat=True)

            lst_salesdet = SalesDetails.objects.filter(fk_item_id__in = ins_item,fk_master__dat_created__gte = current_time).values_list("fk_item_id","fk_master__fk_branch_id")
            ins_transfer = IstDetails.objects.filter(fk_item_id__in=ins_item,fk_transfer__dat_created__gte = current_time)
            lst_grndata = GrnDetails.objects.filter(int_avail__gte=1,fk_item_id__in = ins_item,fk_purchase__dat_created__gte = current_time).values_list("fk_item_id","fk_purchase__fk_branch_id")
            lst_grn_good_ret = GrnrDetails.objects.filter(fk_item_id__in = ins_item,fk_master__dat_created__gte = current_time).values_list("fk_item_id","fk_master__fk_branch")

            # lst_salesdet = SalesDetails.objects.filter(fk_item_id__in = ins_item).values_list("fk_item_id","fk_master__fk_branch_id").distinct()
            # ins_transfer = IstDetails.objects.filter(fk_item_id__in=ins_item,fk_transfer__int_status=1)
            # lst_grndata = GrnDetails.objects.filter(int_avail__gte=1,fk_item_id__in = ins_item).values_list("fk_item_id","fk_purchase__fk_branch_id").distinct()
            # lst_grn_good_ret = GrnrDetails.objects.filter(fk_item__in = ins_item).values_list("fk_item","fk_master__fk_branch").distinct()

            lst_transer_from = ins_transfer.all().values_list("fk_item_id","fk_transfer__fk_from").distinct()
            lst_transer_to = ins_transfer.all().values_list("fk_item_id","fk_transfer__fk_to").distinct()
            lst_items = []
            if lst_salesdet or ins_transfer or lst_grndata or lst_grn_good_ret:

                lst_items.extend(lst_salesdet)
                lst_items.extend(lst_grndata)
                lst_items.extend(lst_grn_good_ret)
                lst_items.extend(lst_transer_to)
                lst_items.extend(lst_transer_from)
                lst_items = set(lst_items)

                ins_branch_stock = BranchStockDetails.objects.filter(fk_item_id__in = ins_item)
                dct_res_data = {}
                if lst_items:
                    for i in lst_items:
                        # if i[0] == 44427:
                        #         # print(stock["fk_master__fk_branch__vchr_code"])
                        #         import pdb; pdb.set_trace()
                        stock = ins_branch_stock.filter(fk_item_id = i[0],fk_master__fk_branch_id = i[1]).values("fk_item__vchr_item_code","fk_master__fk_branch__vchr_code").annotate(int_qty = Sum("int_qty"))
                        dct__temp ={}
                        dct_data_temp = {}

                        if stock:
                            stock = stock[0]
                            dict_transit = ins_transfer.filter(fk_item_id= i[0],fk_transfer__fk_to_id = i[1],fk_transfer__int_status__in=(1,2)).values("int_qty").aggregate(int_qty = Sum("int_qty"))
                            if dict_transit['int_qty']:
                                dct_data_temp["INTRANSIT_QTY"] = dict_transit['int_qty']
                            else:
                                dct_data_temp["INTRANSIT_QTY"] = 0

                            dct_data_temp["STOCK_QTY"] = stock['int_qty']
                            if dct__temp.get(stock["fk_master__fk_branch__vchr_code"]):
                                dct__temp[stock["fk_master__fk_branch__vchr_code"]].update(dct_data_temp)
                            else:
                                dct__temp[stock["fk_master__fk_branch__vchr_code"]] = dct_data_temp
                            if  dct_res_data.get(stock["fk_item__vchr_item_code"]):
                                dct_res_data[stock["fk_item__vchr_item_code"]].update(dct__temp)
                            else:
                                dct_res_data[stock["fk_item__vchr_item_code"]] = dct__temp
                        else:
                            dict_transit = ins_transfer.filter(fk_item_id= i[0],fk_transfer__fk_to_id = i[1],fk_transfer__int_status__in = (1,2)).values("fk_transfer__fk_to__vchr_code","fk_item__vchr_item_code").annotate(int_qty = Sum("int_qty"))
                            if dict_transit:
                                if dict_transit[0].get("int_qty"):
                                    dct_data_temp["INTRANSIT_QTY"] = dict_transit[0]['int_qty']
                                    dct_data_temp["STOCK_QTY"] = 0
                                    if dct__temp.get(dict_transit[0]["fk_transfer__fk_to__vchr_code"]):
                                        dct__temp[dict_transit[0]["fk_transfer__fk_to__vchr_code"]].update(dct_data_temp)
                                    else:
                                        dct__temp[dict_transit[0]["fk_transfer__fk_to__vchr_code"]] = dct_data_temp

                                    if  dct_res_data.get(dict_transit[0]["fk_item__vchr_item_code"]):
                                        dct_res_data[dict_transit[0]["fk_item__vchr_item_code"]].update(dct__temp)
                                    else:
                                        dct_res_data[dict_transit[0]["fk_item__vchr_item_code"]] = dct__temp

                return Response ({"status":200,"data":dct_res_data,"success":True})

            return Response ({"status":203,"data":{},"success":False})

        except Exception as e:
            print("Error",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({"status":0,"reason":e})

class CompanyItemStockEcommerceAPI(APIView):

    permission_classes = [AllowAny]
    def post(self,request):
        try:
            session = Connection() #sql alchemy connection

            current_time = datetime.now() - timedelta(minutes=11)
            str_item_code = json.loads(request.data.get('ITEM_CODE'))


            ins_item = Item.objects.filter(vchr_item_code__in=str_item_code).values_list('pk_bint_id',flat=True)

            lst_salesdet = SalesDetails.objects.filter(fk_item_id__in = ins_item,fk_master__dat_created__gte = current_time).values_list("fk_item_id",flat = True)
            lst_grndata = GrnDetails.objects.filter(int_avail__gte=1,fk_item_id__in = ins_item,fk_purchase__dat_created__gte = current_time).values_list("fk_item_id",flat = True)
            lst_grn_good_ret = GrnrDetails.objects.filter(fk_item_id__in = ins_item,fk_master__dat_created__gte = current_time).values_list("fk_item_id",flat = True)

            lst_items = []
            if lst_salesdet or lst_grndata or lst_grn_good_ret:

                lst_items.extend(lst_salesdet)
                lst_items.extend(lst_grndata)
                lst_items.extend(lst_grn_good_ret)
                lst_items = set(lst_items)

                # ins_branch_stock = BranchStockDetails.objects.filter(fk_item_id__in = ins_item)
                dct_res_data = {}

                rst_sales_det = session.query(func.sum(BranchStockDetailsSA.int_qty).label('STOCK_QTY'),ItemsSA.vchr_item_code.label("ITEM_CODE"))\
                    .join(ItemsSA,ItemsSA.pk_bint_id == BranchStockDetailsSA.fk_item_id)\
                    .filter(BranchStockDetailsSA.fk_item_id.in_ (ins_item))\
                    .group_by(ItemsSA.vchr_item_code).subquery()


                rst_transit_details = session.query(func.sum(IstDetailsSA.int_qty).label("INTRANSIT_QTY"),ItemsSA.vchr_item_code.label("ITEM_CODE"))\
                    .join(ItemsSA,ItemsSA.pk_bint_id == IstDetailsSA.fk_item_id)\
                    .join(StockTransferSA,StockTransferSA.pk_bint_id == IstDetailsSA.fk_transfer_id)\
                    .filter(IstDetailsSA.fk_item_id.in_ (ins_item))\
                    .filter(StockTransferSA.int_status.in_([0,1,2]))\
                    .group_by(ItemsSA.vchr_item_code).subquery()

                rst_data = session.query(rst_sales_det.c.STOCK_QTY,rst_sales_det.c.ITEM_CODE,rst_transit_details.c.INTRANSIT_QTY)\
                    .join(rst_transit_details,rst_transit_details.c.ITEM_CODE == rst_sales_det.c.ITEM_CODE)


                for item in  rst_data.all():
                    dct_nested_data = {}
                    dct_nested_data["STOCK_QTY"] = item.STOCK_QTY
                    dct_nested_data["INTRANSIT_QTY"] = item.INTRANSIT_QTY
                    dct_res_data[item.ITEM_CODE] = dct_nested_data

                # import pdb; pdb.set_trace()
                return Response ({"status":200,"data":dct_res_data,"success":True})

            return Response ({"status":204,"data":{},"success":False})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({"status":0,"reason":e,"code":417})
        finally:
            session.close()
