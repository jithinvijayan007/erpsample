import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
conn = psycopg2.connect(host="localhost", database="pos", user="admin", password="charls@92")
cur = conn.cursor(cursor_factory = RealDictCursor)
conn.autocommit = True


def address():
    try:
        excel_file = pd.ExcelFile('branch_details_PINCODE.xlsx')
        df = pd.read_excel(excel_file, 'branch details PINCODE', header = 0)
        for ind,row in df.iterrows():
            cur.execute("SELECT * FROM branch WHERE vchr_code='"+row['BRANCH CODE']+"'")
            if cur.fetchall():
                cur.execute("UPDATE branch SET vchr_address='"+row['Address - ID PINCODE']+"' WHERE vchr_code='"+row['BRANCH CODE']+"'")
            else:
                print(row['BRANCH'])

        conn.close()
        print("Success")
    except Exception as e:
        print("error :"+str(e))


if __name__ == '__main__':
    address()
