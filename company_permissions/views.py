from django.shortcuts import render
from groups.models import Groups
from userdetails.models import UserDetails as Userdetails
from company_permissions.models import CategoryItems,MainCategory,SubCategory,MenuCategory,GroupPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from POS import ins_logger
from django.db.models import Q
from django.db.models import Value, BooleanField
import json

from random import randint
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime

# Create your views here.
class CompanyPermissions(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_company_id = request.data['int_company_id']
            ins_main = MainCategory.objects.values('pk_bint_id', 'vchr_main_category_name')
            lst_perms = []

            # To check whether admin group is created
            ins_group = Groups.objects.filter(vchr_name__iexact = 'ADMIN', fk_company_id = int_company_id,int_status=0).values()
            if not ins_group:
                bln_add_admin_group = False
            else:
                bln_add_admin_group = True
            # To check whether any user is created in admin group
            ins_user = Userdetails.objects.filter(fk_group__vchr_name__iexact = 'ADMIN', fk_group__fk_company_id = int_company_id, fk_group__int_status=0).values()
            if not ins_user:
                bln_add_admin_user = False
            else:
                bln_add_admin_user = True
            lst_menu_category=[]
            for dct_temp in ins_main:
                ins_sub = SubCategory.objects.filter(Q(fk_main_category = dct_temp['pk_bint_id'])).values('fk_main_category_id','pk_bint_id','vchr_sub_category_name')
                lst_menu_category=[]
                for dct_sub in ins_sub:
                    ins_menu = MenuCategory.objects.annotate(bln_menu_add_perm = Value(False, output_field=BooleanField())).filter(Q(fk_sub_category = dct_sub['pk_bint_id'])).values('fk_sub_category_id','pk_bint_id','vchr_menu_category_name','bln_menu_add_perm')
                    for dct_menu in ins_menu:
                        ins_category_items = CategoryItems.objects.filter(fk_main_category = dct_sub['fk_main_category_id'],fk_sub_category = dct_menu['fk_sub_category_id'],fk_menu_category = dct_menu['pk_bint_id'],fk_company = int_company_id).values()
                        if ins_category_items:
                            dct_menu['bln_menu_add_perm'] = True
                        else:
                            dct_menu['bln_menu_add_perm'] = False
                    if ins_menu:
                        lst_menu_category.append({'name':dct_sub['vchr_sub_category_name'],'sub_id':dct_sub['pk_bint_id'],'menu_items':list(ins_menu),'sub_status':False})
                if ins_sub:
                    lst_perms.append({'name':dct_temp['vchr_main_category_name'],'main_id':dct_temp['pk_bint_id'], 'sub_items':lst_menu_category, 'main_status':False})

            return Response({'status':1,'data':lst_perms,'bln_add_admin_group':bln_add_admin_group,'bln_add_admin_user':bln_add_admin_user})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'data':str(e)})


class CompanyPermissionSave(APIView):
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            int_company_id = int(request.data['int_company_id'])
            lst_perms = json.loads(request.data['lst_per']) #updated data
            lst_perms_copy = json.loads(request.data['lst_perms_copy']) #exact copy of send data
            bln_add_admin_group = request.data['bln_add_admin_group']
            bln_add_admin_user = request.data['bln_add_admin_user']

            ins_group = Groups.objects.filter(vchr_name__iexact = 'ADMIN', fk_company_id = int_company_id, int_status = 0).values()
            for itr_main in range(len(lst_perms)):
                for itr_sub in range(len(lst_perms[itr_main]['sub_items'])):
                    for itr_menu in range(len(lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'])):
                        #if a permissions is removed
                        if lst_perms_copy[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['bln_menu_add_perm'] and not lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['bln_menu_add_perm']:
                            GroupPermissions.objects.filter(fk_category_items__fk_main_category_id = lst_perms[itr_main]['main_id'],fk_category_items__fk_sub_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['sub_id'],fk_category_items__fk_menu_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['pk_bint_id'],fk_category_items__fk_company_id = int_company_id).delete()
                            CategoryItems.objects.filter(fk_main_category_id = lst_perms[itr_main]['main_id'], fk_sub_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['sub_id'],fk_menu_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['pk_bint_id'], fk_company_id = int_company_id).delete()
                        #if a permission is added
                        elif not lst_perms_copy[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['bln_menu_add_perm'] and lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['bln_menu_add_perm']:
                            ins_category_items = CategoryItems.objects.create(fk_main_category_id = lst_perms[itr_main]['main_id'], fk_sub_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['sub_id'],fk_menu_category_id = lst_perms[itr_main]['sub_items'][itr_sub]['menu_items'][itr_menu]['pk_bint_id'], fk_company_id = int_company_id)
                            # Admin Group
                            if ins_group:
                                GroupPermissions.objects.create(
                                    fk_groups_id = ins_group[0]['pk_bint_id'],
                                    fk_category_items_id = ins_category_items.pk_bint_id,
                                    bln_add = True,
                                    bln_edit = True,
                                    bln_view = True,
                                    bln_delete = True,
                                    bln_download = True
                                    )


            # import pdb; pdb.set_trace()
            # Add Admin Group
            if not ins_group and bln_add_admin_group == "true":
                str_group = 'ADMIN'
                lst_category_items = list(CategoryItems.objects.filter(fk_company_id = int_company_id).values())
                ins_group = Groups.objects.create(vchr_name = str_group, fk_company_id = int_company_id, int_status = 1)
                for itr_item in lst_category_items:
                    GroupPermissions.objects.create(
                        fk_groups_id = ins_group.pk_bint_id,
                        fk_category_items_id = itr_item['pk_bint_id'],
                        bln_add = True,
                        bln_edit = True,
                        bln_view = True,
                        bln_delete = True,
                        bln_download = True
                        )

            # Add Admin User
            ins_user = Userdetails.objects.filter(fk_group__vchr_name__iexact = 'ADMIN', fk_group__fk_company_id = int_company_id, fk_group__int_status = 0).values()
            if not ins_user and bln_add_admin_user == "true":
                first_name  = str(request.data.get('firstname'))
                bint_phone = int(request.data.get('contactno'))
                fk_branch= int(request.data.get('branch_id'))
                ins_group = Groups.objects.filter(vchr_name__iexact = 'ADMIN', fk_company_id = int_company_id, int_status = 0).values()
                fk_group = ins_group[0]['pk_bint_id']
                bln_loop=True
                while bln_loop:
                        bint_usercode=randint(10000,99999)
                        if not (Userdetails.objects.filter(bint_usercode=bint_usercode)):
                            bln_loop=False
                vchr_prof = request.FILES.get('image')
                if vchr_prof:
                        my_file = request.FILES.get('image')
                        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                        filename = fs.save(my_file.name, my_file)
                        str_profpic = fs.url(filename)
                username = str(request.data.get('vchr_user_code'))
                last_name=str(request.data.get('lastname'))
                if Userdetails.objects.filter(username=username):
                    return Response({'status':0,'message':'Usercode already exists'})
                else:
                    userobject = Userdetails(bint_phone=bint_phone,bint_usercode=bint_usercode,fk_group_id=fk_group,fk_branch_id=fk_branch,vchr_profpic=str_profpic,username=username,first_name=first_name,last_name=last_name,is_active=True,is_superuser=False,date_joined=datetime.now(),fk_created_id=request.user.id,dat_created=datetime.now())
                userobject.set_password(request.data.get('password'))
                userobject.save()

            return Response({'status':1,'data':'successfully saved'})
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id)})
            lst_category_items = CategoryItems.objects.filter(fk_company_id = int_company_id).values_list('pk_bint_id', flat=True)
            GroupPermissions.objects.filter(fk_category_items_id__in = lst_category_items).delete()
            CategoryItems.objects.filter(fk_company_id = int_company_id).delete()
            Userdetails.objects.filter(fk_company_id = int_company_id).delete()
            Groups.objects.filter(fk_company_id = int_company_id).delete()
            return Response({'status':'0','data':str(e)})
