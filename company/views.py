from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import JsonResponse
from rest_framework.response import Response
from company.models import Company
from django.views.generic import View,TemplateView,CreateView
from rest_framework.views import APIView
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
from POS import ins_logger
import sys, os

class CompanyRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:

            vchr_update = int(request.data.get('vchr_update'))
            #update
            if vchr_update:
                company_id = request.data.get('pk_bint_id')
                vchr_name = request.data.get('vchr_name')
                vchr_address = request.data.get('vchr_address')
                vchr_gstin = request.data.get('vchr_gstin')
                vchr_mail = request.data.get('vchr_mail')
                vchr_phone = request.data.get('vchr_phone')
                vchr_logo = request.data.get('vchr_logo')
                vchr_print_logo = request.data.get('vchr_print_logo')

                # ins_company_name = list(Company.objects.values('pk_bint_id','vchr_name','vchr_gstin').filter(vchr_name = vchr_name,vchr_gstin = vchr_gstin).exclude(pk_bint_id = company_id))
                # if ins_company_name:
                #     return Response({'status':'failed' , 'reason' : "company already exists"})
                if vchr_logo and vchr_print_logo:
                    my_file = request.FILES.get('vchr_logo')
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(my_file.name, my_file)
                    vchr_logo_image = fs.url(filename)

                    my_file = request.FILES.get('vchr_print_logo')
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(my_file.name, my_file)
                    vchr_print_logo_image = fs.url(filename)

                    ins_company_update = Company.objects.filter(pk_bint_id = company_id).update(vchr_name = vchr_name,vchr_address = vchr_address ,vchr_gstin = vchr_gstin,vchr_mail = vchr_mail,vchr_phone = vchr_phone,vchr_logo = vchr_logo_image,vchr_print_logo = vchr_print_logo_image)
                    return Response({'status':1})
                elif vchr_logo:
                    my_file = request.FILES.get('vchr_logo')
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(my_file.name, my_file)
                    vchr_logo_image = fs.url(filename)

                    ins_company_update = Company.objects.filter(pk_bint_id = company_id).update(vchr_name = vchr_name,vchr_address = vchr_address ,vchr_gstin = vchr_gstin,vchr_mail = vchr_mail,vchr_phone = vchr_phone,vchr_logo = vchr_logo_image)
                    return Response({'status':1})
                elif vchr_print_logo:
                    my_file = request.FILES.get('vchr_print_logo')
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(my_file.name, my_file)
                    vchr_print_logo_image = fs.url(filename)

                    ins_company_update = Company.objects.filter(pk_bint_id = company_id).update(vchr_name = vchr_name,vchr_address = vchr_address ,vchr_gstin = vchr_gstin,vchr_mail = vchr_mail,vchr_phone = vchr_phone,vchr_print_logo = vchr_print_logo_image)
                    return Response({'status':1})
                else:
                    ins_company_update = Company.objects.filter(pk_bint_id = company_id).update(vchr_name = vchr_name,vchr_address = vchr_address ,vchr_gstin = vchr_gstin,vchr_mail = vchr_mail,vchr_phone = vchr_phone)
                    return Response({'status':1})

            vchr_name = request.data.get('vchr_name')
            vchr_address = request.data.get('vchr_address')
            vchr_gstin = request.data.get('vchr_gstin')
            vchr_mail = request.data.get('vchr_mail')
            vchr_phone = request.data.get('vchr_phone')
            vchr_print_logo = None
            vchr_print_logo_image = None
            vchr_logo = request.FILES.get('vchr_logo')
            vchr_print_logo = request.FILES.get('vchr_print_logo')
            if vchr_logo:
                my_file = request.FILES.get('vchr_logo')
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(my_file.name, my_file)
                vchr_logo_image = fs.url(filename)

            if vchr_print_logo:
                my_file = request.FILES.get('vchr_print_logo')
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(my_file.name, my_file)
                vchr_print_logo_image = fs.url(filename)

            # ins_company_name = list(Company.objects.values('pk_bint_id','vchr_name','vchr_gstin').filter(vchr_name = vchr_name,vchr_gstin = vchr_gstin))
            # if ins_company_name:
            #     return Response({'status':'failed' , 'reason' : "company already exists"})

            ins_company_registration = Company.objects.create(vchr_name = vchr_name,vchr_address = vchr_address ,vchr_gstin = vchr_gstin,vchr_mail = vchr_mail,vchr_phone = vchr_phone,vchr_logo = vchr_logo_image ,vchr_print_logo = vchr_print_logo_image )

            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0})

    def patch(self,request):
        try:

            company_id = request.data.get('pk_bint_id')
            ins_company_update = Company.objects.update(int_status = -1).filter(pk_bint_id = company_id)

            return Response({'status':1})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0})


    def get(self,request):
        try:



            # listing
            ins_company_list = list(Company.objects.values('pk_bint_id','vchr_name','vchr_address','vchr_gstin','vchr_mail','vchr_phone','vchr_logo','vchr_print_logo').filter(int_status = 0))

            return Response({'status':1 , 'data' : ins_company_list})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'status':0})

class CompanyTypeHead(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            ins_company = Company.objects.filter().values()
            return Response({'status':1,'data':ins_company})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})

    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            str_search_term = request.data.get('term',-1)
            lst_company = []
            if str_search_term != -1:
                ins_company = Company.objects.filter(Q(vchr_name__icontains=str_search_term)).values('pk_bint_id','vchr_name')
                if ins_company:
                    for itr_item in ins_company:
                        dct_company = {}
                        dct_company['name'] = itr_item['vchr_name']
                        dct_company['id'] = itr_item['pk_bint_id']
                        lst_company.append(dct_company)
                return Response({'status':1,'data':lst_company})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(exc_tb.tb_lineno)})
            return Response({'result':0,'reason':e})
