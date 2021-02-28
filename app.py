from flask import Flask, request, jsonify
from finviz_service import FinVizHelper
from database import DBConnection
from sentiment_scanner import SentimentScaner
from reddit_service import RedditLoader
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

    db.InsertHeadlineSentiment("Feb-26-21 04:05PM", "test headline", "1hash", "1", "gme")
    data = db.GetTitleByHash("1has2h")

    finvizHelper = FinVizHelper()
    #news = finvizHelper.loadNews("gme")
    news = finvizHelper.mockLoadNews("gme")
    data = []
    sentimentScaner = SentimentScaner()
    for story in news:
        
        split = story.split("  ")
        date = split[0]
        title = split[1]
        res = {"date":date, "title": title, "score": "", "ticker":ticker }
        
        res["score"] = sentimentScaner.GetSentiment(title)

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


