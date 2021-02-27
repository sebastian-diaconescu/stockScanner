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

@app.route('/upload-revolut/', methods=['POST'])
def loadRevolut():
    return "Refresh complete"

"""
@app.route('/load-sentiment/', methods=['POST'])
def loadSentiment():
    ticker = request.args.get('ticker')
    db = DBConnection()
    db.createTables()
    db.InsertHeadlineSentiment("Feb-26-21 04:05PM", "test headline", "1hash", 1, "gme")
    return "loaded sentiments"
"""
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


