import pandas as pd

df_branch=pd.read_excel('BRANCH.xlsx')



from branch.models import Branch

for ind,row in df_branch.iterrows():
    if  row['Warehouse Code']!=1:
          Branch.objects.filter(vchr_code=row['Warehouse Code']).update(int_pincode=row['Zip Code'],flt_latitude=row['Latitude'],flt_longitude=row['Longitude'])


