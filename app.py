from flask import Flask, request, jsonify
from finviz_service import FinVizHelper
from database import DBConnection
import csv
import codecs
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/scan/')
def scanFinvizTicker():
    ticker = request.args.get('ticker')
    stockFundamental = FinVizHelper().getStockPE(ticker)
    db = DBConnection()
    db.createTables()
    db.InsertData(stockFundamental, ticker)
    db.ClearDatabase()
    return stockFundamental

@app.route('/uploadrevolut', methods=['POST'])
def myroute():
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    data = []
    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    csvResult = jsonify(data)
    
    db = DBConnection()
    db.InsertRevolutStockData(data)

    return csvResult

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


