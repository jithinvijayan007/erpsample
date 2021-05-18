import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
from userdetails.models import UserDetails as Userdetails as UserAppUsermodel
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
        import pdb; pdb.set_trace()
        conn = psycopg2.connect(host="localhost",database="hrms_pos", user="admin", password="tms@123")
        cur = conn.cursor()
        conn.autocommit = True
        df = pd.read_excel("clone_user_hrms_pos/employee.xlsx",header=0,sheet_name="employee").fillna('None')
    except Exception as e:
        return 'cannot read excel'


    """
    key = code form excel
    value = in database matching value
    """
    # cur.execute("SELECT pk_bint_id FROM company_details where vchr_code = 'MYG';")
    # ins_specification = cur.fetchall()
    # if ins_specification:
    #     int_company_id = ins_specification[0]
    # else:
    #     print("Company Not Found!!!")
    #     exit()

    dct_designation = {
    	'SERVICE ENGINEER':'Service engineer',
    	'COMPLETE SOLUTION ADVISOR':'Staff',
    	'COMPLETE SOLUTION ADVISOR- ACCESSORY':'Staff',
    	'CSA - GDOT':'Staff',
    	'CUSTOMER EXPERIENCE ASSISTANT':'Customer Experience Exicutive',
    	'NPS EXECUTIVE':'Staff',
    	'ASST ACCOUNTS MANAGER':'ASST ACCOUNTS MANAGER',
    	'FINANCE MANAGER':'FINANCE MANAGER',
    	'ZONAL MANAGER':'ZONE MANAGER',
    	'TERRITORY MANAGER':'TERRITORY MANAGER',
    	'STRATEGIC BUSINESS ANALYST':'STRATEGIC BUSINESS ANALYST',
    	'SERVICER':'SERVICER',
        'STORE MANAGER':'Branch manager',
    	'ASST STORE MANAGER':'Assistant branch manager',
    	'ASST STORE MANAGER 2':'ASM2',
    	'FLOOR MANAGER':'Floor Manager1',
    }


    dct_designation_ids = {
        'Service engineer':'25472',
        'Staff':'25448',
        'Customer Experience Executive':'26375',
        'ASST ACCOUNTS MANAGER':'26387',
        'FINANCE MANAGER':'26388',
        'ZONE MANAGER':'26392',
        'TERRITORY MANAGER':'26391',
        'STRATEGIC BUSINESS ANALYST':'26390',
        'servicer':'26389',
        'Branch manager':'13047',
    	'Assistant branch manager':'25452',
    	'ASM2':'26380',
    	'Floor Manager1':'26378'
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
        'PURCHASE':'7',
        'MARKETING':'4'
    }
    cur.execute("SELECT pk_bint_id,vchr_name FROM brands;")
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

        import pdb; pdb.set_trace()
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
                                                            # fk_company_id = int_company_id[0],
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



"""Database Changes"""
"""

CREATE TABLE department(
  pk_bint_id BIGSERIAL PRIMARY KEY,
  vchr_code varchar(10) NOT NULL,
  vchr_name varchar(50) NOT NULL,
  fk_company_id BIGINT REFERENCES company(pk_bint_id) NOT NULL
);

insert into department(vchr_code,vchr_name,fk_company_id) values ('HOD','Head Of Department',1),('DEP001','sales',1),('dep002','service',1),('mtg','marketing',1),('adt','auditing',1),('dpt003','finance',1),('dep007','purchase',1);
insert into groups(vchr_name,int_status,fk_created_id,fk_company_id) values ('ASST ACCOUNTS MANAGER',0,6673,1),('FINANCE MANAGER',0,6673,1),('SERVICER',0,6673,1),('STRATEGIC BUSINESS ANALYST',0,6673,1),('TERRITORY MANAGER',0,6673,1),('ZONE MANAGER',0,6673,1);
alter table userdetails add column fk_department_id bigint REFERENCES department(pk_bint_id);
INSERT INTO department (vchr_code,vchr_name,fk_company_id) values ('HOD','Head Of Department',1),('DEP001','sales',1),('dep002','service',1),('mtg','marketing',1),('adt','auditing',1),('dpt003','finance',1),('dept005','call center',1),('dep006','accounts',1),('dep007','purchase',1),('gdp01','gdp',1);

"""
