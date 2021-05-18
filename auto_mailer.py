import psycopg2
import pandas as pd
conn = psycopg2.connect("host=localhost dbname=pos_demo user=admin password=tms@123")
cur = conn.cursor()

# from POS import settings


import smtplib
from os.path import basename
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import copy

import sys

import zipfile

from os.path import basename


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]

date_sub1 = (datetime.datetime.today()).strftime ("%d_%B_%Y")

# from branch_stock.models import MailingProduct
# from django.db.models import Q

def make_excel_and_send(lst_data_frame_summary,lst_data_frame,lst_mail,str_about):
    try:
        df_excel_summary=pd.DataFrame(lst_data_frame_summary)

        df_excel=pd.DataFrame(lst_data_frame)


        str_cur_path=os.getcwd()
        excel_file = str_cur_path+'/STOCK/stock_report_'+date_sub1+'_'+str_about.lower().replace(' ','_')+'.xlsx'
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

        df_excel.index = pd.RangeIndex(start=1, stop=df_excel.shape[0]+1, step=1)

        df_excel_summary.to_excel(writer,index=False, sheet_name='Summary',columns=['BRANCH','ITEM','Item code','APX CODE','PRODUCT','BRAND','Dealer Price','MOP','MRP','COST PRICE','STOCK','IN TRANSIT','TOTAL STOCK','TOTAL DEALER PRICE','TOTAL MOP PRICE','TOTAL MRP PRICE','TOTAL COST PRICE'])


        df_excel.to_excel(writer,index=False, sheet_name='Detail',columns=['BRANCH','Item code','APX CODE','PRODUCT','BRAND','ITEM','IMEI/BATCH','Dealer Price','COST PRICE','MOP','MRP','TOTAL AGE','BRANCH AGE','STOCK','TRANSIT'])
        # df_excel_summary.to_excel(writer)

        workbook = writer.book

        worksheet = writer.sheets['Summary']

        for i,width in enumerate(get_col_widths(df_excel_summary)):
            worksheet.set_column(i-1, i-1, width)


        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 70)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(6, 6, 15)

        worksheet.set_column(4, 4, 30)
        worksheet.set_column(8, 8, 15)
        worksheet.set_column(9, 9, 15)
        worksheet.set_column(11, 11, 15)

        worksheet.set_column(13,13, 20)
        worksheet.set_column(14, 14, 20)
        worksheet.set_column(15, 15, 20)


        worksheet = writer.sheets['Detail']


        for i,width in enumerate(get_col_widths(df_excel)):
            worksheet.set_column(i-1, i-1, width)

        worksheet.set_column(3, 3, 30)

        worksheet.set_column(5, 5, 70)
        worksheet.set_column(6, 6, 40)

        worksheet.set_column(7, 7, 20)
        worksheet.set_column(8, 8, 20)

        worksheet.set_column(11, 11, 15)
        worksheet.set_column(12, 12, 15)

        worksheet.set_column(14, 14, 15)

        writer.save()
        file_daily=str_cur_path+'/STOCK/stock_report_'+date_sub1+'_'+str_about.lower().replace(' ','_')+'.xlsx'
        # After the file is closed
        file_daily_zip=str_cur_path+'/STOCK/stock_report_'+date_sub1+'_'+str_about.lower().replace(' ','_')+'.zip'
        # os.chdir(path)


        zipf = zipfile.ZipFile(file_daily_zip,"w", zipfile.ZIP_DEFLATED)
        zipf.write(file_daily,basename(file_daily))
        zipf.close()
        date_sub = (datetime.datetime.today()).strftime ("%d-%B-%Y")

        msg = MIMEMultipart()
        msg['Subject'] = 'Auto Mailer Stock Reports '  +str_about+' , DATED : '+date_sub
        lst_mail=['paulantonyjose@travidux.in']
        msg['To']=", ".join(lst_mail)




        with open(file_daily_zip, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(file_daily_zip)
            )

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file_daily_zip)

        msg.attach(part)



        server = smtplib.SMTP('smtp.pepipost.com', 587)
        server.starttls()

        server.login("shafeer","Tdx@9846100662")
        server.sendmail("info@enquirytrack.com",lst_mail,msg.as_string())


        server.quit()
    except Exception as e:
        print (e)

# it.vchr_item_code,it.vchr_old_item_code as vchr_apx_code,it.vchr_name as item_name,'False' as bln_batch,it.dbl_dealer_cost,it.dbl_mop,br.vchr_name,ROUND(EXTRACT(EPOCH FROM now()::timestamp-gm.dat_purchase::timestamp)/86400) as total_age, ROUND(EXTRACT(EPOCH FROM now()::timestamp - bsm.dat_stock::timestamp)/86400) as branch_age,jsonb_array_elements(bsd.jsn_imei->'imei') as imei,pd.vchr_name as product_name,brd.vchr_name as brand_name,pl.dbl_cost_amnt

def make_data():
    try:
            qry_summary = """select vchr_item_code, vchr_apx_code,dbl_dealer_cost,dbl_mop,COALESCE(int_qty,0::BIGINT),COALESCE(int_transit,0::BIGINT), COALESCE(int_qty,0)+COALESCE(int_transit,0::BIGINT) as int_total, dbl_dealer_cost*(COALESCE(int_qty,0::BIGINT)+COALESCE(int_transit,0::BIGINT)) as total_dealer_cost,dbl_mop* (COALESCE(int_qty,0::BIGINT)+COALESCE(int_transit,0::BIGINT)) as total_mop,vchr_brand_name,vchr_branch_name,vchr_item_name as item_name,vchr_product_name as product_name,COALESCE(dbl_cost_amnt::varchar,'NA'::varchar) as  dbl_cost_amnt,COALESCE(dbl_cost_amnt,0)*(COALESCE(int_qty,0::BIGINT)+COALESCE(int_transit,0::BIGINT)) as total_dealer_cost,dbl_mrp,dbl_mrp* (COALESCE(int_qty,0::BIGINT)+COALESCE(int_transit,0::BIGINT)) as total_mrp from

            (
            select pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,bsid.int_qty as int_qty,CASE WHEN bsid.jsn_imei ->>'imei' ='[]' then NULL else (bsid.jsn_imei->>'imei') END as jsn_imei,
            CASE WHEN bsd.jsn_batch_no ->>'batch' ='[]' then NULL else (bsd.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no ,
                                bsm.dat_stock as dat_branch_stock,(NOW()::DATE-(bsm.dat_stock )::DATE)::INTEGER as int_branch_age,
                                grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                bsm.dat_stock::DATE as dat_stock ,'BRANCH' as vchr_type,fk_product_id
                            from branch_stock_imei_details bsid
                            join branch_stock_details bsd on bsid.fk_details_id = bsd.pk_bint_id
                            join grn_details grd on bsid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join branch_stock_master bsm on bsd.fk_master_id =bsm.pk_bint_id
                            join branch br on bsm.fk_branch_id = br.pk_bint_id
                            join item it on bsd.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id
                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                        UNION ALL
                            select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,(grd.int_avail) as int_qty,CASE WHEN grd.jsn_imei_avail ->>'imei_avail' ='[]' then NULL else (grd.jsn_imei_avail->>'imei_avail') END  as jsn_imei,CASE WHEN COALESCE(grd.vchr_batch_no,'')='' then '' else '["' || vchr_batch_no||'"]' end as jsn_batch_no,
                                (grm.dat_purchase)::DATE as dat_branch_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_branch_age,
                                (grm.dat_purchase)::DATE as dat_purchase_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                grm.dat_purchase::DATE as dat_stock,'GRN' as vchr_type,fk_product_id
                            from grn_details grd
                            join grn_master grm on grd.fk_purchase_id = grm.pk_bint_id
                            join branch br on grm.fk_branch_id = br.pk_bint_id
                            join item it on grd.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id

                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                        UNION ALL
                            select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,stid.int_qty as int_transit, 0 as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->>'imei') END  as jsn_imei,
                                CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
                                NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                stf.dat_transfer::DATE as dat_stock,'TRANSFER' as vchr_type,fk_product_id
                            from stock_transfer_imei_details stid
                            join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
                            join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
                            join branch br on br.pk_bint_id = stf.fk_to_id
                            join item it on ist.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id

                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                            where stf.int_status in (1,2)
                        UNION ALL
                            select   pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,stid.int_qty as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->>'imei') END  as jsn_imei,
                                CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
                                NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                stf.dat_transfer::DATE as dat_stock,'BILLED' as vchr_type,fk_product_id
                            from stock_transfer_imei_details stid
                            join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
                            join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
                            join branch br on br.pk_bint_id = stf.fk_from_id
                            join item it on ist.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id
                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                            where stf.int_status in (0)) as br_data where (int_qty>0 or int_transit>0) and  fk_product_id not in (select pk_bint_id from products where vchr_name ilike 'SMART CHOICE')"""

            cur.execute(qry_summary)
            lst_summary =cur.fetchall()

            lst_data_frame_summary=[]

            dct_mail_summary={}
            dct_mail_summary['COMBINED_PRODUCTS']=[]

            for data in lst_summary:
                dct_data={}
                dct_data['BRANCH']= data[10]
                dct_data['Item code']= data[0]
                dct_data['APX CODE']= data[1]
                dct_data['PRODUCT']= data[12]
                # dct_data['BRAND']= data[4]
                dct_data['ITEM']= data[11]
                dct_data['Dealer Price']= data[2]
                dct_data['MOP']= data[3]
                dct_data['STOCK']= data[4]
                dct_data['IN TRANSIT']= data[5]
                dct_data['TOTAL STOCK']= data[6]
                dct_data['TOTAL DEALER PRICE']= data[7]
                dct_data['TOTAL MOP PRICE']= data[8]
                dct_data['BRAND']= data[9]

                dct_data['COST PRICE']= data[13]
                dct_data['TOTAL COST PRICE']= data[14]

                dct_data['MRP']= data[15]
                dct_data['TOTAL MRP PRICE']= data[16]

                lst_data_frame_summary.append(dct_data)



                if dct_data['PRODUCT'].upper() not in  ['ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH']:

                    if dct_data['PRODUCT'].upper() not in dct_mail_summary:
                        dct_mail_summary[dct_data['PRODUCT'].upper()]=[]

                    dct_mail_summary[dct_data['PRODUCT'].upper()].append(dct_data)
                else:
                    dct_mail_summary['COMBINED_PRODUCTS'].append(dct_data)

                # dct_data['BRANCH AGE']= data[9]

                # dct_data['PRODUCT']= data[10]




            qry_detail_1 = """select vchr_item_code, vchr_apx_code,vchr_item_name as item_name,'False' as bln_batch,dbl_dealer_cost,dbl_mop,vchr_branch_name,int_total_age,int_branch_age,jsn_imei,vchr_product_name as product_name,vchr_brand_name,dbl_cost_amnt,jsn_batch_no,int_qty,int_transit,vchr_type,dbl_mrp,int_status,pk_bint_id from

            (
            select pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,bsid.int_qty as int_qty,CASE WHEN bsid.jsn_imei ->>'imei' ='[]' then NULL else (bsid.jsn_imei->'imei') END as jsn_imei,
            CASE WHEN bsd.jsn_batch_no ->>'batch' ='[]' then NULL else (bsd.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no ,
                                bsm.dat_stock as dat_branch_stock,(NOW()::DATE-(bsm.dat_stock )::DATE)::INTEGER as int_branch_age,
                                grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                bsm.dat_stock::DATE as dat_stock ,'BRANCH' as vchr_type,fk_product_id, '1' as int_status,bsid.pk_bint_id as pk_bint_id
                            from branch_stock_imei_details bsid
                            join branch_stock_details bsd on bsid.fk_details_id = bsd.pk_bint_id
                            join grn_details grd on bsid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join branch_stock_master bsm on bsd.fk_master_id =bsm.pk_bint_id
                            join branch br on bsm.fk_branch_id = br.pk_bint_id
                            join item it on bsd.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id
                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                        UNION ALL
                            select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,(grd.int_avail) as int_qty,CASE WHEN grd.jsn_imei_avail ->>'imei_avail' ='[]' then NULL else (grd.jsn_imei_avail->'imei_avail') END  as jsn_imei,CASE WHEN COALESCE(grd.vchr_batch_no,'')='' then '' else '["' || vchr_batch_no||'"]' end as jsn_batch_no,
                                (grm.dat_purchase)::DATE as dat_branch_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_branch_age,
                                (grm.dat_purchase)::DATE as dat_purchase_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                grm.dat_purchase::DATE as dat_stock,'GRN' as vchr_type,fk_product_id,'2' as int_status,grd.pk_bint_id as pk_bint_id
                            from grn_details grd
                            join grn_master grm on grd.fk_purchase_id = grm.pk_bint_id
                            join branch br on grm.fk_branch_id = br.pk_bint_id
                            join item it on grd.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id

                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                        UNION ALL
                            select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,stid.int_qty as int_transit, 0 as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->'imei') END  as jsn_imei,
                                CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
                                NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                stf.dat_transfer::DATE as dat_stock,'TRANSFER' as vchr_type,fk_product_id,'3' as int_status,stid.pk_bint_id as pk_bint_id
                            from stock_transfer_imei_details stid
                            join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
                            join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
                            join branch br on br.pk_bint_id = stf.fk_to_id
                            join item it on ist.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id

                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                            where stf.int_status in (1,2)
                        UNION ALL
                            select   pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,it.dbl_mrp,0 as int_transit,stid.int_qty as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->'imei') END  as jsn_imei,
                                CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
                                NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
                                (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
                                (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
                                (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
                                (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
                                stf.dat_transfer::DATE as dat_stock,'BILLED' as vchr_type,fk_product_id,'4' as int_status,stid.pk_bint_id as pk_bint_id
                            from stock_transfer_imei_details stid
                            join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
                            join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
                            join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
                            join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
                            join branch br on br.pk_bint_id = stf.fk_from_id
                            join item it on ist.fk_item_id = it.pk_bint_id
                            join price_list pl on pl.fk_item_id = it.pk_bint_id
                            join brands bd on bd.pk_bint_id =it.fk_brand_id
                            join products pd on pd.pk_bint_id = it.fk_product_id
                            where stf.int_status in (0)) as br_data where (int_qty>0 or int_transit>0) and fk_product_id not in (select pk_bint_id from products where vchr_name ilike 'SMART CHOICE'); """


            # import pdb;pdb.set_trace()
            # qry_detail_2 = """select vchr_item_code, vchr_apx_code,vchr_item_name as item_name,'True' as bln_batch,dbl_dealer_cost,dbl_mop,vchr_branch_name,int_total_age,int_branch_age,jsn_batch_no,vchr_product_name as product_name,vchr_brand_name,dbl_cost_amnt,COALESCE(int_qty,int_transit)::INTEGER from
            #
            # (
            # select pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,0 as int_transit,bsid.int_qty as int_qty,CASE WHEN bsid.jsn_imei ->>'imei' ='[]' then NULL else (bsid.jsn_imei->>'imei') END as jsn_imei,
            # CASE WHEN bsd.jsn_batch_no ->>'batch' ='[]' then NULL else (bsd.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no ,
            #                     bsm.dat_stock as dat_branch_stock,(NOW()::DATE-(bsm.dat_stock )::DATE)::INTEGER as int_branch_age,
            #                     grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
            #                     (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
            #                     (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
            #                     (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
            #                     (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
            #                     bsm.dat_stock::DATE as dat_stock ,'BRANCH' as vchr_type
            #                 from branch_stock_imei_details bsid
            #                 join branch_stock_details bsd on bsid.fk_details_id = bsd.pk_bint_id
            #                 join grn_details grd on bsid.fk_grn_details_id = grd.pk_bint_id
            #                 join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
            #                 join branch_stock_master bsm on bsd.fk_master_id =bsm.pk_bint_id
            #                 join branch br on bsm.fk_branch_id = br.pk_bint_id
            #                 join item it on bsd.fk_item_id = it.pk_bint_id
            #                 join price_list pl on pl.fk_item_id = it.pk_bint_id
            #                 join brands bd on bd.pk_bint_id =it.fk_brand_id
            #                 join products pd on pd.pk_bint_id = it.fk_product_id
            #             UNION ALL
            #                 select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,0 as int_transit,(grd.int_avail) as int_qty,CASE WHEN grd.jsn_imei_avail ->>'imei_avail' ='[]' then NULL else (grd.jsn_imei_avail->>'imei_avail') END  as jsn_imei,CASE WHEN COALESCE(grd.vchr_batch_no,'')='' then '' else '["' || vchr_batch_no||'"]' end as jsn_batch_no,
            #                     (grm.dat_purchase)::DATE as dat_branch_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_branch_age,
            #                     (grm.dat_purchase)::DATE as dat_purchase_stock,(NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age,
            #                     (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
            #                     (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
            #                     (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
            #                     (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
            #                     grm.dat_purchase::DATE as dat_stock,'GRN' as vchr_type
            #                 from grn_details grd
            #                 join grn_master grm on grd.fk_purchase_id = grm.pk_bint_id
            #                 join branch br on grm.fk_branch_id = br.pk_bint_id
            #                 join item it on grd.fk_item_id = it.pk_bint_id
            #                 join price_list pl on pl.fk_item_id = it.pk_bint_id
            #
            #                 join brands bd on bd.pk_bint_id =it.fk_brand_id
            #                 join products pd on pd.pk_bint_id = it.fk_product_id
            #             UNION ALL
            #                 select  pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,stid.int_qty as int_transit, 0 as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->>'imei') END  as jsn_imei,
            #                     CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
            #                     NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
            #                     (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
            #                     (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
            #                     (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
            #                     (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
            #                     stf.dat_transfer::DATE as dat_stock,'TRANSFER' as vchr_type
            #                 from stock_transfer_imei_details stid
            #                 join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
            #                 join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
            #                 join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
            #                 join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
            #                 join branch br on br.pk_bint_id = stf.fk_to_id
            #                 join item it on ist.fk_item_id = it.pk_bint_id
            #                 join price_list pl on pl.fk_item_id = it.pk_bint_id
            #
            #                 join brands bd on bd.pk_bint_id =it.fk_brand_id
            #                 join products pd on pd.pk_bint_id = it.fk_product_id
            #                 where stf.int_status in (1,2)
            #             UNION ALL
            #                 select   pl.dbl_cost_amnt as  dbl_cost_amnt,it.dbl_dealer_cost as dbl_dealer_cost,it.dbl_mop,0 as int_transit,stid.int_qty as int_qty,CASE WHEN stid.jsn_imei ->>'imei' ='[]' then NULL else (stid.jsn_imei->>'imei') END  as jsn_imei,
            #                     CASE WHEN stid.jsn_batch_no ->>'batch' ='[]' then NULL else  (ist.jsn_batch_no->>'batch')::TEXT END as jsn_batch_no,
            #                     NULL as dat_branch_stock,NULL as int_branch_age,grm.dat_purchase as dat_purchase_stock, (NOW()::DATE-(grm.dat_purchase)::DATE)::INTEGER as int_total_age ,
            #                     (br.vchr_code) as vchr_branch_code,(br.pk_bint_id) as int_branch_id,(br.vchr_name) as vchr_branch_name,
            #                     (it.vchr_item_code) as vchr_item_code,it.vchr_old_item_code as vchr_apx_code, (it.pk_bint_id) as int_item_id,(it.vchr_name) as vchr_item_name,
            #                     (bd.vchr_code) as vchr_brand_code,(bd.pk_bint_id) as int_brand_id,(bd.vchr_name) as vchr_brand_name,
            #                     (pd.pk_bint_id) as int_product_id,(pd.vchr_name) as vchr_product_name,(pd.vchr_code) as vchr_product_code,
            #                     stf.dat_transfer::DATE as dat_stock,'BILLED' as vchr_type
            #                 from stock_transfer_imei_details stid
            #                 join grn_details grd on stid.fk_grn_details_id = grd.pk_bint_id
            #                 join grn_master  grm on grd.fk_purchase_id = grm.pk_bint_id
            #                 join ist_details ist on  stid.fk_details_id = ist.pk_bint_id
            #                 join stock_transfer stf on ist.fk_transfer_id = stf.pk_bint_id
            #                 join branch br on br.pk_bint_id = stf.fk_from_id
            #                 join item it on ist.fk_item_id = it.pk_bint_id
            #                 join price_list pl on pl.fk_item_id = it.pk_bint_id
            #                 join brands bd on bd.pk_bint_id =it.fk_brand_id
            #                 join products pd on pd.pk_bint_id = it.fk_product_id
            #                 where stf.int_status in (0))  as br_data where br_data.jsn_batch_no IS NOT NULL """
            #
            #



            # qry_detail_7='''select it.vchr_item_code,it.vchr_old_item_code as vchr_apx_code,it.vchr_name as item_name,'True' as bln_batch,it.dbl_dealer_cost,it.dbl_mop,br.vchr_name,ROUND(EXTRACT(EPOCH FROM now()::timestamp-gm.dat_purchase::timestamp)/86400) as total_age, 0 as branch_age,vchr_batch_no as imei,br.vchr_name as branch_name,pd.vchr_name as product_name,brd.vchr_name as brand_name ,int_avail from  grn_details gd   join grn_master gm on gd.fk_purchase_id=gm.pk_bint_id   join item it on it.pk_bint_id=bsd.fk_item_id join products pd on pd.pk_bint_id=it.fk_product_id join brands brd on brd.pk_bint_id= it.fk_brand_id join branch br on br.pk_bint_id=bsm.fk_branch_id join price_list pl on pl.fk_item_id=it.pk_bint_id where int_avail >0 order by item_name '''



            cur.execute(qry_detail_1)
            lst_detail_1=cur.fetchall()





            lst_details=lst_detail_1

            lst_details=sorted(lst_details,key=lambda k : (k[6],k[2]))

            lst_data_frame=[]

            dct_mail_detail={}
            dct_mail_detail['COMBINED_PRODUCTS']=[]

            for data in lst_details:
                dct_data={}
                dct_data['BRANCH']= data[6]
                dct_data['Item code']= data[0]
                dct_data['APX CODE']= data[1]
                dct_data['PRODUCT']= data[10]
                dct_data['BRAND']= data[11]
                dct_data['ITEM']= data[2]


                dct_data['COST PRICE']= data[12]

                # if '[' in str(data[9]) :
                #     dct_data['IMEI/BATCH']= str(data[9]).replace('[','').replace(']','')
                #
                # else:
                #     dct_data['IMEI/BATCH']= data[9]

                dct_data['Dealer Price']= data[4]
                dct_data['MOP']= data[5]

                dct_data['TOTAL AGE']= data[7]
                dct_data['BRANCH AGE']= data[8]

                dct_data['MRP']= data[17]
                # dct_data['BRANCH AGE']= data[9]
                lst_temp=[]
                # dct_data['PRODUCT']= data[10]
                if data[16] =='TRANSFER':

                    if data[9]:
                        # lst_jsn_imei= copy.deepcopy(eval(data[9]))
                        for jsn_imei in data[9]:
                            dct_data_temp=dct_data.copy()
                            dct_data_temp['IMEI/BATCH'] = jsn_imei
                            dct_data_temp['TRANSIT'] = 1
                            dct_data_temp['STOCK'] = 0


                            lst_temp.append(dct_data_temp)

                            # import pdb;pdb.set_trace()

                    elif data[13]:
                        dct_data_temp=dct_data.copy()

                        dct_data_temp['IMEI/BATCH'] = eval(data[13])[0]
                        dct_data_temp['TRANSIT'] = data[15]
                        dct_data_temp['STOCK'] = data[14]

                        lst_temp.append(dct_data_temp)


                        # import pdb; pdb.set_trace()

                        # import pdb;pdb.set_trace()

                        # int_qty  = ins_data.int_qty
                        # for int_count in range(ins_data.int_qty):
                        #     dct_data['jsn_batch_no'] = ins_data.jsn_batch_no[0]
                        #     dct_data['int_transit'] = 1
                        #     dct_data['int_qty'] = 0
                        #     lst_data.append(dct_data.copy())


                else:
                    if data[9]:
                        for jsn_imei in data[9]:
                            dct_data_temp=dct_data.copy()

                            dct_data_temp['IMEI/BATCH'] = jsn_imei
                            dct_data_temp['STOCK'] = 1
                            dct_data_temp['TRANSIT'] = 0

                            # lst_data_frame.append(dct_data)
                            lst_temp.append(dct_data_temp)

                            # import pdb;pdb.set_trace()

                    elif data[13]:
                        dct_data['IMEI/BATCH'] = eval(data[13])[0]
                        dct_data['TRANSIT'] = data[15]
                        dct_data['STOCK'] = data[14]

                        lst_temp.append(dct_data)

                        # lst_data_frame.append(dct_data)
                        # if dct_data['PRODUCT'] not in  ['ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH']:
                        #
                        #     if dct_data['PRODUCT'] not in dct_mail_detail:
                        #         dct_mail_detail[dct_data['PRODUCT']]=[]
                        #
                        #     dct_mail_detail[dct_data['PRODUCT']].append(dct_data)
                        # else:
                        #     dct_mail_detail['COMBINED_PRODUCTS'].append(dct_data)
                # if 'IMEI/BATCH' not in dct_data:
                #     import pdb;pdb.set_trace()
                # if dct_data['IMEI/BATCH']=='32S000015':
                #     import pdb;pdb.set_trace()

                lst_data_frame.extend(lst_temp)
                if dct_data['PRODUCT'] not in  ['ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH']:

                    if dct_data['PRODUCT'] not in dct_mail_detail:
                        dct_mail_detail[dct_data['PRODUCT']]=[]

                    dct_mail_detail[dct_data['PRODUCT']].extend(lst_temp)
                else:
                    dct_mail_detail['COMBINED_PRODUCTS'].extend(lst_temp)


                                # int_qty  = ins_data.int_qty
                                # for int_count in range(ins_data.int_qty):
                                #     dct_data['jsn_batch_no'] = ins_data.jsn_batch_no[0]
                                #     dct_data['int_qty'] = 1






                                            # import pdb;pdb.set_trace()


                        # else:
                        #                                 dct_data['IMEI/BATCH'] = ''
                        #                                 if data[14]:
                        #                                     dct_data['STOCK'] = 1
                        #                                 if data[15]:
                        #
                        #                                     dct_data['TRANSIT'] = 1
                        #
                        #                                 # import pdb;pdb.set_trace()
                        #
                        #                                 lst_data_frame.append(dct_data)
                        #                                 if dct_data['PRODUCT'] not in  ['ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH']:
                        #
                        #                                     if dct_data['PRODUCT'] not in dct_mail_detail:
                        #                                         dct_mail_detail[dct_data['PRODUCT']]=[]
                        #
                        #                                     dct_mail_detail[dct_data['PRODUCT']].append(dct_data)
                        #                                 else:
                        #                                     dct_mail_detail['COMBINED_PRODUCTS'].append(dct_data)
                        #

                # import pdb;pdb.set_trace()



            '''ALL PRODUCTS'''

            # lst_mail=MailingProduct.objects.filter(fk_product_id__isnull=True).values_list('vchr_email',flat=True)
            qry_mail="""SELECT ARRAY_AGG(vchr_email) from mailing_product where fk_product_id IS NULL"""
            cur.execute(qry_mail)
            lst_mail=set(cur.fetchall()[0][0])

            # lst_mail=['paulantonyjose@travidux.in']

            make_excel_and_send(lst_data_frame_summary,lst_data_frame,lst_mail,'ALL PRODUCTS')

            '''ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH'''
            qry_mail="""SELECT ARRAY_AGG(vchr_email) from mailing_product join products pd on mailing_product.fk_product_id=pd.pk_bint_id where pd.vchr_name IN ('ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH')"""
            cur.execute(qry_mail)
            lst_mail=set(cur.fetchall()[0][0])



            # lst_mail=['paulantonyjose@travidux.in']

            make_excel_and_send(dct_mail_summary['COMBINED_PRODUCTS'],dct_mail_detail['COMBINED_PRODUCTS'],lst_mail,'ACC BGN, ACC ZRD , HVA, BT SPEAKERS, SPEAKER ,SMART WATCH, WATCH')

            qry_products="""SELECT ARRAY_AGG(DISTINCT(pd.vchr_name)) from mailing_product join products pd on mailing_product.fk_product_id=pd.pk_bint_id where pd.vchr_name NOT IN ('ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH') AND fk_product_id IS NOT NULL
"""
            cur.execute(qry_products)
            qry_mail_product=cur.fetchall()[0][0]


            # qry_mail_product=MailingProduct.objects.filter(~Q(fk_product_id__isnull=True),~Q(fk_product__vchr_name__in=['ACC BGN','ACC ZRD','HVA','BT SPEAKERS','SPEAKER','SMART WATCH','WATCH'])).distinct().values_list('fk_product__vchr_name',flat=True)

            for data in qry_mail_product:
                qry_products="SELECT ARRAY_AGG(vchr_email) from mailing_product join products pd on mailing_product.fk_product_id=pd.pk_bint_id where pd.vchr_name='"+str(data)+"'"
                cur.execute(qry_products)
                lst_mail=set(cur.fetchall()[0][0])

                # lst_mail=['paulantonyjose@travidux.in']
                if data.upper() in dct_mail_summary:
                    make_excel_and_send(dct_mail_summary[data.upper()],dct_mail_detail[data.upper()],lst_mail,data)
    except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, {'details':date_sub1+'line no: ' + str(e)+str(exc_tb.tb_lineno)})
    finally:
            cur.close()

if __name__ == '__main__':
    make_data()
