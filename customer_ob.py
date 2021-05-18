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
    df = pd.read_excel("/home/renjunapaul/Downloads/cusomer_ob.xlsx",header=0)
    df = df.fillna(False)
    
