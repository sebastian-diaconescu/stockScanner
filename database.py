from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, FLOAT
from sqlalchemy.ext.declarative import declarative_base

class DBConnection:
    def __init__(self):      
        self.engine = create_engine('postgres://dnjeujepwaungq:878cd5627953bf0d4ae99139a3733d9e07bf12429231ece3fc1ef23812468f9f@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/dfuhv8ajipjhcs')
      
    def createTables(self):  
        self.engine.connect()
        
        metadata = MetaData(self.engine)                 
        Table("fundamental", metadata,
            Column('Id', Integer, primary_key=True, nullable=False), 
            Column('whigh52', FLOAT),
            Column('ticker', String),
            )

        metadata.drop_all(self.engine)
        #TODO: remove this or extract into a new server method    
        
        base = declarative_base()
        base.metadata.drop_all(self.engine, checkfirst=False)
        #metadata.create_all()
        

    def InsertData(self, fundamentalData, ticker):
        conn = self.engine.connect()
        high52 = float(fundamentalData["52W High"].replace("%", ""))
        print(high52)
        conn.execute("INSERT INTO fundamental (whigh52, ticker) VALUES ("+ high52 +", '" + ticker + "')")
        # Close connection
        conn.close()