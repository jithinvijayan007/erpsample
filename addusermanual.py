from userdetails.models import UserDetails,SalaryStructure,EmpLeaveData
from category.models import Category
from branch.models import Branch
from department.models import Department
from job_position.models import JobPosition
import calendar
from userdetails.models import DocumentHrms
from brands.models import Brands
from groups.models import Groups
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import random
from django.contrib.auth.hashers import make_password
row = {}
row['EMPLOYEE CODE'] = input('enter username')

def adduser():
    if not UserDetails.objects.filter(vchr_employee_code = row['EMPLOYEE CODE']):

        row['EMPLOYEE NAME'] = input('full name')
        row['EMPLOYEE MAIL ID'] = input('enter email')
        row['EMPLOYEE CONTACT NUMBER'] = input('enter number')
        row['BRAND'] = 'nan'


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
        ins_user.fk_branch_id = 99
        if row['BRAND'] != 'nan' and type(row['BRAND']) != float:
            ins_user.fk_brand_id = dct_brands.get(row['BRAND'],None)
        ins_user.fk_category_id = 1
        ins_user.fk_department_id = 3
        ins_user.fk_group_id = 17

        ins_user.save()
    else:
        print('user already exist')

adduser()