# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from category.models import Category,OtherCategory,EmpCategory
from rest_framework.permissions import IsAuthenticated,AllowAny
import datetime
from django.db.models import Q
import traceback
######error logg

from POS import ins_logger
import sys, os

# Create your views here.

class CategoryList(APIView): # View for listing all category values
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            lst_articles = list(EmpCategory.objects.filter(int_status=0).values('pk_bint_id','vchr_name','vchr_code').order_by("-dat_created")) #passes as a list object
            return Response({'status':1,'lst_articles':lst_articles})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0})




class CategoryAdd(APIView):# For adding values to the category table
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            str_name = request.data.get('vchr_name') #Get's values from front with field name = vchr_name and vchr_code
            str_code = request.data.get('vchr_code')
            if Category.objects.filter(Q(vchr_name=str_name) | Q(vchr_code=str_code),int_status=0):
                            return Response({'status':0,'reason':'Already exists'})
            else:

                ins_category_reg = Category.objects.create(vchr_name = str_name,vchr_code = str_code,fk_created_id=request.user.id,dat_created=datetime.datetime.now(),int_status=0)
                return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0})

    def put(self,request):
        '''edit category'''
        try:
            str_name=request.data.get('vchr_name')
            str_code = request.data.get('vchr_code')
            pk_bint_id=request.data.get('pk_bint_id')

            if Category.objects.filter(vchr_name=str_name,int_status=0).exclude(pk_bint_id=pk_bint_id):
                        return Response({'status':0,'reason':'already exists'})

            else:
                Category.objects.filter(pk_bint_id=pk_bint_id).update(vchr_name=str_name,vchr_code=str_code,fk_updated_id=request.user.id,dat_updated=datetime.datetime.now())
                return Response({'status':1})


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0,'reason':e})


    def patch(self,request):
        '''delete category'''
        try:
                        pk_bint_id = request.data.get('pk_bint_id')
                        Category.objects.filter(pk_bint_id=pk_bint_id).update(int_status=-1,fk_updated_id=request.user.id,dat_updated=datetime.datetime.now())
                        return Response({'status':1,'message':'successfully updated'})
        except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
                        return Response({'status':0,'reason':e})


class CategoryTypeHead(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            str_search_term = request.data.get('term',-1)
            lst_category = []
            if str_search_term != -1:
                ins_category = Category.objects.filter(Q(vchr_name__icontains=str_search_term) | Q(vchr_code__icontains=str_search_term),int_status = 0).values('pk_bint_id','vchr_name','vchr_code')
                if ins_category:
                    for itr_item in ins_category:
                        dct_category = {}
                        dct_category['name'] = itr_item['vchr_name']
                        dct_category['id'] = itr_item['pk_bint_id']
                        lst_category.append(dct_category)
                return Response({'status':1,'data':lst_category})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return JsonResponse({'result':0,'reason':e})


class OtherCategoryTypeHead(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            str_search_term = request.data.get('term',-1)
            lst_category = []
            if str_search_term != -1:
                ins_category = OtherCategory.objects.filter(Q(vchr_name__icontains=str_search_term)).values('pk_bint_id','vchr_name')
                if ins_category:
                    for itr_item in ins_category:
                        dct_category = {}
                        dct_category['name'] = itr_item['vchr_name']
                        dct_category['id'] = itr_item['pk_bint_id']
                        lst_category.append(dct_category)
                return Response({'status':1,'data':lst_category})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return JsonResponse({'result':0,'reason':e})
