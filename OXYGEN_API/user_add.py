import pandas as pd
import psycopg2
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import random
from django.db import transaction
from django.contrib.auth.hashers import make_password
from userdetails.models import UserDetails,SalaryStructure,EmpLeaveData
from category.models import Category
from branch.models import Branch
from department.models import Department
from job_position.models import JobPosition
import calendar
from userdetails.models import DocumentHrms
from brands.models import Brands
from groups.models import Groups

def user_insert():
    dct_oxy2trv = {
        'SALES CONSULTANT' : 'STAFF',
        'BRANCH MANAGER':'BRANCH MANAGER',
        'ACCOUNTANT':'ASSISTANT BRANCH MANAGER',
    }
    dct_groupsdata = {x['vchr_name'].upper(): x['pk_bint_id'] for x in Groups.objects.filter().values()}
    # ins_hrmsdocumet = DocumentHrms.objects.get(vchr_short_code='OXY')
    try:
        # import pdb;pdb.set_trace()
        with transaction.atomic():
            int_depart_id = Department.objects.filter(vchr_name = 'SALES').values('pk_bint_id').first()['pk_bint_id']
            # import pdb;pdb.set_trace()
            excel_file = pd.ExcelFile('/home/fahad/Documents/OXYGEN_PROJECT/project/erp/OXYGEN_API/EMPLOYEE DATA.xlsx')
            lst_sheet = []
            lst_sheet.append({'sheet':'ADOOR','header':0})
            
            dct_brands = {x['vchr_name']:x['pk_bint_id'] for x in Brands.objects.filter().values()}
            dct_cat = {}
            # for ins_data in Category.objects.filter(int_status=0).values('pk_bint_id','vchr_name'):
            #     dct_cat[ins_data['vchr_name']] = ins_data['pk_bint_id']
            dct_slab = {}
            flag_branch = True
            for ins_data in SalaryStructure.objects.filter(bln_active=True).values('pk_bint_id','vchr_name'):
                dct_slab[ins_data['vchr_name']] = ins_data['pk_bint_id']
            # import pdb;pdb.set_trace()
            for dct_sheet in excel_file.sheet_names:
                flag_branch = True
                print(dct_sheet)
                df = pd.read_excel(excel_file,sheet_name=dct_sheet)
                for ind,row in df.iterrows():
                    if flag_branch:
                        int_branch_id = Branch.objects.filter(vchr_name__icontains = row['BRANCH']).values('pk_bint_id').first()['pk_bint_id']
                        flag_branch = False
                    # import pdb; pdb.set_trace()
                    # emp_id = 
                    if not UserDetails.objects.filter(vchr_employee_code = row['EMPLOYEE CODE']):
                        ins_user = UserDetails()
                        ins_user.username = row['EMPLOYEE CODE']
                        ins_user.password = make_password('OXYGEN@123')
                        ins_user.first_name = row['EMPLOYEE NAME'].split()[0]
                        ins_user.last_name = ' '.join(row['EMPLOYEE NAME'].split()[1:])
                        ins_user.is_superuser = False
                        ins_user.email = row['EMPLOYEE MAIL ID']
                        ins_user.bint_phone = row['EMPLOYEE CONTACT NUMBER']
                        ins_user.is_staff = False
                        ins_user.is_active = True
                        ins_user.fk_created_id = 42
                        ins_user.vchr_employee_code = row['EMPLOYEE CODE']
                        ins_user.fk_branch_id = int_branch_id
                        if row['BRAND'] != 'nan' and type(row['BRAND']) != float:
                            ins_user.fk_brand_id = dct_brands.get(row['BRAND'],None)
                        ins_user.fk_category_id = 1
                        ins_user.fk_department_id = int_depart_id
                        ins_user.fk_group_id = dct_groupsdata.get(dct_oxy2trv.get(row['EMPLOYEE DESIGNATION'].strip()),None)

                        ins_user.save()
                        # if not row['LOP']:
                        #     row['LOP']=0
                        # ins_leave = EmpLeaveData(fk_employee_id = ins_user.user_ptr_id,dbl_number = row['LOP'])
                        # ins_leave.save()
            print('success')
    except Exception as e:
        print(dct_sheet)
        print(row)
        # import pdb;pdb.set_trace()
        print("error :"+str(e))
    # cur.close()
    # conn.close()

# def create_groups():
#     ins_group_save = Groups.objects.create(vchr_code=vchr_code,vchr_name=vchr_name,int_status = 0,dat_created=datetime.now(),fk_created_id= request.user.id,fk_company_id = int_company)
#     return 1
# def user_update():
#     try:
#         with transaction.atomic():
#             df = pd.read_excel('/home/examuser/a.xlsx',header=0)
#             for ind, row in df.iterrows():
#                 dat_dob = datetime.now()-relativedelta(years=row['Age'])
#                 if row['M/F'] == 'M':
#                     vchr_gender = 'Male'
#                 elif row['M/F'] == 'F':
#                     vchr_gender = 'Female'
#                 UserDetails.objects.filter(username = row['ID']).update(vchr_gender=vchr_gender,dat_dob=dat_dob)
#
#     except Exception as e:
#         print("error :"+str(e))
