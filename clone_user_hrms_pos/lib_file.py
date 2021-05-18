import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
from user_app.models import UserModel as UserAppUsermodel
from django.contrib.auth.models import User
from pandas import ExcelWriter
import pandas as pd
import psycopg2
import datetime
from django.conf import settings
# from branch.models import Branch,Department
# from inventory.models import Brands
# from company.models import CompanyDetails
# from groups.models import Groups


def change_data():
    # try:
    try:
        conn = psycopg2.connect(host="localhost",database="libin_bi3", user="admin", password="tms@123")
        cur = conn.cursor()
        conn.autocommit = True
        df = pd.read_excel("lib_file/employee.xlsx",header=0,sheet_name="employee").fillna('None')
    except Exception as e:
        return 'cannot read excel'


    """
    key = code form excel
    value = in database matching value
    """
    cur.execute("SELECT pk_bint_id FROM company_details where vchr_code = 'MYG';")
    ins_specification = cur.fetchall()
    if ins_specification:
        int_company_id = ins_specification[0]
    else:
        print("Company Not Found!!!")
        exit()

    dct_designation = {
    	'SERVICE ENGINEER':'SERVICE ENGINEER',
    	'COMPLETE SOLUTION ADVISOR':'STAFF',
    	'COMPLETE SOLUTION ADVISOR- ACCESSORY':'STAFF',
    	'CSA - GDOT':'STAFF',
    	'CUSTOMER EXPERIENCE ASSISTANT':'Customer Experience Executive',
    	'NPS EXECUTIVE':'STAFF',
    	'ASST ACCOUNTS MANAGER':'ASST ACCOUNTS MANAGER',
    	'FINANCE MANAGER':'FINANCE MANAGER',
    	'ZONAL MANAGER':'ZONE MANAGER',
    	'TERRITORY MANAGER':'TERRITORY MANAGER',
    	'STRATEGIC BUSINESS ANALYST':'STRATEGIC BUSINESS ANALYST',
    	'SERVICER':'servicer',
        'STORE MANAGER':'BRANCH MANAGER',
    	'ASST STORE MANAGER':'ASSISTANT BRANCH MANAGER',
    	'ASST STORE MANAGER 2':'ASM2',
    	'FLOOR MANAGER':'Floor Manager1',
    }
    dct_designation_ids = {
        'SERVICE ENGINEER':'17',
        'STAFF':'6',
        'Customer Experience Executive':'47',
        'ASST ACCOUNTS MANAGER':'30',
        'FINANCE MANAGER':'32',
        'ZONE MANAGER':'5',
        'TERRITORY MANAGER':'3',
        'STRATEGIC BUSINESS ANALYST':'49',
        'servicer':'15',
        'BRANCH MANAGER':'2',
    	'ASSISTANT BRANCH MANAGER':'18',
    	'ASM2':'42',
    	'Floor Manager1':'44'
    }

    # dct_branch = {
    #     'CKI':'cky',
    #     'HO':'3GH',
    #     'LAN':'LAN',
    # }
    # dct_branch = {
    #     'CKI':'154',
    #     'HO':'146',
    #     'LAN':'152',
    # }

    cur.execute("SELECT pk_bint_id,vchr_code FROM branch;")
    ins_specification = cur.fetchall()
    dct_branch = {}
    for data in ins_specification:
        dct_branch[data[1].upper()]=data[0]

    # dct_departmet = {
    #     'SALES':'sales',
    # 	'PURCHASE':'purchase',
    # 	'MARKETING':'marketing',
    # }
    lst_departmet = ['SALES','PURCHASE','MARKETING']
    dct_departmet_ids = {
        'SALES':'2',
        'PURCHASE':'9',
        'MARKETING':'4'
    }
    cur.execute("SELECT id,vchr_brand_name FROM brands;")
    ins_specification = cur.fetchall()
    dct_brands = {}
    for data in ins_specification:
        dct_brands[data[1]]=data[0]

    # import pdb; pdb.set_trace()
    dct_error_data = {}
    dct_data_success = {}
    dct_data_pending = {}
    for ind,row in df.iterrows():

        str_emp_code = row['EMP CODE']
        str_first_name = row['FIRST NAME']
        str_last_name = row['LAST NAME']
        str_username = str(str_first_name) +" "+ str(str_last_name)
        str_email = row['EMAIL'] if row['EMAIL'] != 'None' else ''
        str_phone = row['PHONE'] if row['PHONE'] != 'None' else 0
        str_designation = ''
        str_branch_code = ''
        str_brand = ''
        str_department = ''
        str_error = ""
        # print(str_emp_code,str_first_name,str_dct_designation.get(row['DESIGNATION'])last_name,str_department,str_email,str_phone,str_designation,str_branch_code,str_brand)

        if(dct_designation.get(row['DESIGNATION']) != None):
            str_designation = dct_designation.get(row['DESIGNATION'])
            # print(dct_designation.get(row['DESIGNATION'])," : ",row['DESIGNATION'])
        else:
            str_error = str_error + "DESIGNATION,"



        if dct_branch.get(row['BRANCH CODE']) != None :
            str_branch_code = row['BRANCH CODE']
        else:
            str_error = str_error + "BRANCH CODE,"

        # if dct_departmet.get(row['DEPARTMENT']) != None :
        if row['DEPARTMENT'] in lst_departmet:
            str_department = row['DEPARTMENT']
        else:
            str_error = str_error + "DEPARTMENT,"
            if dct_data_pending.get(row['DEPARTMENT']):
                dct_data_pending[row['DEPARTMENT']].add(row['DESIGNATION'])
            else:
                dct_data_pending[row['DEPARTMENT']] = {row['DESIGNATION']}

        if dct_brands.get(row['BRAND']) != None :
            str_brand = dct_brands.get(row['BRAND'])
        else:
            str_error = str_error + "BRAND,"

        # import pdb; pdb.set_trace()
        print(str_emp_code)
        if str_designation != '' and str_branch_code != '' and str_department != '' and str_brand != '' :
            rst_userexists = User.objects.filter(username = str_emp_code)
            if rst_userexists:
                # pass
                dct_error_data[str_username] = "User Exists"
            else:
                rst_data = UserAppUsermodel.objects.create(first_name = str_first_name,
                                                            last_name = str_last_name,
                                                            email = str_email,
                                                            username=str_emp_code,
                                                            bint_phone = str_phone,
                                                            # vchr_user_code = str_emp_code,
                                                            fk_group_id = dct_designation_ids.get(str_designation),
                                                            fk_branch_id = dct_branch.get(str_branch_code),
                                                            fk_brand_id = str_brand,
                                                            fk_department_id = dct_departmet_ids.get(str_department),
                                                            fk_company_id = int_company_id[0],
                                                            )
                rst_data.set_password(str_emp_code+'@123')
                rst_data.save()
                dct_data_success[str_username] = str_emp_code
        else:
            dct_error_data[str_username] = str_error

    # print("Data Not Entered : ", dct_error_data)
    # print("Data Entered : ", dct_data_success)
    print("Data : ",dct_data_pending)

    """Creating Excel for Successfull Entries"""
    writer = pd.ExcelWriter(str(settings.MEDIA_ROOT).split('media')[0] + '/lib_file/Files/Successfull_Data_'+str(datetime.datetime.today())+'.xlsx', engine ='xlsxwriter')
    workbook = writer.book
    head_style = workbook.add_format({'font_size':11, 'bold':1, 'align': 'center','border':1,'border_color':'#000000'})
    head_style.set_pattern(1)
    head_style.set_bg_color('#bfbfbf')
    head_style.set_align('vcenter')

    row_style = workbook.add_format({'font_size':11, 'text_wrap': True})
    row_style.set_align('vcenter')
    worksheet = workbook.add_worksheet()

    int_row = 0
    worksheet.write(int_row, 0, 'User Name',head_style)
    worksheet.write(int_row, 1, 'Error Status',head_style)

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(0, 1, 40)

    for dct_key,dct_value in dct_data_success.items():
        int_row += 1
        worksheet.write(int_row, 0, dct_key,row_style)
        worksheet.write(int_row, 1, dct_value,row_style)
    writer.save()

    """Creating Excel for Unsuccessfull Entries"""
    writer = pd.ExcelWriter(str(settings.MEDIA_ROOT).split('media')[0] + '/lib_file/Files/Unsuccessfull_Data_'+str(datetime.datetime.today())+'.xlsx', engine ='xlsxwriter')
    workbook = writer.book
    head_style = workbook.add_format({'font_size':11, 'bold':1, 'align': 'center','border':1,'border_color':'#000000'})
    head_style.set_pattern(1)
    head_style.set_bg_color('#bfbfbf')
    head_style.set_align('vcenter')

    row_style = workbook.add_format({'font_size':11, 'text_wrap': True})
    row_style.set_align('vcenter')
    worksheet = workbook.add_worksheet()

    int_row = 0
    worksheet.write(int_row, 0, 'User Name',head_style)
    worksheet.write(int_row, 1, 'Error Status',head_style)

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(0, 1, 40)

    for dct_key,dct_value in dct_error_data.items():
        int_row += 1
        worksheet.write(int_row, 0, dct_key)
        worksheet.write(int_row, 1, dct_value)
    writer.save()
    # import pdb; pdb.set_trace()
    print("\n\n~~~~~~END~~~~~~")

    # except Exception as e:
    #     print("Something Went Wrong....!\n",e)
