from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, FLOAT, DateTime
from sqlalchemy.ext.declarative import declarative_base


class DBConnection:
    def __init__(self):      
        self.engine = create_engine('postgres://dnjeujepwaungq:878cd5627953bf0d4ae99139a3733d9e07bf12429231ece3fc1ef23812468f9f@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/dfuhv8ajipjhcs')
      
    def createTables(self):  
        self.engine.connect()
        

        metadata = MetaData(self.engine)                 
        Table("fundamental", metadata,
            Column('Id', Integer, primary_key=True, nullable=False), 
            Column('whigh52perc', FLOAT),
            Column('ticker', String),
            )

        Table("headline_sentiment", metadata,
            Column ("Id", Integer, primary_key=True, nullable=False),
            Column ("date", DateTime, nullable=False),
            Column ("headline", String, nullable=False),
            Column ("headline_hash", String, nullable=False),
            Column ("sentiment_score", FLOAT),
            Column ("ticker", String)
        )       

        metadata.create_all()
        
    def InsertHeadlineSentiment(self, date, headline, headline_hash, sentiment_score, ticker):
        conn = self.engine.connect()
        conn.execute("INSERT INTO headline_sentiment (date, headline, headline_hash, sentiment_score, ticker)" + 
        "Values ("+ date + ", " + headline + ", " + headline_hash + ", " + sentiment_score + ", " + ticker + ")")
        conn.close()

    def InsertData(self, fundamentalData, ticker):
        conn = self.engine.connect()
        high52 = fundamentalData["52W High"].replace("%", "")
        
        conn.execute("INSERT INTO fundamental (whigh52perc, ticker) VALUES ('"+ high52 +"', '" + ticker + "')")
        # Close connection
        conn.close()

    def InsertRevolutStockData(self, data):
        self.engine.connect()       
        metadata = MetaData(self.engine)      
        revolutTickerTableName = "revolut_tickers"

        self.drop_table(revolutTickerTableName)

        Table(revolutTickerTableName, metadata,
            Column('Id', Integer, primary_key=True, nullable=False), 
            Column('ticker', String),
            Column('name', String),
            )

        metadata.create_all()

        conn = self.engine.connect()
        for row in data:
            conn.execute("INSERT INTO revolut_tickers (ticker, name) VALUES ('"+ row[1] +"', '" + row[0] + "')")
            pass
        conn.close()

    def drop_table(self, table_name):
        self.engine.connect()
        base = declarative_base()
        metadata = MetaData(self.engine, reflect=True)
        table = metadata.tables.get(table_name)
        if table is not None:
            base.metadata.drop_all(self.engine, [table], checkfirst=True)


    
        
    

    def ClearDatabase(self):
        self.engine.connect()       
        metadata = MetaData(self.engine)                 
        metadata.drop_all(self.engine)