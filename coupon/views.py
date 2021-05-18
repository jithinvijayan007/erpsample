# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from datetime import datetime
from POS import ins_logger
import sys, os
from rest_framework.response import Response
from coupon.models import Coupon,StaffCouponMaster,StaffCouponDetails
from products.models import Products
from brands.models import Brands
from item_category.models import ItemCategory,Item
from item_group.models import ItemGroup
import pandas as pd
from datetime import datetime,date
from pytz import timezone
from django.db.models import Q,F
from django.db import transaction
from rest_framework.parsers import MultiPartParser,FileUploadParser
from rest_framework.serializers import ModelSerializer,FileField
from ledger_details.models import ImportFiles
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Upper
import json
localtz = timezone('Asia/Kolkata')


# Create your views here.
class Xlsserilzer(ModelSerializer):
    class Meta:
        model = ImportFiles
        fields = ('vchr_file_name',)



class AddCoupon(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            str_code=request.data.get('strCouponCode')
            dat_expiry=request.data.get('datExpiry')
            int_which=request.data.get('intWhich')
            fk_package=request.data.get('fkPackage')
            int_discount_percentage = request.data.get('intDiscountPercentage')
            bint_max_discount_amt = request.data.get('bintMaxDiscountAmt')
            bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt')
            int_max_usage_no = request.data.get('intMaxUsageNo')
            dat_expiry=datetime.strptime(dat_expiry,'%Y-%m-%d')
            if Coupon.objects.filter(vchr_coupon_code=str_code):
                return Response({'status':0,'reason':"Coupon code already exists!"})

            if(int_which==0):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            elif(int_which==1):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,fk_product_id=fk_package,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            elif(int_which==2):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,fk_brand_id=fk_package,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            elif(int_which==3):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,fk_item_category_id=fk_package,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            elif(int_which==4):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,fk_item_group_id=fk_package,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            elif(int_which==5):
                Coupon.objects.create(vchr_coupon_code=str_code,dat_expiry=dat_expiry,fk_item_id=fk_package,int_discount_percentage=int_discount_percentage,\
                bint_max_discount_amt = bint_max_discount_amt,bint_min_purchase_amt = bint_min_purchase_amt,int_max_usage_no = int_max_usage_no,int_which=int_which,\
                fk_created_id=request.user.id,dat_created=localtz.localize(datetime.now()))
            return Response({'status':1})
        except Exception as e:

                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                            return Response({'status':0,'reason':e})


class ListCoupon(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        try:

            ListCoupon=list(Coupon.objects.filter(int_which=1).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','fk_product__vchr_name','dat_created' ))
            ListCoupon.extend(list(Coupon.objects.filter(int_which=2).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','fk_brand__vchr_name','dat_created')))

            ListCoupon.extend(list(Coupon.objects.filter(int_which=3).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','fk_item_category__vchr_item_category','dat_created')))
            ListCoupon.extend(list(Coupon.objects.filter(int_which=4).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','fk_item_group__vchr_item_group','dat_created')))
            ListCoupon.extend(list(Coupon.objects.filter(int_which=5).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','fk_item__vchr_name','dat_created')))
            ListCoupon.extend(list(Coupon.objects.filter(int_which=0).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
            'int_which','dat_created')))
            ListCoupon = sorted(ListCoupon, key = lambda i: i['dat_created'],reverse=True)
            lst_package=['All','Product','Brand','Item Category','Item Group','Item']
            for item in ListCoupon:
                if 'fk_product__vchr_name' in item:
                    item['vchr_name']=item.pop('fk_product__vchr_name')
                if 'fk_brand__vchr_name' in item:
                    item['vchr_name']=item.pop('fk_brand__vchr_name')
                if 'fk_item_category__vchr_item_category' in item:
                    item['vchr_name']=item.pop('fk_item_category__vchr_item_category')
                if 'fk_item_group__vchr_item_group' in item:
                    item['vchr_name']=item.pop('fk_item_group__vchr_item_group')
                if 'fk_item__vchr_name' in item:
                    item['vchr_name']=item.pop('fk_item__vchr_name')
                if item['dat_expiry']:
                    # item['dat_issue_edit']=ins_data['dat_issue']
                    item['dat_expiry']=item['dat_expiry'].strftime('%d-%m-%Y')
                item['coupon_type']=lst_package[item['int_which']]

            return Response({'status':1,'list':ListCoupon})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})

class ViewCoupon(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        try:

            int_id=request.GET.get('id')
            if Coupon.objects.filter(pk_bint_id=int_id):
                lst_coupon=list(Coupon.objects.filter(pk_bint_id=int_id).values('pk_bint_id','vchr_coupon_code','dat_expiry','int_discount_percentage','bint_max_discount_amt','bint_min_purchase_amt','int_max_usage_no',\
                'int_which','fk_product__vchr_name','fk_brand__vchr_name','fk_item_category__vchr_item_category','fk_item_group__vchr_item_group','fk_item__vchr_name','fk_product_id','fk_brand_id','fk_item_category_id','fk_item_group_id','fk_item_id'))

            lst_package=['All','Product','Brand','Item Category','Item Group','Item']
            lst_coupon[0]['package']=lst_package[lst_coupon[0]['int_which']]
            if lst_coupon[0]['dat_expiry']:
                    # item['dat_issue_edit']=ins_data['dat_issue']
                    lst_coupon[0]['dat_expiry']=lst_coupon[0]['dat_expiry']
            return Response({'status':1,'list':lst_coupon})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})

class EditCoupon(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            int_id=request.data.get('pk_bint_id')
            dat_expiry=request.data.get('datExpiry')
            dat_expiry=datetime.strptime(dat_expiry,"%Y-%m-%d")
            # import pdb;
            # pdb.set_trace()
            if Coupon.objects.filter(pk_bint_id=int_id):
                if(request.data.get('intWhich')==0):
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))

                elif request.data.get('intWhich')==1:
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),fk_product_id=request.data.get('fkPackage'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))

                elif request.data.get('intWhich')==2:
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),fk_brand_id=request.data.get('fkPackage'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))


                elif request.data.get('intWhich')==3:
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),fk_item_category_id=request.data.get('fkPackage'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))


                elif request.data.get('intWhich')==4:
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),fk_item_group_id=request.data.get('fkPackage'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))


                elif request.data.get('intWhich')==5:
                    Coupon.objects.filter(pk_bint_id=int_id).update(vchr_coupon_code=request.data.get('strCouponCode'),dat_expiry=dat_expiry,\
                    int_which=request.data.get('intWhich'),fk_item_id=request.data.get('fkPackage'),int_discount_percentage = request.data.get('intDiscountPercentage'),\
                    bint_max_discount_amt = request.data.get('bintMaxDiscountAmt'),bint_min_purchase_amt = request.data.get('bintMinPurchaseAmt'),int_max_usage_no = request.data.get('intMaxUsageNo'))


            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})


class ImportCoupon(APIView):
    permission_classes=[AllowAny]
    parser_classes = [MultiPartParser,FileUploadParser]
    serializer_class = Xlsserilzer
    def post(self,request):
        try:

            starttime=datetime.now()
            dct_product = dict(Products.objects.filter(int_status =0).annotate(name=Upper('vchr_name')).values_list('name','pk_bint_id'))
            dct_brand = dict(Brands.objects.filter(int_status =0).annotate(name=Upper('vchr_name')).values_list('name','pk_bint_id'))
            dct_item_category = dict(ItemCategory.objects.filter(int_status =0).annotate(name=Upper('vchr_item_category')).values_list('name','pk_bint_id'))
            dct_item_group = dict(ItemGroup.objects.filter(int_status =0).annotate(name=Upper('vchr_item_group')).values_list('name','pk_bint_id'))
            dct_item = dict(Item.objects.filter(int_status =0).annotate(code=Upper('vchr_item_code')).values_list('code','pk_bint_id'))
            lst_coupon = Coupon.objects.all().annotate(code=Upper('vchr_coupon_code')).values_list('code',flat=True)

            with transaction.atomic():
                lst_coupon_ins = []
                lst_pending_coup =[]
                lst_type = ['ALL','PRODUCT','BRAND','ITEMCATEGORY','ITEMGROUP','ITEM']
                files = request.FILES.get('files')
                Importfilesobj = ImportFiles(
                        vchr_file_name = files.name,
                        fk_uploaded_by = request.user.userdetails,
                        dat_uploaded = datetime.now(),
                        int_type = 1
                        )
                Importfilesobj.save()
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                if files:
                    str_filename = fs.save(files.name,files)
                    str_excel = fs.url(str_filename)

                df = pd.read_excel(settings.MEDIA_ROOT+'/'+str_filename)

                lst_coupon_codes=list(df['Code'])
                ins_coupon_code = set([x for x in lst_coupon_codes if lst_coupon_codes.count(x) > 1])
                str_coupon_codes=''
                if ins_coupon_code:
                    for x in ins_coupon_code:
                        str_coupon_codes=str(str_coupon_codes)+str(x)+''

                    return Response({'status':0,'reason':"Duplicate Coupon code : "+str_coupon_codes+"   exists!"})

                # df = pd.read_excel('demo.xlsx')
                for ind,row in df.iterrows():


                    if not str(row['Code'])== 'nan' and not str(row['Discount Amount'])== 'nan' and not str(row['Expiry Date'])== 'nan' and not str(row['Type'])== 'nan':
                        if str(row['Item Name'])== 'nan':
                            row['Name'] = None
                        if str(row['Item Code'])== 'nan':
                            row['Item Code'] = None
                        if str(row['Discount%'])== 'nan':
                            row['Discount%'] = 0
                        if str(row['Min Purchase Amount'])== 'nan':
                            row['Min Purchase Amount'] = 0

                        try:
                            row['Expiry Date']=datetime.strptime(row['Expiry Date'],'%d-%m-%Y')
                            dat_expiry=row['Expiry Date']
                        except:
                            try:
                                dat_expiry=datetime.strftime(row['Expiry Date'],'%Y-%m-%d')

                            except:
                                return Response({'status':0,'reason':" Date format not correct in Coupon code : "+str(row['Code'])})

                        if str(row['Code']).upper() in lst_coupon:
                        # if Coupon.objects.filter(vchr_coupon_code=str(row['Code'])):
                            return Response({'status':0,'reason':"Coupon code : "+str(row['Code'])+"  already exists!"})

                        if str(row['Type']).upper() in lst_type:
                            int_which = lst_type.index(str(row['Type']).upper())
                            if(int_which==0):

                                ins_coupon = Coupon(
                                                    vchr_coupon_code = str(row['Code']),
                                                    bint_max_discount_amt = row['Discount Amount'],
                                                    int_discount_percentage = row['Discount%'],
                                                    bint_min_purchase_amt = row['Min Purchase Amount'],
                                                    dat_expiry = dat_expiry,
                                                    int_which=int_which,
                                                    int_max_usage_no= 1,
                                                    dat_created = localtz.localize(datetime.now()))
                                lst_coupon_ins.append(ins_coupon)
                            elif(int_which==1):
                                ins_product = dct_product.get((str(row['Item Name']).upper()).split()[0])
                                # ins_product = Products.objects.filter(vchr_name__icontains=str(row['Item Name']),int_status =0).values('pk_bint_id').first()

                                if ins_product:

                                    ins_coupon = Coupon(
                                                        vchr_coupon_code = str(row['Code']),
                                                        bint_max_discount_amt = row['Discount Amount'],
                                                        int_discount_percentage = row['Discount%'],
                                                        bint_min_purchase_amt = row['Min Purchase Amount'],
                                                        dat_expiry = dat_expiry,
                                                        fk_product_id=ins_product,
                                                        int_which=int_which,
                                                        int_max_usage_no= 1,
                                                        dat_created = localtz.localize(datetime.now()))
                                    lst_coupon_ins.append(ins_coupon)
                                else:
                                    return Response({'status':0,'reason':"Some issues in the Coupon code : "+str(row['Code'])})
                                    lst_pending_coup.append(str(row['Code']))

                            elif(int_which==2):
                                ins_brand = dct_brand.get((str(row['Item Name']).upper()).split()[0])
                                # ins_brand = Brands.objects.filter(vchr_name__icontains=str(row['Item Name']),int_status =0).values('pk_bint_id').first()

                                if ins_brand:

                                    ins_coupon = Coupon(
                                                        vchr_coupon_code = str(row['Code']),
                                                        bint_max_discount_amt = row['Discount Amount'],
                                                        int_discount_percentage = row['Discount%'],
                                                        bint_min_purchase_amt = row['Min Purchase Amount'],
                                                        dat_expiry = dat_expiry,
                                                        fk_brand_id=ins_brand,
                                                        int_which=int_which,
                                                        int_max_usage_no= 1,
                                                        dat_created = localtz.localize(datetime.now()))
                                    lst_coupon_ins.append(ins_coupon)
                                else:
                                    return Response({'status':0,'reason':"Some issues in the Coupon code: "+str(row['Code'])})
                                    lst_pending_coup.append( str(row['Code']))
                            elif(int_which==3):
                                ins_item_category=dct_item_category.get(str((row['Item Name']).upper()).split()[0])
                                # ins_item_category = ItemCategory.objects.filter(vchr_item_category__icontains=str(row['Item Name']),int_status =0).values('pk_bint_id').first()
                                if ins_item_category:

                                    ins_coupon = Coupon(
                                                        vchr_coupon_code = str(row['Code']),
                                                        bint_max_discount_amt = row['Discount Amount'],
                                                        int_discount_percentage = row['Discount%'],
                                                        bint_min_purchase_amt = row['Min Purchase Amount'],
                                                        dat_expiry = dat_expiry,
                                                        fk_item_category_id=ins_item_category,
                                                        int_which=int_which,
                                                        int_max_usage_no= 1,
                                                        dat_created = localtz.localize(datetime.now()))
                                    lst_coupon_ins.append(ins_coupon)
                                else:
                                    return Response({'status':0,'reason':"Some issues in the Coupon code: "+str(row['Code'])})
                                    lst_pending_coup.append(str(row['Code']))
                            elif(int_which==4):


                                ins_item_group = dct_item_group.get((str(row['Item Name']).upper()).split()[0])
                                # ins_item_group = ItemGroup.objects.filter(vchr_item_group__icontains=str(row['Item Name']),int_status =0).values('pk_bint_id').first()
                                if ins_item_group:

                                    ins_coupon = Coupon(
                                                        vchr_coupon_code = str(row['Code']),
                                                        bint_max_discount_amt = row['Discount Amount'],
                                                        int_discount_percentage = row['Discount%'],
                                                        bint_min_purchase_amt = row['Min Purchase Amount'],
                                                        dat_expiry = dat_expiry,
                                                        fk_item_group_id=ins_item_group,
                                                        int_which=int_which,
                                                        int_max_usage_no= 1,
                                                        dat_created = localtz.localize(datetime.now()))
                                    lst_coupon_ins.append(ins_coupon)
                                else:
                                    return Response({'status':0,'reason':"Some issues in the Coupon code: "+str(row['Code'])})
                                    lst_pending_coup.append(str(row['Code']))
                            elif(int_which==5):

                                ins_item = dct_item.get((str(row['Item Code']).upper()).split()[0])
                                # ins_item = Item.objects.filter(Q(vchr_name__icontains=str(row['Item Name'])) & Q(vchr_item_code__icontains=str(row['Item Code'])),int_status =0).values('pk_bint_id').first()

                                if ins_item:
                                    ins_coupon = Coupon(
                                                        vchr_coupon_code = str(row['Code']),
                                                        bint_max_discount_amt = row['Discount Amount'],
                                                        int_discount_percentage = row['Discount%'],
                                                        bint_min_purchase_amt = row['Min Purchase Amount'],
                                                        dat_expiry = dat_expiry,
                                                        fk_item_id=ins_item,
                                                        int_which=int_which,
                                                        int_max_usage_no= 1,
                                                        dat_created = localtz.localize(datetime.now()))
                                    lst_coupon_ins.append(ins_coupon)
                                else:
                                    return Response({'status':0,'reason':"Some issues in the Coupon code: "+str(row['Code'])})
                                    lst_pending_coup.append(str(row['Code']))

                    else:
                        return Response({'status':0,'reason':"some fields not entered in row "+str(ind+2)})
                Coupon.objects.bulk_create(lst_coupon_ins)
                diff=datetime.now()-starttime

                return Response({'status':1,'diff':diff})
        except Exception as e:

                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                            return Response({'status':0,'reason':e})



class StaffCoupon(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:

            dict_product = StaffCouponMaster.objects.filter(int_status = 1).annotate(product_name = F('fk_product__vchr_name'),id = F('fk_product'),master_id = F('pk_bint_id')).values('product_name','id',"int_employee","int_not_employee","master_id")
            if dict_product:
                return Response({'status':1,'data':dict_product})
            return Response({'status':0,'reason':'no data found','data':[]})
        except Exception as e:
            return Response({'status':0,})
    def post(self,request):
        try:
            int_product =       request.data["product_id"]
            int_num_employee =  request.data['employee_number']
            int_num_promoter =  request.data['promoter_number']

            ins_master = StaffCouponMaster.objects.filter(fk_product_id = int_product,int_status = 1)
            if ins_master:
                return Response({'status':0,'reason':'coupon already exist'})
            else:
                StaffCouponMaster.objects.create(
                                                fk_product_id = int_product,
                                                int_employee = int_num_employee,
                                                int_not_employee = int_num_promoter,
                                                fk_created_id = request.user.id,
                                                dat_created = datetime.now(),
                                                int_status = 1
                )
                return Response({'status':1,'data':"insert succesfull"})
            return Response({'status':0,'reason':"master data not found"})
        except KeyError as e:
            return Response({'status':0,'reason':'KEY ERROR',"error_code":400})
        except Exception as e:
            return response({'status':0,'reason':e})

class Staffcoupondetails(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
        #     import pdb; pdb.set_trace()
            lst_brand = request.data.get('brand')
            lst_item_group = request.data.get('item_group')
            lst_item_category = request.data.get('item_category')

            flt_discount_percent = request.data['discount_percent']
            int_master = request.data['master_id']
            dct_filter = {}
            # if lst_brand:
            dct_filter['json_brand__contains'] = lst_brand
            # if lst_item_group:
            dct_filter['json_item_group__contains'] = lst_item_group

            # if lst_item_category:
            dct_filter['json_item_category__contains'] = lst_item_category

            if lst_brand or lst_item_category or lst_item_group:
                ins_details = StaffCouponDetails.objects.filter(**dct_filter)
                if ins_details:
                    return Response({'status':0,'reason':'coupon already exist'})



            ins_details = StaffCouponDetails(
                                fk_master_id            = int_master,
                                json_brand              = lst_brand,
                                json_item_category      = lst_item_category,
                                json_item_group         = lst_item_group,
                                dbl_discount_percent    = flt_discount_percent
            )
            ins_details.save()
            if ins_details:
                return Response({'status':1,'reason':'success'})
            return Response({'status':0,'reason':'failed'})


        except Exception as e:
            return Response({'status':0,'reason':e})


class StaffcoupondetailsMobile(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            int_coupon_id = request.data.get('masterId')
            # import pdb; pdb.set_trace()
            # int_coupon_id = 1
            if not int_coupon_id:
                bool_staff =  request.data.get('isStaff')
                if bool_staff:
                    dct_coupon = StaffCouponMaster.objects.filter(int_status = 1,int_employee__isnull=False ).annotate(coupon_number = F('int_employee'),product_name = F('fk_product__vchr_name')).values('coupon_number','pk_bint_id','product_name')
                else:
                    dct_coupon = StaffCouponMaster.objects.filter(int_status = 1,int_not_employee__isnull=False ).annotate(coupon_number = F('int_not_employee'),product_name = F('fk_product__vchr_name')).values('coupon_number','pk_bint_id','product_name')
                return Response({'status':1,"data":dct_coupon})
            else:
                lst_data=[]
                ins_discount = StaffCouponDetails.objects.filter(fk_master_id = int(int_coupon_id)).values()
                for dct_item in ins_discount:
                    dct_data={}
                    dct_data['lst_brand'] = ''
                    dct_data['lst_item_cat'] = ''
                    dct_data['lst_item_grp'] = ''
                    dct_data['dbl_discount_percent'] = dct_item['dbl_discount_percent']
                    dct_data['pk_bint_id'] = dct_item['pk_bint_id']
                    dct_data['blnvar'] = False
                    if dct_item['json_brand']:
                        dct_brand = Brands.objects.filter(pk_bint_id__in = dct_item['json_brand']).values_list('vchr_name')
                        dct_data['lst_brand'] = ','.join(i[0].title() for i in dct_brand)
                    if dct_item['json_item_category']:
                        dct_item_cat = ItemCategory.objects.filter(pk_bint_id__in = dct_item['json_item_category']).values_list('vchr_item_category')
                        dct_data['lst_item_cat'] = ','.join(i[0].title() for i in dct_item_cat)
                    if dct_item['json_item_group']:
                        dct_itm_grp = ItemGroup.objects.filter(pk_bint_id__in = dct_item['json_item_group']).values_list('vchr_item_group')
                        dct_data['lst_item_grp'] = ','.join(i[0].title() for i in dct_itm_grp)
                    lst_data.append(dct_data)
                if ins_discount:
                    return Response({"status":1,'data':lst_data})
                else:
                    return Response({"status":0,'data':[]})
        except Exception as e:
            return Response({'reason':e,"status":"0"})


class ItemsData(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_product = request.data['product_id']
            lst_brands = request.data['brands']

            dct_itemcat = Item.objects.filter(fk_product_id = int_product,fk_brand_id__in = lst_brands).annotate(id = F("fk_item_category_id"),item_category = F("fk_item_category__vchr_item_category")).values("id","item_category")
            dct_group = Item.objects.filter(fk_product_id = int_product,fk_brand_id__in = lst_brands).annotate(id = F("fk_item_group_id"),item_group = F("fk_item_group__vchr_item_group")).values("id","item_group")
            return Response({"status":1,'item_category':dct_itemcat,'item_group':dct_group})
        except Exception as e:
            return Response({'reason':e,"status":"0"})
