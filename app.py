from flask import Flask, request, jsonify
from finviz_service import FinVizHelper
from database import DBConnection
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
    db.ClearDatabase()
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
    news = finvizHelper.loadNews("gme")

    return jsonify(news)
    #return jsonify(data)

    #return "loaded sentiments"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


