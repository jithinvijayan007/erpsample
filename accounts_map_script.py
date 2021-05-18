from accounts_map.models import AccountsMap
from branch.models import Branch
from sap_api.models import ChartOfAccounts
from datetime import datetime
import xlrd
from django.conf import settings
import pandas as pd
from POS.dftosql import Savedftosql
from django.db.models.functions import Upper
cell_value = ''
#function which replace the value with
def fillnan(value):
    global cell_value
    if value:
        cell_value = value
        return cell_value
    return cell_value


def accountsmap():
    df = pd.read_excel("acc_map1.xlsx",header=0)
    # replace the NaN as false
    df = df.fillna(False)
    # import pdb;pdb.set_trace()
    df['vchr_module_name'] = df['Type']
    df['vchr_category'] = df.get('value').str.upper()# if not df.get('value').empty else None
    df['COA Code'] = df.get('COA Code').apply(str)# if not df.get('COA Code').empty else None
    df['fk_branch_id'] = None
    dct_branch = dict(Branch.objects.annotate(code=Upper('vchr_code')).values_list('code','pk_bint_id'))
    if not set(tuple(df['SAP Branch Code'].str.strip().str.upper())).issubset(tuple(dct_branch.keys())):
        lst_branch = list(set(tuple(df['SAP Branch Code'].str.upper())) - set(tuple(dct_branch.keys())))
        return ({"error_message":"Some Branches ({str_missing_branch}) not found.".format(str_missing_branch=','.join(lst_branch))})
    df['fk_branch_id'] = df['SAP Branch Code'].str.strip().str.upper().map(dct_branch.get)

    dct_account = dict(ChartOfAccounts.objects.annotate(accnum=Upper('vchr_acc_code')).values_list('accnum','pk_bint_id'))
    if not set(tuple(df['COA Code'].str.strip().str.upper())).issubset(tuple(dct_account.keys())):
        lst_account = list(set(tuple(df['COA Code'].str.upper())) - set(tuple(dct_account.keys())))
        return ({"error_message":"Some Accounts ({str_missing_account}) not found.".format(str_missing_account=','.join(lst_account))})
    df['fk_coa_id'] = df['COA Code'].str.strip().str.upper().map(dct_account.get)
    df['int_status'] = 0

    AccountsMap.objects.filter(fk_coa__vchr_acc_code__in=df['COA Code']).update(int_status=1)
    uploadcolumns = ['vchr_module_name','vchr_category','fk_coa_id','int_status','fk_branch_id']
    xlsdf = Savedftosql(df[uploadcolumns],'accounts_map')
    xlsdf.insert_data()
    return 'Success'

def accountsmap2():
    df = pd.read_excel("acc_map2.xlsx",header=0)
    # replace the NaN as false
    df = df.fillna(False)
    df['vchr_module_name'] = df['Type']
    df['vchr_category'] = df.get('value').str.upper()# if not df.get('value').empty else None
    df['COA Code'] = df.get('COA Code').apply(str)# if not df.get('COA Code').empty else None
    df['fk_branch_id'] = None

    dct_account = dict(ChartOfAccounts.objects.annotate(accnum=Upper('vchr_acc_code')).values_list('accnum','pk_bint_id'))
    if not set(tuple(df['COA Code'].str.strip().str.upper())).issubset(tuple(dct_account.keys())):
        lst_account = list(set(tuple(df['COA Code'].str.upper())) - set(tuple(dct_account.keys())))
        return ({"error_message":"Some Accounts ({str_missing_account}) not found.".format(str_missing_account=','.join(lst_account))})
    df['fk_coa_id'] = df['COA Code'].str.strip().str.upper().map(dct_account.get)
    df['int_status'] = 0

    AccountsMap.objects.filter(fk_coa__vchr_acc_code__in=df['COA Code']).update(int_status=1)
    uploadcolumns = ['vchr_module_name','vchr_category','fk_coa_id','int_status']
    xlsdf = Savedftosql(df[uploadcolumns],'accounts_map')
    xlsdf.insert_data()
    return 'Success'
