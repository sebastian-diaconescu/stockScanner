from finvizfinance.quote import finvizfinance
import requests
from bs4 import BeautifulSoup

class FinVizHelper:
    def getStockPE(self, ticker):
        stock = finvizfinance(ticker)
        fundament = stock.TickerFundament()
        return fundament

    def loadNews(self, ticker):
        #url = "https://finviz.com/quote.ashx?t="
        #page = url + ticker
        pageURl = "https://finviz.com/quote.ashx?t=gme"
        headers={'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(pageURl, headers=headers)
        if (response.status_code != 200):
            return "no response from page " + response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        newsTable = soup.find(id="news-table").find_all(tr)
        allArticles = []
        for i in range(len(newsTable)):
            anArticle = newsTable[i].text
            allArticles.append(anArticle)

        return sallArticles
        
        
        