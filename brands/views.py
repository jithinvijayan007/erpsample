from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from brands.models import Brands
from django.db.models import Q
# Create your views here.

class AddBrands(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        '''list all brands'''
        try:
            lst_brand = list(Brands.objects.filter(int_status=0).values('pk_bint_id','vchr_code','vchr_name').order_by('vchr_name'))
            return Response({'status':1,'data':lst_brand})
        except Exception as e:
            return Response({'status':0,'reason':e})

    def post(self,request):
        '''add brands'''
        try:
            str_name = request.data.get('strBrand')
            str_code = request.data.get('strCode')
            if Brands.objects.filter(vchr_name=str_name,vchr_code=str_code,int_status=0):
                return Response({'status':0,'reason':'already exists'})
            else:
                Brands.objects.create(vchr_name=str_name,vchr_code=str_code,int_status=0,fk_company_id = 1)
            return Response({'status':1,'message':'created successfully'})
        except Exception as e:
            return Response({'status':0,'reason':e})

    def put(self,request):
        '''edit brand'''
        try:
            int_brand_id = request.data.get('intId')
            str_name = request.data.get('strName')
            if Brands.objects.filter(vchr_name=str_name,int_status=0).exclude(pk_bint_id=int_brand_id):
                return Response({'status':0,'reason':'already exists'})
            else:
                Brands.objects.filter(pk_bint_id=int_brand_id).update(vchr_name=str_name)
            return Response({'status':1,'message':'successfully updated'})
        except Exception as e:
            return Response({'status':0,'reason':e})

    def patch(self,request):
        '''delete brand'''
        try:
            int_brand_id = request.data.get('intId')
            Brands.objects.filter(pk_bint_id=int_brand_id).update(int_status=-1)
            return Response({'status':1,'message':'successfully deleted'})
        except Exception as e:
            return Response({'status':0,'reason':e})

class ViewBrand(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        '''view brand'''
        try:
            int_brand_id = request.data.get('intId')
            lst_brand = list(Brands.objects.filter(pk_bint_id=int_brand_id).values('pk_bint_id','vchr_code','vchr_name'))
            return Response({'status':1,'data':lst_brand})
        except Exception as e:
            return Response({'status':0,'reason':e})



class BrandsTypeHead(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            str_search_term = request.data.get('term',-1)
            lst_brands = []
            if str_search_term != -1:
                ins_brands = Brands.objects.filter(Q(vchr_code__icontains=str_search_term) | Q(vchr_name__icontains=str_search_term),int_status = 0).values('pk_bint_id','vchr_name','vchr_code')
                if ins_brands:
                    for itr_item in ins_brands:
                        dct_brands = {}
                        dct_brands['name'] = itr_item['vchr_name']
                        dct_brands['code'] = itr_item['vchr_code']
                        dct_brands['id'] = itr_item['pk_bint_id']
                        lst_brands.append(dct_brands)
                return Response({'status':1,'data':lst_brands})

        except Exception as e:
            return JsonResponse({'result':0,'reason':e})
