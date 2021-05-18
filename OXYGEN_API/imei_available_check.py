import requests
from datetime import datetime
from datetime import datetime,date,timedelta
import json
str_headers = {'UserId': 'APXAPI', 'SecurityCode': '4135-1471-5866-6461'}

str_stock_url = 'http://oxyapp.hostsaleserver.in:8082/api/apxapi/GetStoreInHandImeiSerialNos?CompanyCode={CompanyCode}&BranchCode={BranchCode}&ItemModelCode={ItemModelCode}&StockType={StockType}'



def Stock_Item_Checking(str_branchCode, item_code,str_imei):
    # import pdb; pdb.set_trace()

    # str_stock_url = str_stock_url.format(CompanyCode='ODS',BranchCode='ALP',ItemModelCode='1022436',StockType='SALE')
    str_stock_url = 'http://oxyapp.hostsaleserver.in:8082/api/apxapi/GetStoreInHandImeiSerialNos?CompanyCode={CompanyCode}&BranchCode={BranchCode}&ItemModelCode={ItemModelCode}&StockType={StockType}'
    str_stock_url = str_stock_url.format(CompanyCode='ODS',BranchCode=str_branchCode,ItemModelCode=item_code,StockType='SALE')
    # ins_response =  json.loads(response.text)
    response = requests.request("GET", str_stock_url, headers=str_headers)
    ins_response =  json.loads(response.text)

    
    str_stock_url = 'http://oxyapp.hostsaleserver.in:8082/api/apxapi/GetStoreInHandImeiSerialNos?CompanyCode={CompanyCode}&BranchCode={BranchCode}&ItemModelCode={ItemModelCode}&StockType={StockType}'
    str_stock_url = str_stock_url.format(CompanyCode='ODS',BranchCode=str_branchCode,ItemModelCode=item_code,StockType='SALE')

    response = requests.request("GET", str_stock_url, headers=str_headers)
    ins_response =  json.loads(response.text)
    if ins_response['Data']:
        lst_imei = [data['SERIAL_NO'] for data in ins_response['Data']]
        if str_imei in lst_imei:
            return 'Available'
        else:
            return "Not Available"

      