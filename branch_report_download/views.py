from django.shortcuts import render
from django.db.models import Q,F
from django.contrib.auth.models import User
from collections import Counter
from collections import OrderedDict
import operator
from rest_framework.views import APIView
from rest_framework.response import Response
from sqlalchemy import case, literal_column
from aldjemy.core import get_engine

from userdetails.models import UserDetails
from customer.models import CustomerDetails
from company.models import Company as CompanyDetails
from enquiry.models import EnquiryMaster
from enquiry_mobile.models import ItemEnquiry
from na_enquiry.models import NaEnquiryMaster,NaEnquiryDetails
from branch.models import Branch
from zone.models import Zone
from territory.models import Territory
from datetime import datetime
from sqlalchemy import desc
from item_category.models import Item
from brands.models import Brands
from globalMethods import show_data_based_on_role,get_user_products
from pdfGenerate import generate_pdf
from generateExcel import generate_excel
import random
import json
from enquiry_print.views import enquiry_print
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import mapper, aliased
from sqlalchemy import and_,func ,cast,Date
from sqlalchemy.sql.expression import literal,union_all
from POS import ins_logger
import aldjemy
from rest_framework.permissions import IsAuthenticated
# from COUNTRY.models import COUNTRY
from titlecase import titlecase
from collections import OrderedDict
from products.models import Products
from sqlalchemy import desc
from POS.dftosql import Savedftosql
from sqlalchemy import create_engine,inspect,MetaData,Table,Column,select,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

# from groups.models import GroupPermissions,Groups,MainCategory, SubCategory
from groups.models import Groups

# from airline.models import AirlineDetails
from globalMethods import show_data_based_on_role,chart_data_sort


sqlalobj = Savedftosql('','')
engine = sqlalobj.engine
metadata = MetaData()
metadata.reflect(bind=engine)
Connection = sessionmaker()
Connection.configure(bind=engine)


EnquiryMasterSA = EnquiryMaster.sa
# CountriesSA = Countries.sa
UserSA=UserDetails.sa
AuthUserSA = User.sa
CustomerSA = CustomerDetails.sa
BranchSA = Branch.sa


#mobile
BrandSA = Brands.sa
ItemSA = Item.sa

CustomerModelSA=CustomerDetails.sa
ItemsSA=Item.sa
BrandsSA=Brands.sa
# ==============================
ItemEnquirySA = ItemEnquiry.sa
ProductsSA = Products.sa
ItemEnquiry = metadata.tables['item_enquiry']
# ================================

def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()

from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny
from django.db.models import Count
from django.http import JsonResponse
import calendar
from export_excel.views import export_excel
# from hasher.views import hash_enquiry
# Create your views here.


class MobileBranchReportDownload(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # import pdb; pdb.set_trace()
            session = Session()
            dct_data={}

            int_company = request.data['company_id']
            ins_company = CompanyDetails.objects.filter(pk_bint_id = int_company)
            # lst_branch = list(Branch.objects.filter(fk_company_id = ins_company[0].pk_bint_id).values())
            lst_branch = list(Branch.objects.all().values())
            # fromdate =  datetime.strptime(request.data['date_from'][:10] , '%Y-%m-%d' )
            fromdate = request.data['date_from']
            # # todate =  datetime.strptime(request.data['date_to'][:10] , '%Y-%m-%d' )
            todate =  request.data['date_to']
            if request.data['bln_chart']:
                str_sort = request.data.get('strGoodPoorClicked','NORMAL')
                int_page = int(request.data.get('intCurrentPage',1))
                if request.data.get('show_type'):
                    str_show_type = 'total_amount'
                else:
                    str_show_type = 'int_quantity'

                engine = get_engine()
                conn = engine.connect()

                lst_mv_view = []

                lst_mv_view = request.data.get('lst_mv')

                if not lst_mv_view:
                    session.close()
                    return JsonResponse({'status': 0, 'reason':'No view list found'})
                query_set = ""
                if len(lst_mv_view) == 1:

                    if request.data['type'].upper() == 'ENQUIRY':

                        query = "select vchr_enquiry_status as status, sum("+str_show_type+") as counts, vchr_product_name as vchr_service, concat(staff_first_name, ' ',staff_last_name) as vchr_staff_full_name, user_id as fk_assigned, staff_first_name, staff_last_name ,vchr_brand_name, vchr_item_name, is_resigned, promoter, branch_id, product_id, brand_id, branch_name from "+lst_mv_view[0]+" {} group by vchr_enquiry_status ,vchr_service, vchr_staff_full_name, fk_assigned, vchr_brand_name, vchr_item_name, promoter, is_resigned,staff_first_name, staff_last_name, branch_id, product_id, brand_id, branch_name"
                    else:

                        query = "select vchr_enquiry_status as status, sum("+str_show_type+") as counts, vchr_product_name as vchr_service, concat(staff_first_name, ' ',staff_last_name) as vchr_staff_full_name,user_id as fk_assigned,staff_first_name, staff_last_name ,vchr_brand_name, vchr_item_name, is_resigned, promoter, branch_id, product_id, brand_id, branch_name from "+lst_mv_view[0]+" {} group by vchr_enquiry_status ,vchr_service, vchr_staff_full_name, fk_assigned, vchr_brand_name, vchr_item_name, promoter, is_resigned,staff_first_name, staff_last_name, branch_id, product_id, brand_id, branch_name"

                else:

                    if request.data['type'].upper() == 'ENQUIRY':

                        for data in lst_mv_view:
                            query_set += "select vchr_enquiry_status as status,vchr_product_name as vchr_service,concat(staff_first_name,' ',staff_last_name) as vchr_staff_full_name,sum("+str_show_type+") as counts,user_id as fk_assigned,vchr_brand_name,vchr_item_name,promoter,is_resigned, branch_id, product_id, brand_id, branch_name from "+data+" {} group by  vchr_enquiry_status , vchr_service, vchr_staff_full_name, fk_assigned, vchr_brand_name, vchr_item_name, promoter, is_resigned, branch_id, product_id, brand_id, branch_name union "
                    else:

                         for data in lst_mv_view:

                            query_set +="select vchr_enquiry_status as status,vchr_product_name as vchr_service,concat(staff_first_name,' ',staff_last_name) as vchr_staff_full_name,sum("+str_show_type+") as counts,user_id as fk_assigned, vchr_brand_name, vchr_item_name,promoter,is_resigned,branch_id, product_id, brand_id, branch_name from "+data+" {} group by vchr_enquiry_status, vchr_service, vchr_staff_full_name, fk_assigned, vchr_brand_name, vchr_item_name, promoter,is_resigned,branch_id, product_id, brand_id, branch_name union "

                    query = query_set.rsplit(' ', 2)[0]


                """ data wise filtering """

                str_filter_data = "where dat_enquiry :: date BETWEEN '"+request.data['date_from']+"' AND '"+request.data['date_to']+"' AND int_company_id = "+int_company+""

                """Permission wise filter for data"""
                if request.user.userdetails.fk_group.vchr_name.upper() in ['ADMIN','GENERAL MANAGER SALES','COUNTRY HEAD']:
                    pass
                elif request.user.userdetails.fk_group.vchr_name.upper() in ['BRANCH MANAGER','ASSISTANT BRANCH MANAGER']:
                    str_filter_data = str_filter_data+" AND branch_id = "+str(request.user.userdetails.fk_branch_id)+""

                elif request.user.userdetails.fk_hierarchy_group_id or request.user.userdetails.fk_group.vchr_name.upper() in ['CLUSTER MANAGER']:
                    lst_branch=show_data_based_on_role(request)
                    str_filter_data += " AND branch_id IN ("+str(lst_branch)[1:-1]+")"
                else:
                    session.close()
                    return Response({'status': 0,'reason':'No data'})

                if request.data.get('branch'):
                    str_filter_data += " AND branch_id IN ("+str(request.data.get('branch'))[1:-1]+")"

                if request.data.get('product'):
                    str_filter_data += " AND product_id = "+str(request.data.get('product'))+""

                if request.data.get('brand'):
                    str_filter_data += " AND brand_id = "+str(request.data.get('brand'))+""

                # import pdb; pdb.set_trace()
                #for getting user corresponding products
                lst_user_id =[]
                lst_user_id.append(request.user.id)

                lst_user_products = get_user_products(lst_user_id)
                if lst_user_products:
                    str_filter_data += " AND product_id in ("+str(lst_user_products)[1:-1]+")"





                if len(lst_mv_view) == 1:
                    query = query.format(str_filter_data)
                else:
                    query = query.format(str_filter_data,str_filter_data)
                rst_enquiry = conn.execute(query).fetchall()

                if not rst_enquiry:
                    session.close()
                    return Response({'status':'failled','data':'No Data'})
                dct_data={}
                dct_data['branch_all']={}
                dct_data['service_all']={}
                dct_data['brand_all']={}
                dct_data['item_all']={}
                dct_data['status_all']={}

                for ins_data in rst_enquiry:
                    if ins_data.branch_name.title() not in dct_data['branch_all']:
                        dct_data['branch_all'][ins_data.branch_name.title()]={}
                        dct_data['branch_all'][ins_data.branch_name.title()]['Enquiry']=int(ins_data.counts)
                        dct_data['branch_all'][ins_data.branch_name.title()]['Sale']=0

                        if ins_data.status == 'INVOICED':
                            dct_data['branch_all'][ins_data.branch_name.title()]['Sale'] = int(ins_data.counts)
                    else:
                        dct_data['branch_all'][ins_data.branch_name.title()]['Enquiry']+=int(ins_data.counts)
                        if ins_data.status == 'INVOICED':
                            dct_data['branch_all'][ins_data.branch_name.title()]['Sale']+=int(ins_data.counts)

                    if ins_data.vchr_service.title() not in dct_data['service_all']:
                        dct_data['service_all'][ins_data.vchr_service.title()]={}
                        dct_data['service_all'][ins_data.vchr_service.title()]['Enquiry']=int(ins_data.counts)
                        dct_data['service_all'][ins_data.vchr_service.title()]['Sale']=0
                        if ins_data.status == 'INVOICED':
                            dct_data['service_all'][ins_data.vchr_service.title()]['Sale']=int(ins_data.counts)
                    else:
                        dct_data['service_all'][ins_data.vchr_service.title()]['Enquiry']+=int(ins_data.counts)
                        if ins_data.status == 'INVOICED':
                            dct_data['service_all'][ins_data.vchr_service.title()]['Sale']+=int(ins_data.counts)

                    if ins_data.vchr_brand_name.title() not in dct_data['brand_all']:
                        dct_data['brand_all'][ins_data.vchr_brand_name.title()]={}
                        dct_data['brand_all'][ins_data.vchr_brand_name.title()]['Enquiry']=int(ins_data.counts)
                        dct_data['brand_all'][ins_data.vchr_brand_name.title()]['Sale']=0
                        if ins_data.status == 'INVOICED':
                            dct_data['brand_all'][ins_data.vchr_brand_name.title()]['Sale']=int(ins_data.counts)
                    else:
                        dct_data['brand_all'][ins_data.vchr_brand_name.title()]['Enquiry']+=int(ins_data.counts)
                        if ins_data.status == 'INVOICED':
                            dct_data['brand_all'][ins_data.vchr_brand_name.title()]['Sale']+=int(ins_data.counts)

                    if ins_data.vchr_item_name.title() not in dct_data['item_all']:
                        dct_data['item_all'][ins_data.vchr_item_name.title()]={}
                        dct_data['item_all'][ins_data.vchr_item_name.title()]['Enquiry']=int(ins_data.counts)
                        dct_data['item_all'][ins_data.vchr_item_name.title()]['Sale']=0
                        if ins_data.status == 'INVOICED':
                            dct_data['item_all'][ins_data.vchr_item_name.title()]['Sale']=int(ins_data.counts)
                    else:
                        dct_data['item_all'][ins_data.vchr_item_name.title()]['Enquiry']+=int(ins_data.counts)
                        if ins_data.status == 'INVOICED':
                            dct_data['item_all'][ins_data.vchr_item_name.title()]['Sale']+=int(ins_data.counts)

                    if ins_data.status not in dct_data['status_all']:
                        dct_data['status_all'][ins_data.status]=int(ins_data.counts)
                    else:
                        dct_data['status_all'][ins_data.status]+=int(ins_data.counts)

                dct_data['brand_all']=paginate_data(dct_data['brand_all'],10)
                dct_data['brand_all'] = chart_data_sort(request,dct_data['brand_all'],'NORMAL',1)
                # sorted_dct_data = sorted(dct_data['brand_all'][1].items(), key= best_key)
                # dct_data['brand_all'] = dict(sorted_dct_data)

                dct_data['branch_all']=paginate_data(dct_data['branch_all'],10)
                dct_data['branch_all'] = chart_data_sort(request,dct_data['branch_all'],str_sort,int_page)
                # sorted_dct_data = sorted(dct_data['branch_all'][1].items(), key= best_key)
                # dct_data['branch_all'] = dict(sorted_dct_data)

                dct_data['item_all']=paginate_data(dct_data['item_all'],10)
                dct_data['item_all'] = chart_data_sort(request,dct_data['item_all'],'NORMAL',1)
                # sorted_dct_data = sorted(dct_data['item_all'][1].items(), key= best_key)
                # dct_data['item_all'] = dict(sorted_dct_data)

                dct_data['service_all']=paginate_data(dct_data['service_all'],10)
                dct_data['service_all'] = chart_data_sort(request,dct_data['service_all'],'NORMAL',1)
                # sorted_dct_data = sorted(dct_data['service_all'][1].items(), key= best_key)
                # dct_data['service_all'] = dict(sorted_dct_data)


                if request.data['type'].upper() == 'ENQUIRY':
                    str_report_name = 'Branch Enquiry Report'
                    lst_details = ['branch_all-bar','service_all-bar','brand_all-bar','item_all-bar','status_all-pie']
                    dct_label = {'branch_all':'Branch wise','service_all':'Product wise','brand_all':'Brand wise','item_all':'Item wise','status_all':'Status wise'}
                else:
                    str_report_name = 'Branch Sales Report'
                    lst_details = ['branch_all-bar','service_all-bar','brand_all-bar','item_all-bar']
                    dct_label = {'branch_all':'Branch wise','service_all':'Product wise','brand_all':'Brand wise','item_all':'Item wise'}

            if request.data['bln_table']:
                if request.data['type'].upper() == 'ENQUIRY':
                    str_report_name = 'Branch Enquiry Report'
                else:
                    str_report_name = 'Branch Sales Report'
                rst_enquiry = session.query(ItemEnquirySA.vchr_enquiry_status.label('status'),ProductsSA.vchr_name.label('vchr_service'),func.concat(AuthUserSA.first_name, ' ',
                                    AuthUserSA.last_name).label('vchr_staff_full_name'),
                                    EnquiryMasterSA.fk_assigned_id.label('fk_assigned'),func.DATE(EnquiryMasterSA.dat_created_at).label('dat_created_at'),EnquiryMasterSA.vchr_enquiry_num,func.concat(CustomerModelSA.vchr_name).label('vchr_full_name'),
                                    AuthUserSA.id.label('user_id'),AuthUserSA.last_name.label('staff_last_name'),
                                    AuthUserSA.first_name.label('staff_first_name'),BranchSA.vchr_name.label('vchr_name'),BrandsSA.vchr_name,ItemsSA.vchr_name,
                                    UserSA.fk_brand_id,UserSA.dat_resignation_applied,
                                    case([(UserSA.dat_resignation_applied < datetime.now(),literal_column("'resigned'"))],
                                        else_=literal_column("'not resigned'")).label("is_resigned"))\
                                    .filter(cast(EnquiryMasterSA.dat_created_at,Date) >= fromdate,
                                            cast(EnquiryMasterSA.dat_created_at,Date) <= todate,
                                            EnquiryMasterSA.fk_company_id == request.user.userdetails.fk_company_id,
                                            EnquiryMasterSA.chr_doc_status == 'N')\
                                    .join(EnquiryMasterSA,ItemEnquirySA.fk_enquiry_master_id == EnquiryMasterSA.pk_bint_id)\
                                    .join(BranchSA,BranchSA.pk_bint_id == EnquiryMasterSA.fk_branch_id)\
                                    .join(CustomerSA,EnquiryMasterSA.fk_customer_id == CustomerSA.pk_bint_id)\
                                    .join(AuthUserSA, EnquiryMasterSA.fk_assigned_id == AuthUserSA.id)\
                                    .join(UserSA, AuthUserSA.id == UserSA.user_ptr_id )\
                                    .join(ProductsSA,ProductsSA.pk_bint_id == ItemEnquirySA.fk_product_id)\
                                    .join(BrandsSA,BrandsSA.pk_bint_id==ItemEnquirySA.fk_brand_id)\
                                    .join(ItemsSA,ItemsSA.pk_bint_id==ItemEnquirySA.fk_item_id)

                """Permission wise filter for data"""
                if request.user.userdetails.fk_group.vchr_name.upper() in ['ADMIN','GENERAL MANAGER SALES','COUNTRY HEAD']:
                    pass
                elif request.user.userdetails.fk_group.vchr_name.upper() in ['BRANCH MANAGER','ASSISTANT BRANCH MANAGER']:
                    rst_enquiry = rst_enquiry.filter(EnquiryMasterSA.fk_branch_id == request.user.userdetails.fk_branch_id)
                elif request.user.userdetails.fk_hierarchy_group_id or request.user.userdetails.fk_group.vchr_name.upper() in ['CLUSTER MANAGER']:
                    lst_branch=show_data_based_on_role(request)
                    rst_enquiry = rst_enquiry.filter(EnquiryMasterSA.fk_branch_id.in_(lst_branch))
                else:
                    session.close()
                    return Response({'status':0,'reason':'No data'})

                if request.data.get('branch'):
                    rst_enquiry = rst_enquiry.filter(EnquiryMasterSA.fk_branch_id.in_(tuple(request.data.get('branch'))))


                # import pdb; pdb.set_trace()
                #for getting user corresponding products
                lst_user_id =[]
                lst_user_id.append(request.user.id)
                lst_user_products = get_user_products(lst_user_id)

                if lst_user_products:
                    rst_enquiry = rst_enquiry.filter(ProductsSA.id.in_(lst_user_products))

                if not rst_enquiry.all():
                    session.close()
                    return Response({'status':'failled','data':'No Data'})

                lst_tbl_head = ['Enquiry No','Branch','Product','Brand','Item','Status']
                lst_tbl_index = [5,10,1,11,12,0]

            if request.data['document'].upper() == 'PDF':

                if request.data['bln_table'] and request.data['bln_chart']:
                    file_output = generate_pdf(request,str_report_name,lst_details,dct_label,dct_data,lst_tbl_head,lst_tbl_index,list(rst_enquiry.all()))
                elif request.data['bln_chart']:
                    file_output = generate_pdf(request,str_report_name,lst_details,dct_label,dct_data)
                elif request.data['bln_table']:
                    file_output = generate_pdf(request,str_report_name,lst_tbl_head,lst_tbl_index,list(rst_enquiry.all()))


                if request.data.get('export_type').upper() == 'DOWNLOAD':
                    session.close()
                    return Response({"status": 1,'file':file_output['file'],'file_name':file_output['file_name']})
                elif request.data.get('export_type').upper() == 'MAIL':
                    session.close()
                    return Response({"status": 1})

            elif request.data['document'].upper() == 'EXCEL':
                if request.data['bln_table'] and request.data['bln_chart']:
                    data=generate_excel(request,str_report_name,lst_details,dct_label,dct_data,lst_tbl_head,lst_tbl_index,list(rst_enquiry.all()))
                elif request.data['bln_chart']:
                    data=generate_excel(request,str_report_name,lst_details,dct_label,dct_data)
                elif request.data['bln_table']:
                    data=generate_excel(request,str_report_name,lst_tbl_head,lst_tbl_index,list(rst_enquiry.all()))

                if request.data.get('export_type').upper() == 'DOWNLOAD':
                    session.close()
                    return Response({"status": 1,"file":data})
                elif request.data.get('export_type').upper() == 'MAIL':
                    session.close()
                    return Response({"status": 1})

        except Exception as e:
            session.close()
            return Response({'status': 0,'data':str(e)})



def best_key(tup):
    key,data = tup
    return -data['Enquiry']

def key_sort(tup):
    k,d = tup
    return d['Enquiry'],d['Sale']
def paginate_data(dct_data,int_page_legth):
    print("gukhbkj",dct_data)
    dct_paged = {}
    int_count = 1
    sorted_dct_data = reversed(sorted(dct_data.items(), key=key_sort))
    dct_data = OrderedDict(sorted_dct_data)
    for key in dct_data:
        if int_count not in dct_paged:
            dct_paged[int_count]={}
            dct_paged[int_count][key]=dct_data[key]
        elif len(dct_paged[int_count]) < int_page_legth:
            dct_paged[int_count][key]= dct_data[key]
        else:
            int_count += 1
            dct_paged[int_count] ={}
            dct_paged[int_count][key] = dct_data[key]
    return dct_paged
