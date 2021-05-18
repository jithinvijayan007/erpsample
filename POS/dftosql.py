from django.conf import settings
from sqlalchemy import create_engine
import pandas as pd
class Savedftosql(object):
    def __init__(self,df,db,*arg,**kargs):
        self.user = settings.DATABASES['default']['USER']
        self.password = settings.DATABASES['default']['PASSWORD']
        self.database_name = settings.DATABASES['default']['NAME']
        self.db = db
        self.database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=self.user,
        password=self.password,
        database_name=self.database_name,
        )
        self.df = df
        #self.engine = create_engine(self.database_url,echo=False)
        self.engine = create_engine(self.database_url,pool_size=10,max_overflow=20,echo=False)
    def savepromo(self):
        self.df.to_sql(self.db,con=self.engine,if_exists='append')

    def insert_data(self):
        self.df.to_sql(self.db,con=self.engine,if_exists='append',index=False)
