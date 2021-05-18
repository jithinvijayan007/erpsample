import pandas as pd
import psycopg2
from datetime import datetime
import random
import json
import time
def branchfromexcel():
    try:
        time_start = time.time()
        try:
            # import pdb; pdb.set_trace()
            conn = psycopg2.connect(host="localhost",database="pos_sap_new", user="admin", password="tms@123")
            cur = conn.cursor()
            conn.autocommit = True
            df = pd.read_excel("Main master.xlsx",header=0,sheet_name="location master")
        except Exception as e:
            return 'cannot read excel'
        lst_added = []
        lst_updated = []
        for ind,row in df.iterrows():
            vchr_branch_name = row['BRANCH NAME']
            vchr_branch_code = row['BR.CODE']

            cur.execute("select pk_bint_id,vchr_code from branch where upper(vchr_name) = '"+vchr_branch_name.upper()+"';")
            ins_branch = cur.fetchall()

            if not ins_branch:
                cur.execute("insert into branch(vchr_name,vchr_code) values('"+vchr_branch_name.upper()+"','"+vchr_branch_code+"')")
                lst_added.append(vchr_branch_name)
            else:
                if ins_branch[0][1] != vchr_branch_code:
                    cur.execute("update branch set vchr_code = '"+vchr_branch_code+"' where pk_bint_id = '"+str(ins_branch[0][0])+"';")
                    lst_updated.append(vchr_branch_name)

        print('added - ')
        print(len(lst_added))
        print('updated - ')
        print(len(lst_updated))
        print("success")

    except Exception as e:
        import pdb; pdb.set_trace()
        raise

if __name__ == '__main__':
    branchfromexcel()
