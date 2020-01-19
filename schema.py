
import mysql.connector 
from sodapy import Socrata
import sqlalchemy as db
import pandas as pd
# from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import mapper

class DbSchema:
    def __init__(self, config):
        self.engine = db.create_engine(f'mysql+mysqlconnector://{config.user}:{config.password}@{config.host}/con_bills')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.current_bills_table = self.current_bills()
        self.topics_table = self.topics()
        self.metadata.create_all(self.engine)

    def current_bills(self):
        return db.Table('current_bills', self.metadata,               
            db.Column('BillID', db.String(40), primary_key=True),
            db.Column('BillType', db.String(20)),
            db.Column('Chamber', db.Boolean()),
            db.Column('Cong', db.Integer()),
            db.Column('Cosponsr', db.Float()),
            db.Column('IntrDate', db.DateTime()),
            db.Column('Mult', db.Boolean()),
            db.Column('PLaw', db.Boolean()),
            db.Column('Title', db.String(500)),
            db.Column('Veto', db.Boolean()),
            db.Column('Class', db.Float()),
            db.Column('District', db.Float()),
            db.Column('FrstConH', db.Float()),
            db.Column('FrstConS', db.Float()),
            db.Column('Gender', db.Boolean()),
            db.Column('MRef', db.Boolean()),
            db.Column('NameFull', db.String(40)),
            db.Column('Party', db.Float()),
            db.Column('Postal', db.String(10)),
            db.Column('PassH', db.Boolean()),
            db.Column('PassS', db.Boolean()),
            db.Column('PLawDate', db.DateTime()),
            db.Column('PLawNum', db.String(40)),
            db.Column('ImpBill', db.Boolean()),
            db.Column('Majority', db.Boolean()),
            db.Column('Major', db.Float()),
            db.Column('Minor', db.Float()),
            db.Column('URL', db.String(100)),
            db.Column('Summary', db.String(2000))   
        )

    def topics(self):
        return db.Table('topics', self.metadata,
            db.Column('Index', db.Integer, autoincrement=True, primary_key=True),
            db.Column('BillID', db.String(40), db.ForeignKey("current_bills.BillID"), nullable=False),
            db.Column('dominant_topic', db.Integer)
        )

    def query(self, q):
        # try:
        return pd.read_sql_query(q, self.engine)
        # Pass when no data is returned    
        # except db.ResourceClosedError:
            # pass

    def query_list(self, col, table, distinct = True):
        elts = ['SELECT',
                'DISTINCT' if distinct else '',
                col,
                'FROM',
                table]
        query_str = ' '.join(elts)
        df = self.query(query_str)
        l = df.iloc[:,0].tolist()
        return l