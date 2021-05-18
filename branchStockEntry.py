import pandas as pd
import psycopg2
from datetime import datetime
import random
import json
import time
cell_value = ''

def fillnan(value):
    global cell_value
    if value:
        cell_value = value
        return cell_value
    return cell_value

def branchstockexcel():
    try:
        try:
            time_start = time.time()
            conn = psycopg2.connect(host="localhost",database="pos", user="admin", password="uDS$CJ8j")
            cur = conn.cursor()
            conn.autocommit = True
            

        except Exception as e:
            print('cannot read excel')
            return 'cannot read excel'
        lst_file =['WHO1.xlsx']
        # lst_file = ['BPS.xlsx','CVD.xlsx','HIL.xlsx','KND.xlsx','MKD.xlsx','PAVR.xlsx','TBR.xlsx','HL.xlsx','DHO.xlsx','KLM.xlsx','KPY.xlsx','MUV.xlsx','PBR.xlsx',' TPR.xlsx']
        # lst_file = ['3GH.xlsx','GDP.xlsx','ITS.xlsx',' KSD.xlsx','MRK.xlsx','PMN.xlsx','WHO1.xlsx','CAM.xlsx','IJK.xlsx','KNS.xlsx',' KTD.xlsx','PAL.xlsx','ROC.xlsx','WHO3.xlsx']
        # lst_file = ['EDA.xlsx','KRD.xlsx','MPD.xlsx','PTM.xlsx','THL.xlsx','KON.xlsx','MAL.xlsx','MUK.xlsx','SBY.xlsx','TLP.xlsx']
        for str_file in lst_file:
            df = pd.read_excel(str_file,header=0)
            df = df.fillna(False)
            df['BRANCH'] = df['BRANCH'].apply(lambda branch: fillnan(branch))
            # df['APX CODE'] = df['APX CODE'].apply(lambda branch: fillnan(branch))
            df['ITEM'] = df['ITEM'].apply(lambda branch: fillnan(branch))
            lst_item_code =[]
            lst_branch_code=[]
            lst_no_imei = []
            lst_no_batch = []
            dct_branch_stock = {}
            for ind,row in df.iterrows():
                vchr_branch = row['BRANCH'].upper()
                if str(vchr_branch).upper() == "NAN" or str(vchr_branch).upper() == "NIL":
                    vchr_branch = ""
                vchr_item = row['ITEM']
                if str(vchr_item).upper() == "NAN" or str(vchr_item).upper() == "NIL":
                    vchr_item = ""
                vchr_imei_list = row[' IMEI NO']
                vchr_batch_list = row['BATCH NO']
                int_qty = row['QTY']
                if str(int_qty).upper() == "NAN" or str(int_qty).upper() == "NIL":
                    int_qty = 0
                if str(vchr_imei_list).upper() == "NAN" or str(vchr_imei_list).upper() == "NIL":
                    lst_no_imei.append(vchr_item)
                    str_imei = ""
                else:
                    str_imei = vchr_imei_list
                if str(vchr_batch_list).upper() == "NAN" or str(vchr_batch_list).upper() == "NIL":
                    lst_no_batch.append(vchr_item)
                    str_batch = ""
                else:
                    str_batch = vchr_batch_list

                if type(str_batch) is float:
                    str_batch = int(str_batch)
                if vchr_branch not in dct_branch_stock:
                    dct_branch_stock[vchr_branch] = {}
                    dct_branch_stock[vchr_branch][vchr_item] = {}
                    dct_branch_stock[vchr_branch][vchr_item]["lst_imei"] = []
                    dct_branch_stock[vchr_branch][vchr_item]["lst_batch"] = []
                    dct_branch_stock[vchr_branch][vchr_item]["int_quantity"] = int_qty
                    if str_imei:
                        dct_branch_stock[vchr_branch][vchr_item]["lst_imei"].append(str(str_imei))
                    if str_batch:
                        # import pdb; pdb.set_trace()
                        dct_branch_stock[vchr_branch][vchr_item]["lst_batch"].append(str(str_batch))

                elif vchr_item not in dct_branch_stock[vchr_branch]:
                    dct_branch_stock[vchr_branch][vchr_item] = {}
                    dct_branch_stock[vchr_branch][vchr_item]["lst_imei"] = []
                    dct_branch_stock[vchr_branch][vchr_item]["lst_batch"] = []
                    dct_branch_stock[vchr_branch][vchr_item]["int_quantity"] = int_qty
                    if str_imei:
                        dct_branch_stock[vchr_branch][vchr_item]["lst_imei"].append(str(str_imei))
                    if str_batch:
                        dct_branch_stock[vchr_branch][vchr_item]["lst_batch"].append(str(str_batch))

                else:
                    dct_branch_stock[vchr_branch][vchr_item]["int_quantity"] += int_qty
                    if str_imei:
                        dct_branch_stock[vchr_branch][vchr_item]["lst_imei"].append(str(str_imei))
                    if str_batch:
                        dct_branch_stock[vchr_branch][vchr_item]["lst_batch"].append(str(str_batch))


            dct_dbl_tax = {}
            dct_dbl_tax['CGST'] = 0
            dct_dbl_tax['SGST'] = 0
            dct_dbl_tax['IGST'] = 0
            dct_dbl_tax = json.dumps(dct_dbl_tax)
            dbl_total_amount = 0
            cur.execute("select pk_bint_id from supplier where vchr_name = 'OB VENDOR'")
            ins_suppler_id = cur.fetchall()
            int_supplier_id = ins_suppler_id[0][0]
            str_grpo = 'GRP/OB/'
            cur.execute("select int_number from document where vchr_module_name = 'GRN'")
            int_index = cur.fetchall()[0][0]
            for ins_branch_name in dct_branch_stock:
                cur.execute("select pk_bint_id,int_type from branch where vchr_code = '"+ins_branch_name+"';")
                ins_branch = cur.fetchall()
                if not ins_branch:
                    lst_branch_code.append(ins_branch_name)
                    continue
                else:
                    int_index+=2
                    vchr_purchase = str_grpo+ins_branch_name+'/'+str(int_index).zfill(4)
                    int_index +=1
                    if ins_branch[0][1] == 1:
                        cur.execute("insert into grn_master(vchr_purchase_num,dat_purchase,fk_branch_id,dbl_total,fk_supplier_id,dat_created) values('"+vchr_purchase+"','"+str(datetime.now())+"',(select pk_bint_id from branch where int_type = 2 limit 1),'"+str(dbl_total_amount)+"','"+str(int_supplier_id)+"','"+str(datetime.now())+"') returning pk_bint_id;")
                    else:
                        cur.execute("insert into grn_master(vchr_purchase_num,dat_purchase,fk_branch_id,dbl_total,fk_supplier_id,dat_created) values('"+vchr_purchase+"','"+str(datetime.now())+"',(select pk_bint_id from branch where vchr_code='"+ins_branch_name+"' limit 1),'"+str(dbl_total_amount)+"','"+str(int_supplier_id)+"','"+str(datetime.now())+"') returning pk_bint_id;")
                    int_grn_master = cur.fetchone()[0]
                    int_branch_id = ins_branch[0][0]
                    if ins_branch[0][1] == 1:
                        cur.execute("insert into branch_stock_master(dat_stock,fk_branch_id,dbl_tax,dbl_amount,jsn_tax) values('"+str(datetime.now())+"','"+str(int_branch_id)+"',0,0,'"+str(dct_dbl_tax)+"') returning pk_bint_id;")
                        ins_branch_stock_master = cur.fetchone()
                        int_branch_stock_master_id = ins_branch_stock_master[0]


                    for ins_item_name in dct_branch_stock[ins_branch_name]:
                        cur.execute("select pk_bint_id,dbl_supplier_cost,dbl_mop from item where vchr_item_code = '"+str(ins_item_name)+"'")
                        ins_item = cur.fetchall()

                        if ins_item:
                            int_item_id = ins_item[0][0]
                            dct_imei = {"imei":dct_branch_stock[ins_branch_name][ins_item_name]["lst_imei"]}
                            dct_imei = json.dumps(dct_imei)
                            dct_imei_avail = {"imei_avail":dct_branch_stock[ins_branch_name][ins_item_name]["lst_imei"]}
                            dct_imei_avail = json.dumps(dct_imei_avail)
                            dct_imei_avail_dummy = {"imei_avail":[]}
                            dct_imei_avail_dummy = json.dumps(dct_imei_avail_dummy)
                            dct_batch = {"batch":dct_branch_stock[ins_branch_name][ins_item_name]["lst_batch"]}
                            str_batch = dct_branch_stock[ins_branch_name][ins_item_name]["lst_batch"][0] if dct_branch_stock[ins_branch_name][ins_item_name]["lst_batch"] else ""
                            dct_batch = json.dumps(dct_batch)
                            int_qty = int(dct_branch_stock[ins_branch_name][ins_item_name]["int_quantity"])
                            dbl_supplier_cost = ins_item[0][1]
                            dbl_mop = ins_item[0][2]
                            dbl_total_amount += dbl_mop * int_qty
                            grn_total_amount = dbl_mop * int_qty
                                # cur.execute("insert into branch_stock_details(fk_item_id,fk_master_id,int_qty,jsn_imei,jsn_imei_avail,jsn_batch_no) values('"+str(int_item_id)+"','"+str(int_branch_stock_master_id)+"','"+str(int_qty)+"','"+str(dct_imei)+"','"+str(dct_imei)+"','"+str(dct_batch)+"')returning pk_bint_id; ")

                            if ins_branch[0][1] == 1:
                                cur.execute("insert into branch_stock_details(fk_item_id,fk_master_id,int_qty,int_received,jsn_imei,jsn_imei_avail,jsn_batch_no) values("+str(int_item_id)+","+str(int_branch_stock_master_id)+","+str(int_qty)+","+str(int_qty)+",'"+str(dct_imei)+"','"+str(dct_imei)+"','"+str(dct_batch)+"')returning pk_bint_id; ")
                                ins_branch_stock_details = cur.fetchone()
                                int_branch_stock_details_id = ins_branch_stock_details[0]

                                cur.execute("insert into grn_details(fk_item_id,int_qty,int_avail,dbl_costprice,dbl_ppu,dbl_total_amount,jsn_imei,jsn_imei_avail,fk_purchase_id,vchr_batch_no) values('"+str(int_item_id)+"','"+str(int_qty)+"',0,'"+str(dbl_supplier_cost)+"','"+str(dbl_mop)+"','"+str(grn_total_amount)+"','"+str(dct_imei)+"','"+str(dct_imei_avail_dummy)+"','"+str(int_grn_master)+"','"+str(str_batch)+"') returning pk_bint_id;")
                                int_grn_details = cur.fetchone()[0]

                                cur.execute("insert into branch_stock_imei_details(fk_details_id,int_qty,int_received,jsn_imei,jsn_imei_reached,jsn_batch_no,jsn_batch_reached,fk_grn_details_id) values("+str(int_branch_stock_details_id)+","+str(int_qty)+","+str(int_qty)+",'"+str(dct_imei)+"','"+str(dct_imei)+"','"+str(dct_batch)+"','"+str(dct_batch)+"','"+str(int_grn_details)+"')returning pk_bint_id; ")
                            else:
                                cur.execute("insert into grn_details(fk_item_id,int_qty,int_avail,dbl_costprice,dbl_ppu,dbl_total_amount,jsn_imei,jsn_imei_avail,fk_purchase_id,vchr_batch_no) values('"+str(int_item_id)+"','"+str(int_qty)+"',"+str(int_qty)+",'"+str(dbl_supplier_cost)+"','"+str(dbl_mop)+"','"+str(grn_total_amount)+"','"+str(dct_imei)+"','"+str(dct_imei_avail)+"','"+str(int_grn_master)+"','"+str(str_batch)+"') returning pk_bint_id;")
                                # int_grn_details = cur.fetchone()[0]

                        else:
                            lst_item_code.append(ins_item_name)

                if dbl_total_amount != 0:
                    cur.execute("update grn_master set dbl_total = '"+str(dbl_total_amount)+"' where pk_bint_id = '"+str(int_grn_master)+"';")


            # import pdb; pdb.set_trace()
            if lst_branch_code or lst_item_code:
                #creating dataframes
                lst_branch_code = list(set(lst_branch_code))
                lst_item_code = list(set(lst_item_code))
                df_branch = pd.DataFrame({'BRANCH CODE':lst_branch_code})
                df_item = pd.DataFrame({'ITEM CODE':lst_item_code})
                #creating and writing to excel
                excel_file = 'items&branch_not_in_table.xlsx'
                file_name_export = excel_file
                writer = pd.ExcelWriter(file_name_export,engine='xlsxwriter')
                df_item.to_excel(writer,sheet_name='Sheet1',index=True, startrow=0,startcol=0)
                df_branch.to_excel(writer,sheet_name='Sheet2',index=True, startrow=0,startcol=0)
                writer.save()

            print('sucess')
            # print(lst_item_code)
            print(len(lst_item_code))
            print(len(lst_branch_code))
            print(time.time()-time_start)
    except Exception as e:
        import pdb; pdb.set_trace()
        raise

if __name__ == '__main__':
    branchstockexcel()
