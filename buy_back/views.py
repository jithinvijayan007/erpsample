from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from CRM import ins_logger
from .models import BuyBack
from django.db.models import Q
from inventory.models import ItemGroup,Items

# Create your views here.
class AddBuyBack(APIView):
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            dat_from = datetime.strptime(request.data.get('datFrom'), '%d/%m/%Y' )
            dat_to = datetime.strptime(request.data.get('datTo'), '%d/%m/%Y' )
            int_group_id = request.data.get('intItemId')
            dbl_amount = request.data.get('dblAmount')
            lst_instan=[]
            lst_item=Items.objects.filter(fk_item_group_id=int_group_id).values_list('id',flat=True)
            BuyBack.objects.filter(fk_item_id__in=lst_item).update(int_status = 0)
            for int_item_id in lst_item:
                ins_buyback=BuyBack(dat_start=dat_from, dat_end=dat_to, fk_item_id=int_item_id, dbl_amount=dbl_amount)
                lst_instan.append(ins_buyback)
            BuyBack.objects.bulk_create(lst_instan)

            # BuyBack.objects.create(dat_start=dat_from, dat_end=dat_to, fk_item_id=int_item_id, dbl_amount=dbl_amount)

            return Response({'status':'success'})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})

    def patch(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_buyback_id = request.data.get('intBuybackId')
            dat_from = datetime.strptime(request.data.get('datFrom'), '%d/%m/%Y' )
            dat_to = datetime.strptime(request.data.get('datTo'), '%d/%m/%Y' )
            int_item_id = request.data.get('intItemId')
            dbl_amount = request.data.get('dblAmount')
            if int_buyback_id == int_item_id:
                BuyBack.objects.filter(fk_item__fk_item_group_id=int_buyback_id,int_status=1).update(dat_start=dat_from, dat_end=dat_to, dbl_amount=dbl_amount)
            else:
                lst_instan=[]
                BuyBack.objects.filter(fk_item__fk_item_group_id=int_buyback_id).update(int_status = 0)
                lst_item=Items.objects.filter(fk_item_group_id=int_item_id).values_list('id',flat=True)
                for item_id in lst_item:
                    ins_buyback=BuyBack(dat_start=dat_from, dat_end=dat_to, fk_item_id=item_id, dbl_amount=dbl_amount)
                    lst_instan.append(ins_buyback)
                BuyBack.objects.bulk_create(lst_instan)
            return Response({'status':'success'})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})

    def put(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_buyback_id = request.data.get('intBuybackId')
            BuyBack.objects.filter(fk_item__fk_item_group_id=int_buyback_id).update(int_status=-1)
            # BuyBack.objects.filter(pk_bint_id=int_buyback_id).update(int_status=-1)
            return Response({'status':'success'})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})


class BuyBackView(APIView):
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_buyback_id = request.data.get('intBuybackId')
            ins_buyback = BuyBack.objects.filter(fk_item__fk_item_group_id=int_buyback_id,int_status=1).values('dat_start','dat_end','fk_item__fk_item_group_id','fk_item__fk_item_group__vchr_item_group','dbl_amount').first()
            dct_data = {}
            dct_data['datStart'] = ins_buyback['dat_start']
            dct_data['datEnd'] = ins_buyback['dat_end']
            dct_data['intItemId'] = ins_buyback['fk_item__fk_item_group_id']
            dct_data['strItemName'] = ins_buyback['fk_item__fk_item_group__vchr_item_group']
            dct_data['dblAmount'] = ins_buyback['dbl_amount']
            return Response({'status':'success','data':dct_data})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})


class BuyBackList(APIView):
    def post(self,request):
        try:
            dat_from = datetime.strptime(request.data.get('datFrom'), '%d/%m/%Y' )
            dat_to = datetime.strptime(request.data.get('datTo'), '%d/%m/%Y' )
            ins_buyback = BuyBack.objects.filter(Q(dat_start__range=(dat_from,dat_to))|Q(dat_end__range=(dat_from,dat_to))|Q(dat_start__lte=dat_from,dat_end__gte=dat_from)|Q(dat_start__lte=dat_to,dat_end__gte=dat_to),int_status=1).values('pk_bint_id','dat_start','dat_end','fk_item__vchr_item_name','dbl_amount','fk_item__fk_item_group__vchr_item_group','fk_item__fk_item_group_id').order_by('-pk_bint_id')
            if request.data.get('intItemId'):

                ins_buyback = ins_buyback.filter(fk_item__fk_item_group_id=request.data.get('intItemId'))
            lst_buyback_data = []
            lst_temp=[]
            for ins_data in ins_buyback:
                if ins_data['fk_item__fk_item_group_id'] not in lst_temp:
                    dct_data = {}
                    dct_data['intId'] = ins_data['fk_item__fk_item_group_id']
                    dct_data['datFrom'] = ins_data['dat_start'].strftime("%d-%m-%Y")
                    dct_data['datTo'] = ins_data['dat_end'].strftime("%d-%m-%Y")
                    dct_data['strItemName'] = ins_data['fk_item__fk_item_group__vchr_item_group']
                    dct_data['dblAmount'] = ins_data['dbl_amount']
                    lst_temp.append(ins_data['fk_item__fk_item_group_id'])
                    lst_buyback_data.append(dct_data)
            # import pdb; pdb.set_trace()
            return Response({'status':'success','data':lst_buyback_data})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})


class GetItemBuyback(APIView):
    def post(self,request):
        try:
            int_item_id = request.data.get('intItemId')
            ins_buyback = BuyBack.objects.filter(int_status__gte=0,fk_item_id=int_item_id,dat_start__gte=datetime.now(),dat_end__lte=datetime.now()).values('dbl_amount').last()
            dbl_amount = 0
            if ins_buyback:
                dbl_amount = ins_buyback['dbl_amount']
            return Response({'status':'success','data':dbl_amount})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':'failed'})
