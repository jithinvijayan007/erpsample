from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import HttpResponse
from .models import AddComboMaster,AddComboDiscount,AddComboDiscountItem

from sqlalchemy.orm import sessionmaker,aliased
from sqlalchemy import and_,func ,cast,DATE,case,distinct,Date
from aldjemy.core import get_engine
from django.db.models import Value, CharField, BooleanField, IntegerField, FloatField, Case, When
import datetime
from item_category.models import Item
from brands.models import Brands
from django.contrib.auth.models import User
from branch.models import Branch
from pricelist.models import PriceList
from django.db.models import Q
from collections import OrderedDict



AddComboMasterSA = AddComboMaster.sa
AddComboDiscountSA = AddComboDiscount.sa
AddComboDiscountItemSA = AddComboDiscountItem.sa
ItemsSA =  Item.sa
BrandsSA = Brands.sa

def Session():
    from aldjemy.core import get_engine
    engine=get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()

# Create your views here.
class AddCombo(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:

            # import pdb; pdb.set_trace()

            data = request.data.get('data')
            user_name = request.data.get('user')
            user = User.objects.filter(username = user_name,is_active=True).all().first()
            #if offer type is item wise
            # if request.data.get("intCategory") == '1':
            if data['intCategory'] == '1':
                # print(request.data.get("intCategory"))
                # item_quantity = request.data.get("intQty")
                # item_id = request.data.get("intItem")
                # offer_name = request.data.get("strOfferName")

                item_quantity = data['intQty']
                item_id = Item.objects.filter(vchr_item_code = data['intItem']).values('pk_bint_id').first()['pk_bint_id']
                offer_name = data['strOfferName']

                # dat_to = (datetime.datetime.strptime(request.data.get("datTo")[:10],'%Y-%m-%d')).date()
                # dat_from = (datetime.datetime.strptime(request.data.get("datFrom")[:10],'%Y-%m-%d')).date()

                dat_to = (datetime.datetime.strptime(data['datTo'][:10],'%Y-%m-%d')).date()
                dat_from = (datetime.datetime.strptime(data['datFrom'][:10],'%Y-%m-%d')).date()

                #if discount type is  on percentage
                # if request.data.get("intDisType") == '1':
                if data['intDisType'] == '1':
                    # print(request.data.get("intDisType"))
                    # fl_discount_percent = request.data.get("intDisPer")
                    # fl_discount_percent = request.data.get("intDisPer")
                    fl_discount_percent = data["intDisPer"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_item_id = item_id
                    ins_item_offer.int_quantity = item_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    # ins_item_offer.fk_company_id = request.user.userdetails.fk_company_id
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data["intDisType"])
                    ins_item_discount.dbl_percent = fl_discount_percent
                    ins_item_discount.save()

                #if discount type is on amount
                # if request.data.get("intDisType") == '2':
                if data['intDisType'] == '2':
                    # print(request.data.get("intDisType"))
                    # dis_amount = request.data.get("intDisAmt")
                    dis_amount = data["intDisAmt"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_item_id = item_id
                    ins_item_offer.int_quantity = item_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.dbl_amt= dis_amount
                    ins_item_discount.save()

                #if discount type is on item
                # if request.data.get("intDisType") == '3':
                if data['intDisType'] == '3':
                    # print(request.data.get("intDisType"))

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_item_id = item_id
                    ins_item_offer.int_quantity = item_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.save()
                    # import pdb; pdb.set_trace()

                    # for item_data in request.data.get("lstDisItem"):
                    for item_data in data["lstDisItem"]:
                        ins_item_discount_item = AddComboDiscountItem()
                        ins_item_discount_item.fk_master_id = ins_item_discount.pk_bint_id
                        ins_item_discount_item.int_quantity = item_data['intDisQty']
                        ins_item_discount_item.fk_item_id = Item.objects.filter(vchr_item_code = item_data['intDisItem']).values('pk_bint_id').first()['pk_bint_id']
                        if item_data['intItemPer']:
                            ins_item_discount_item.dbl_percent = item_data['intItemPer']
                        elif item_data['intItemAmt']:
                            ins_item_discount_item.dbl_amt = item_data['intItemAmt']
                        ins_item_discount_item.save()


            #if offer type is Brand wise
            # elif request.data.get("intCategory") == '2':
            elif data['intCategory'] == '2':
                # print(request.data.get("intCategory"))
                # brand_quantity = request.data.get("intQty")
                # brand_id = request.data.get("intBrand")
                # offer_name = request.data.get("strOfferName")

                brand_quantity = data["intQty"]
                brand_id = Brands.objects.filter(vchr_name__iexact = data["intBrand"]).values('pk_bint_id').first()['pk_bint_id']
                offer_name = data["strOfferName"]

                # dat_to = (datetime.datetime.strptime(request.data.get("datTo")[:10],'%Y-%m-%d')).date()
                # dat_from = (datetime.datetime.strptime(request.data.get("datFrom")[:10],'%Y-%m-%d')).date()

                dat_to = (datetime.datetime.strptime(data["datTo"][:10],'%Y-%m-%d')).date()
                dat_from = (datetime.datetime.strptime(data["datFrom"][:10],'%Y-%m-%d')).date()

                #if discount type is  on percentage
                # if request.data.get("intDisType") == '1':
                if data['intDisType'] == '1':
                    # print(request.data.get("intDisType"))
                    fl_discount_percent = data["intDisPer"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_brand_id = brand_id
                    ins_item_offer.int_quantity = brand_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.dbl_percent = fl_discount_percent
                    ins_item_discount.save()

                #if discount type is on amount
                # if request.data.get("intDisType") == '2':
                if data['intDisType'] == '2':
                    # print(request.data.get("intDisType"))
                    # dis_amount = request.data.get("intDisAmt")
                    dis_amount = data["intDisAmt"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_brand_id = brand_id
                    ins_item_offer.int_quantity = brand_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.dbl_amt= dis_amount
                    ins_item_discount.save()

                #if discount type is on item
                # if request.data.get("intDisType") == '3':
                if data['intDisType'] == '3':
                    # print(request.data.get("intDisType"))

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.fk_brand_id = brand_id
                    ins_item_offer.int_quantity = brand_quantity
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.save()
                    # import pdb; pdb.set_trace()

                    # for item_data in request.data.get("lstDisItem"):
                    for item_data in data["lstDisItem"]:
                        ins_item_discount_item = AddComboDiscountItem()
                        ins_item_discount_item.fk_master_id = ins_item_discount.pk_bint_id
                        ins_item_discount_item.int_quantity = item_data['intDisQty']
                        ins_item_discount_item.fk_item_id = Item.objects.filter(vchr_item_code = item_data['intDisItem']).values('pk_bint_id').first()['pk_bint_id']
                        if item_data['intItemPer']:
                            ins_item_discount_item.dbl_percent = item_data['intItemPer']
                        elif item_data['intItemAmt']:
                            ins_item_discount_item.dbl_amt = item_data['intItemAmt']
                        ins_item_discount_item.save()


            #if offer type is Amount wise
            # elif request.data.get("intCategory") == '3':
            elif data['intCategory'] == '3':
                # print(request.data.get("intCategory"))

                # amount = request.data.get("intAmt")
                # offer_name = request.data.get("strOfferName")
                # dat_to = (datetime.datetime.strptime(request.data.get("datTo")[:10],'%Y-%m-%d')).date()
                # dat_from = (datetime.datetime.strptime(request.data.get("datFrom")[:10],'%Y-%m-%d')).date()

                amount = data["intAmt"]
                offer_name = data["strOfferName"]
                dat_to = (datetime.datetime.strptime(data["datTo"][:10],'%Y-%m-%d')).date()
                dat_from = (datetime.datetime.strptime(data["datFrom"][:10],'%Y-%m-%d')).date()

                #if discount type is  on percentage
                # if request.data.get("intDisType") == '1':
                if data['intDisType'] == '1':
                    # print(request.data.get("intDisType"))
                    # fl_discount_percent = request.data.get("intDisPer")
                    fl_discount_percent = data["intDisPer"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.dbl_amt = amount
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.dbl_percent = fl_discount_percent
                    ins_item_discount.save()

                #if discount type is on amount
                # if request.data.get("intDisType") == '2':
                if data['intDisType'] == '2':
                    # print(request.data.get("intDisType"))
                    # dis_amount = request.data.get("intDisAmt")
                    dis_amount = data["intDisAmt"]

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.dbl_amt = amount
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.dbl_amt= dis_amount
                    ins_item_discount.save()

                #if discount type is on item
                # if request.data.get("intDisType") == '3':
                if data['intDisType'] == '3':
                    # print(request.data.get("intDisType"))

                    ins_item_offer = AddComboMaster()
                    # ins_item_offer.int_offer_type = request.data.get("intCategory")
                    ins_item_offer.int_offer_type = data["intCategory"]
                    ins_item_offer.vchr_offer_name = offer_name
                    ins_item_offer.dbl_amt = amount
                    ins_item_offer.dat_to = dat_to
                    ins_item_offer.dat_from =dat_from
                    ins_item_offer.fk_company_id = user.userdetails.fk_company_id
                    ins_item_offer.save()

                    ins_item_discount = AddComboDiscount()
                    ins_item_discount.fk_master_id = ins_item_offer.pk_bint_id
                    # ins_item_discount.int_discount_type = int(request.data.get("intDisType"))
                    ins_item_discount.int_discount_type = int(data['intDisType'])
                    ins_item_discount.save()
                    # import pdb; pdb.set_trace()

                    # for item_data in request.data.get("lstDisItem"):
                    for item_data in data["lstDisItem"]:
                        ins_item_discount_item = AddComboDiscountItem()
                        ins_item_discount_item.fk_master_id = ins_item_discount.pk_bint_id
                        ins_item_discount_item.int_quantity = item_data['intDisQty']
                        ins_item_discount_item.fk_item_id = Item.objects.filter(vchr_item_code = item_data['intDisItem']).values('pk_bint_id').first()['pk_bint_id']
                        if item_data['intItemPer']:
                            ins_item_discount_item.dbl_percent = item_data['intItemPer']
                        elif item_data['intItemAmt']:
                            ins_item_discount_item.dbl_amt = item_data['intItemAmt']
                        ins_item_discount_item.save()
            # import pdb; pdb.set_trace()

            return Response({'status':1})

        except Exception as e:
            return Response({'status':0,'data':str(e)})


class ListCombo(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:

            session=Session()
            #listing all combo offers
            # import pdb; pdb.set_trace()
            dat_to = (datetime.datetime.strptime(request.data.get("datTo")[:10],'%Y-%m-%d')).date()
            dat_from = (datetime.datetime.strptime(request.data.get("datFrom")[:10],'%Y-%m-%d')).date()
            rst_lst_combo_offers_all = session.query(AddComboMasterSA.vchr_offer_name.label('offer_name'),\
                                            AddComboMasterSA.int_offer_type.label('offer_type'),\
                                            AddComboMasterSA.pk_bint_id.label('master_id'),\
                                            AddComboDiscountSA.int_discount_type.label('discount_type'))\
                                            .join(AddComboDiscountSA,AddComboDiscountSA.fk_master_id == AddComboMasterSA.pk_bint_id)\
                                            .filter(and_(cast(AddComboMasterSA.dat_from,DATE)>= dat_from,cast(AddComboMasterSA.dat_to,DATE)<= dat_to))\
                                            .filter(AddComboMasterSA.int_status >= 0)\
                                            .order_by(AddComboMasterSA.dat_from)
            # print(rst_lst_combo_offers_all.all())
            #structuring the combo offers
            lst_view_offer = []
            for ins_offer in rst_lst_combo_offers_all:
                dct_view_offer = {}
                dct_view_offer['offer_id'] = ins_offer.master_id
                dct_view_offer['offer_name'] = ins_offer.offer_name
                if ins_offer.offer_type == 1:
                    dct_view_offer['offer_type'] = "ITEM WISE"
                elif ins_offer.offer_type == 2:
                    dct_view_offer['offer_type'] = "BRAND WISE"
                elif ins_offer.offer_type == 3:
                    dct_view_offer['offer_type'] = "AMOUNT"
                if ins_offer.discount_type == 1:
                    dct_view_offer['discount_type'] = "PERCENTAGE"
                elif ins_offer.discount_type == 2:
                    dct_view_offer['discount_type'] = "AMOUNT"
                elif ins_offer.discount_type == 3:
                    dct_view_offer['discount_type'] = "ITEM"
                lst_view_offer.append(dct_view_offer)

            # print(lst_view_offer)
            session.close()
            return Response({'status':1 , 'lst_view_offer' :lst_view_offer })

        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})



class ListDetailedCombo(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:

            session=Session()
            #listing all combo offers with details
            # import pdb; pdb.set_trace()
            int_offer_id = request.data.get("id")
            # int_offer_id = 41
            rst_lst_combo_offers_all = session.query(AddComboMasterSA.vchr_offer_name.label('offer_name'),\
                                            AddComboMasterSA.int_offer_type.label('offer_type'),\
                                            AddComboMasterSA.pk_bint_id.label('master_id'),\
                                            AddComboMasterSA.int_quantity.label('int_quantity'),\
                                            AddComboDiscountSA.int_discount_type.label('discount_type'),\
                                            ItemsSA.vchr_item_name.label('item_name'),\
                                            AddComboMasterSA.fk_item_id.label('item_id'),\
                                            BrandsSA.vchr_brand_name.label('brand_name'),\
                                            AddComboMasterSA.fk_brand_id.label('brand_id'),\
                                            AddComboMasterSA.dbl_amt.label('offer_amount'),\
                                            AddComboDiscountSA.dbl_amt.label('discount_amount'),\
                                            AddComboDiscountSA.dbl_percent.label('discount_percent'),\
                                            AddComboDiscountSA.pk_bint_id.label('discount_table_id'))\
                                            .join(AddComboDiscountSA,AddComboDiscountSA.fk_master_id == AddComboMasterSA.pk_bint_id)\
                                            .outerjoin(ItemsSA,ItemsSA.id == AddComboMasterSA.fk_item_id)\
                                            .outerjoin(BrandsSA, BrandsSA.id == AddComboMasterSA.fk_brand_id)\
                                            .filter(AddComboMasterSA.pk_bint_id == int_offer_id)
            # print(rst_lst_combo_offers_all.all())
            #structuring the combo offers
            lst_view_offer = []
            for ins_offer in rst_lst_combo_offers_all.all():
                dct_view_offer = {}
                dct_view_offer['offer_id'] = ins_offer.master_id
                dct_view_offer['offer_name'] = ins_offer.offer_name
                dct_view_offer['int_quantity'] = ins_offer.int_quantity
                if ins_offer.offer_type == 1:
                    dct_view_offer['offer_type'] = "ITEM WISE"
                    dct_view_offer['int_offer_type'] = ins_offer.offer_type
                    dct_view_offer['item_name'] = ins_offer.item_name
                    dct_view_offer['item_id'] = ins_offer.item_id
                elif ins_offer.offer_type == 2:
                    dct_view_offer['offer_type'] = "BRAND WISE"
                    dct_view_offer['int_offer_type'] = ins_offer.offer_type
                    dct_view_offer['brand_name'] = ins_offer.brand_name
                    dct_view_offer['brand_id'] = ins_offer.brand_id
                elif ins_offer.offer_type == 3:
                    dct_view_offer['offer_type'] = "AMOUNT"
                    dct_view_offer['int_offer_type'] = ins_offer.offer_type
                    dct_view_offer['offer_amount'] = ins_offer.offer_amount
                if ins_offer.discount_type == 1:
                    dct_view_offer['discount_type'] = "PERCENTAGE"
                    dct_view_offer['int_discount_type'] = str(ins_offer.discount_type)
                    dct_view_offer['discount_percent'] = ins_offer.discount_percent
                elif ins_offer.discount_type == 2:
                    dct_view_offer['discount_type'] = "AMOUNT"
                    dct_view_offer['int_discount_type'] = str(ins_offer.discount_type)
                    dct_view_offer['discount_amount'] = ins_offer.discount_amount
                elif ins_offer.discount_type == 3:
                    dct_view_offer['discount_type'] = "ITEM"
                    dct_view_offer['int_discount_type'] = str(ins_offer.discount_type)
                    rst_lst_discount_items = session.query(AddComboDiscountItemSA.int_quantity.label('int_quantity'),\
                                                AddComboDiscountItemSA.dbl_amt.label('item_discount_amount'),\
                                                AddComboDiscountItemSA.dbl_percent.label('item_discount_percentage'),\
                                                AddComboDiscountItemSA.fk_item_id.label('item_id'),\
                                                ItemsSA.vchr_item_name.label('item_name'))\
                                                .join(ItemsSA,ItemsSA.id == AddComboDiscountItemSA.fk_item_id)\
                                                .filter(AddComboDiscountItemSA.fk_master_id == ins_offer.discount_table_id)
                    lst_discount_item =[]
                    for ins_discount_items in rst_lst_discount_items.all():
                        dct_item_list = {}
                        dct_item_list['item_name'] = ins_discount_items.item_name
                        dct_item_list['item_id'] = ins_discount_items.item_id
                        dct_item_list['int_quantity'] = ins_discount_items.int_quantity
                        if ins_discount_items.item_discount_amount:
                            dct_item_list['item_discount_amount'] = ins_discount_items.item_discount_amount
                        else:
                            dct_item_list['item_discount_percentage'] = ins_discount_items.item_discount_percentage
                        lst_discount_item.append(dct_item_list)
                    dct_view_offer['item_list'] = lst_discount_item
                    # print(lst_discount_item)
                lst_view_offer.append(dct_view_offer)

            # print(lst_view_offer)
            session.close()
            return Response({'status':1 , 'lst_view_offer' :lst_view_offer })

        except Exception as e:
            session.close()
            return Response({'status':0,'data':str(e)})


class DeleteCombo(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        # import pdb; pdb.set_trace()
        try:
            int_offer_id = request.data.get("id")
            vchr_offer_name = request.data.get('vchr_offer_name')
            int_offer_type = request.data.get('int_offer_type')
            dat_from = request.data.get('dat_from')
            dat_to = request.data.get('dat_to')
            if vchr_offer_name:
                ins_item_offer = AddComboMaster.objects.filter(vchr_offer_name = vchr_offer_name,int_offer_type = int_offer_type,dat_from = dat_from,dat_to = dat_to).update(int_status = -1)
                if not ins_item_offer:
                    return Response({'status':0, 'data': 'no offer selected'})
            else:
                return Response({'status':0, 'data': 'no offer selected'})
            return Response({'status':1})

        except Exception as e:
            return Response({'status':0,'data':str(e)})



class ItemOffers(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            item_id = request.data.get('itemId')

            """brand for knowing offers for brands"""
            ins_brand = Item.objects.filter(pk_bint_id = item_id).values('fk_brand_id').first()['fk_brand_id']
            """price template of branch and amount respect to price template"""
            ins_branch_template = Branch.objects.filter(pk_bint_id = request.user.userdetails.fk_branch_id).values('int_price_template').first()['int_price_template']

            ins_amount = PriceList.objects.filter(fk_item_id = item_id, int_status = 0, dat_efct_from__lte = datetime.datetime.now()).values('pk_bint_id').annotate(int_branch_template = Value(ins_branch_template, IntegerField())).annotate(dbl_amount = Case(When(int_branch_template = 0, then = 'dbl_cost_amnt'), When(int_branch_template = 1, then = 'dbl_dealer_amt'), When(int_branch_template = 2, then = 'dbl_mop'), When(int_branch_template = 3, then = 'dbl_my_amt'), When(int_branch_template = 4, then = 'dbl_mrp'), default = 0.0, output_field = FloatField())).order_by('dat_efct_from').first()
            if ins_amount:
                ins_amount = ins_amount['dbl_amount']
            else:
                ins_amount = 0
            # if ins_branch_template == 0:
            #     ins_amount = PriceList.objects.filter(fk_item_id = item_id).values('dbl_cost_amnt').first()['dbl_cost_amnt']
            # elif ins_branch_template == 1:
            #     ins_amount = PriceList.objects.filter(fk_item_id = item_id).values('dbl_dealer_amt').first()['dbl_dealer_amt']
            # elif ins_branch_template == 2:
            #     ins_amount = PriceList.objects.filter(fk_item_id = item_id).values('dbl_mop').first()['dbl_mop']
            # elif ins_branch_template == 3:
            #     ins_amount = PriceList.objects.filter(fk_item_id = item_id).values('dbl_my_amt').first()['dbl_my_amt']
            # elif ins_branch_template == 4:
            #     ins_amount = PriceList.objects.filter(fk_item_id = item_id).values('dbl_mrp').first()['dbl_mrp']


            ins_item_offers = AddComboMaster.objects.filter(dat_to__gte = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'),dat_from__lte = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')).values('pk_bint_id','int_offer_type','vchr_offer_name','fk_item_id','fk_brand_id','dbl_amt','int_quantity','dat_to','dat_from').exclude(int_status = -1)

            ins_item_offers = ins_item_offers.filter(Q(fk_item_id = item_id) | Q(fk_brand_id = ins_brand) | Q(dbl_amt__lte = ins_amount))



            dct_offer_data = {}
            if ins_item_offers:
                for ins_combo_master in ins_item_offers:
                    dct_offer_data[ins_combo_master['pk_bint_id']] = {}
                    dct_offer_data[ins_combo_master['pk_bint_id']]['vchr_offer_name'] = ins_combo_master['vchr_offer_name']
                    dct_offer_data[ins_combo_master['pk_bint_id']]['pk_bint_id'] = ins_combo_master['pk_bint_id']
                    dct_offer_data[ins_combo_master['pk_bint_id']]['int_offer_type'] = ins_combo_master['int_offer_type']
                    dct_offer_data[ins_combo_master['pk_bint_id']]['datTo'] = datetime.datetime.strftime(ins_combo_master['dat_to'],"%d %b %Y")
                    dct_offer_data[ins_combo_master['pk_bint_id']]['datFrom'] = datetime.datetime.strftime(ins_combo_master['dat_from'],"%d %b %Y")

                    if ins_combo_master['int_offer_type'] == 1: #offer on item
                        dct_offer_data[ins_combo_master['pk_bint_id']]['vchr_offer_type'] = "Item Wise"
                        dct_offer_data[ins_combo_master['pk_bint_id']]['fk_item_id'] = ins_combo_master['fk_item_id']
                        dct_offer_data[ins_combo_master['pk_bint_id']]['int_quantity'] = ins_combo_master['int_quantity']
                    elif ins_combo_master['int_offer_type'] == 2: #offer on brand
                        dct_offer_data[ins_combo_master['pk_bint_id']]['vchr_offer_type'] = "Brand Wise"
                        dct_offer_data[ins_combo_master['pk_bint_id']]['fk_brand_id'] = ins_combo_master['fk_brand_id']
                        dct_offer_data[ins_combo_master['pk_bint_id']]['int_quantity'] = ins_combo_master['int_quantity']
                    elif ins_combo_master['int_offer_type'] == 3:#offer on amount
                        dct_offer_data[ins_combo_master['pk_bint_id']]['vchr_offer_type'] = "Amount Wise"
                        dct_offer_data[ins_combo_master['pk_bint_id']]['dbl_amt'] = ins_combo_master['dbl_amt']

                ins_discount_data = list(AddComboDiscount.objects.filter(fk_master_id__in = (dct_offer_data.keys())).values('pk_bint_id','fk_master_id','int_discount_type','dbl_amt','dbl_percent'))

                for ins_combo_discount in  ins_discount_data:
                    dct_offer_data[ins_combo_discount['fk_master_id']]['discount'] = {}
                    dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']] = {}
                    dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['int_discount_type'] = ins_combo_discount['int_discount_type']
                    if ins_combo_discount['int_discount_type'] == 1:#discount giving as percentage
                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['vchr_discount_type'] = "PERCENTAGE"
                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['dbl_percent'] = ins_combo_discount['dbl_percent']
                    if ins_combo_discount['int_discount_type'] == 2:#discount giving as amount
                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['vchr_discount_type'] = "AMOUNT"
                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['dbl_amt'] = ins_combo_discount['dbl_amt']
                    if ins_combo_discount['int_discount_type'] == 3:#discount giving as items
                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['vchr_discount_type'] = "ITEM"
                        #getting discount items
                        ins_items = list(AddComboDiscountItem.objects.filter(fk_master_id = ins_combo_discount['pk_bint_id']).values('pk_bint_id','fk_item_id','fk_item__vchr_item_code','fk_item__vchr_name','dbl_amt','dbl_percent','int_quantity'))

                        dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items']={}
                        for ins_discount_item in ins_items:
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]={}
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]['fk_item__vchr_name'] = ins_discount_item['fk_item__vchr_name']
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]['fk_item_id'] = ins_discount_item['fk_item_id']
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]['int_quantity'] = ins_discount_item['int_quantity']
                            # if ins_discount_item['']
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]['dbl_amt'] = ins_discount_item['dbl_amt']
                            dct_offer_data[ins_combo_discount['fk_master_id']]['discount'][ins_combo_discount['pk_bint_id']]['discount_items'][ins_discount_item['pk_bint_id']]['dbl_percent'] = ins_discount_item['dbl_percent']

                dct_offer_data = paginate_data_index(dct_offer_data,4)

            else:
                return Response({'status' : 1 , 'reason' : "no offers available" , 'data' : {} })

            return Response({'status':1 , 'data' : dct_offer_data})

        except Exception as e :
            return Response({'status':0,'data':str(e)})


def paginate_data_index(dct_data,int_page_legth):
    dct_paged = {}
    int_count = 1
    dct_data = OrderedDict(dct_data)
    for key in dct_data:
        if int_count not in dct_paged:
            dct_paged[int_count]={}
            index = len(dct_paged[int_count])
            dct_paged[int_count][index]=dct_data[key]
        elif len(dct_paged[int_count]) < int_page_legth:
            index = len(dct_paged[int_count])
            dct_paged[int_count][index]= dct_data[key]
        else:
            int_count += 1
            dct_paged[int_count] ={}
            index = len(dct_paged[int_count])
            dct_paged[int_count][index] = dct_data[key]
    return dct_paged
