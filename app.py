from flask import Flask, request, jsonify
from finviz_service import FinVizHelper
from database import DBConnection
from sentiment_scanner import SentimentScaner
from reddit_service import RedditLoader

import hashlib
import csv
import codecs

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/load-fundamentals/', methods=['POST'])
def scanFinvizTicker():
    ticker = request.args.get('ticker')
    stockFundamental = FinVizHelper().getStockPE(ticker)
    db = DBConnection()
    db.createTables()
    db.InsertData(stockFundamental, ticker)
    
    return stockFundamental

@app.route('/upload-revolut', methods=['POST'])
def loadRevolut():
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    data = []
    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    #csvResult = jsonify(data)
    
    db = DBConnection()
    db.InsertRevolutStockData(data)
    return "Refresh complete"

@app.route('/load-sentiment', methods=['POST'])
def loadSentiment():
    ticker = request.args.get('ticker')
    db = DBConnection()
    db.createTables()

    
    finvizHelper = FinVizHelper()
    news = finvizHelper.loadNews(ticker)
    #news = finvizHelper.mockLoadNews("gme")
    data = []
    sentimentScaner = SentimentScaner()
    for story in news:
        split = story.split("  ")
        date = split[0]
        title = split[1]
        sentimentScore = sentimentScaner.GetSentiment(title)
        res = {"date":date, "title": title, "score": sentimentScore, "ticker":ticker }
        hashVal = hashlib.md5(title.encode('utf-8')).hexdigest() 

        data = db.GetTitleByHash(hashVal)
        if (data == None):
            db.InsertHeadlineSentiment(date, title, hashVal, sentimentScore, ticker)
        

        data.append(res)
        pass



    return jsonify(data)


@app.route('/load-reddit-posts', methods=['POST'])
def loadReddit():
     sub = request.args.get('sub')
     redditLoader = RedditLoader()
     #posts = redditLoader.GetPostsFromBF(sub)
     posts = redditLoader.GetPostsFromPraw(sub)
     db = DBConnection()
     db.drop_table("reddit")
     db.createTables()
     res = db.InsertRedditData(posts)
     return jsonify(res)
     

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


