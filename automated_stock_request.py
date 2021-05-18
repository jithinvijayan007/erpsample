import pandas as pd
from math import floor
import psycopg2
from datetime import datetime,timedelta
# from psycopg2.extras import RealDictconnsor
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from io import StringIO


def stock_request():
    try:
        try:
            db_connetion_string = "postgres://admin:tms@123@localhost/rol_test"
            conn = create_engine(db_connetion_string)
            # conn = conn.connsor(connsor_factory = RealDictconnsor)
            # conn.autocommit = True
        except Exception as e:
            print('cannot connect database')

        dat_from = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        dat_to = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        int_days = 7
        rst_rol=conn.execute("select jsn_data from tools where vchr_tool_code='ROL' and int_status=1").fetchall()
        # rst_rol = conn.fetchall()
        rst_rol =  rst_rol[0]['jsn_data'][0]  if rst_rol else 1
        rst_sales_details = conn.execute('select fk_branch_id as branch_id,fk_item_id as item,sum(int_qty) as qty from sales_details sd join sales_master sm on sm.pk_bint_id=sd.fk_master_id group by 1,2').fetchall()
        # rst_sales_details = conn.fetchall()
        if not rst_sales_details:
            return
        rst_stock_details = conn.execute('select fk_branch_id as branch_id,fk_item_id as item,sum(int_qty) as qty from branch_stock_details bd join branch_stock_master bm on bm.pk_bint_id=bd.fk_master_id group by 1,2').fetchall()
        # rst_stock_details = conn.fetchall()
        rst_request_num = conn.execute("select vchr_short_code,int_number from document where vchr_module_name='STOCK REQUEST'").fetchall()
        # rst_request_num = conn.fetchall()
        str_short_code = 'AUTO-'+rst_request_num[0]['vchr_short_code']
        int_number = rst_request_num[0]['int_number']
        dct_stock_request = {}
        # import pdb;pdb.set_trace()
        for ins_data in rst_sales_details:
            if ins_data['branch_id'] not in dct_stock_request:
                dct_stock_request[ins_data['branch_id']]={}
                dct_stock_request[ins_data['branch_id']][ins_data['item']]={}
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_from_id'] = ins_data['branch_id']
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_to_id'] = 1270
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_item_id'] = ins_data['item']
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['int_qty'] = floor((ins_data['qty']/int_days)*rst_rol)
                if not dct_stock_request[ins_data['branch_id']][ins_data['item']]['int_qty']:
                    del dct_stock_request[ins_data['branch_id']][ins_data['item']]

            else:
                dct_stock_request[ins_data['branch_id']][ins_data['item']]={}
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_from_id'] = ins_data['branch_id']
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_to_id'] = 1270
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['fk_item_id'] = ins_data['item']
                dct_stock_request[ins_data['branch_id']][ins_data['item']]['int_qty'] = floor((ins_data['qty']/int_days)*rst_rol)
                if not dct_stock_request[ins_data['branch_id']][ins_data['item']]['int_qty']:
                    del dct_stock_request[ins_data['branch_id']][ins_data['item']]
        for ins_stock in rst_stock_details:
            if ins_stock['branch_id'] in dct_stock_request and ins_stock['item'] in dct_stock_request[ins_stock['branch_id']]:
                # if ins_stock['item'] in dct_stock_request[ins_stock['branch_id']]:
                if ins_stock['qty'] >= dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['int_qty']:
                    # import pdb;pdb.set_trace()
                    del dct_stock_request[ins_stock['branch_id']][ins_stock['item']]
                else:
                    str_request_no = str_short_code + '-' + str(int_number+1).zfill(4)
                    int_number=int_number+1
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['int_qty'] -= ins_stock['qty']
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['dat_request'] = datetime.now()
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['vchr_stkrqst_num'] = str_request_no
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['vchr_remarks'] = 'Automated Request'
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['dat_created'] = datetime.now()
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['dat_expected'] = datetime.now() + timedelta(2)
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['int_doc_status'] = 0
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['int_status'] = 0
                    dct_stock_request[ins_stock['branch_id']][ins_stock['item']]['int_automate'] = 2
                    
        import pdb;pdb.set_trace()
        lst_requests = list(list(dct_stock_request.values())[0].values())
        lst_stock_request = []
        dct_stock_request_master = {}
        # for dct_request in lst_requests:
        #     if dct_request['vchr_stkrqst_num'] not in dct_stock_request_master:
        df_request = pd.DataFrame()
        df = pd.DataFrame(lst_requests)
        df_request['dat_request'] = df['dat_request']
        df_request['vchr_stkrqst_num'] = df['vchr_stkrqst_num']
        df_request['vchr_remarks'] = df['vchr_remarks']
        df_request['dat_created'] = df['dat_created']
        df_request['dat_expected'] = df['dat_expected']
        df_request['int_doc_status'] = df['int_doc_status']
        df_request['int_status'] = df['int_status']
        df_request['int_automate'] = df['int_automate']
        df_request['fk_from_id'] = df['fk_from_id']
        df_request['fk_to_id'] = df['fk_to_id']
        df_request=df_request[df_request.dat_request.notnull()]

        df_request.to_sql(con=conn,if_exists='append',index=False,name='stock_request')
        rst_rol=conn.execute("select array_agg(vchr_stkrqst_num||':'||pk_bint_id) from stock_request where vchr_stkrqst_num in ('"+asx+"')").fetchall()
        





    except Exception as e:
        print(str(e))
    


if __name__ == '__main__':
    stock_request()
