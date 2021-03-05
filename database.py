from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, FLOAT, DateTime, text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
import re

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
            Column ("ticker", String, nullable=False)
        )     

        Table("reddit", metadata,
            Column ("Id", Integer, primary_key=True, nullable=False),
            Column ("date", DateTime, nullable=False),
            Column ("title", String, nullable=False),
            Column ("content", String, nullable=False),
            Column ("sentiment_score", FLOAT),
            Column ("tickers", String),
            Column ("sub", String, nullable=False)
        )     

        metadata.create_all()
        
    def InsertHeadlineSentiment(self, date, headline, headline_hash, sentiment_score, ticker):
        conn = self.engine.connect()

        insert = "INSERT INTO headline_sentiment (date, headline, headline_hash, sentiment_score, ticker) Values ('"+ str(date) + "', '" + headline + "', '" + headline_hash + "', '" + str(sentiment_score) + "', '" + ticker + "')"
      
        conn.execute(insert)
        conn.close()

    def GetTitleByHash(self, headline_hash):
        conn = self.engine.connect()
        t = text("SELECT * FROM headline_sentiment WHERE headline_hash = '"+ headline_hash +"'")
        result = conn.execute(t)
        
        res = result.first()
        conn.close()

        if (res == None):
            return None
        
        return dict(res)

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
            Column('ticker', String, unique=True),
            Column('name', String),
            Column('sector', String),
            Column('industry', String)
            )

        metadata.create_all()

        conn = self.engine.connect()
        for row in data:
            conn.execute("INSERT INTO revolut_tickers (name, ticker,  sector, industry) VALUES ('"+ row[0] +"', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "') ON CONFLICT (ticker) DO NOTHING;")
            pass
        conn.close()

    def InsertRedditData(self, posts):
        conn = self.engine.connect()
        
        for post in posts:
            content = post['content']
            title = post['title']
            content = re.sub(r'[^a-zA-Z0-9\.\, ]+', '', content)
            title = re.sub(r'[^a-zA-Z0-9\.\, ]+', '', title)
            insert = "INSERT INTO reddit (date, title, content, sub)" + " VALUES " + "('"+ str(post['date']) +"', '" +  title +"', '" + content + "', '" + post['sub'] + "')"
            conn.execute(insert)
            pass
        
        # Close connection
        conn.close()
        return posts

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