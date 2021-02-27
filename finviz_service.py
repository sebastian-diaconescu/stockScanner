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
        page = "https://finviz.com/quote.ashx?t=gme"
        r = requests.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        
        newsTable = soup.find(id="news-table")
        articleSoup = newsTable.findAll('tr')
        
        allArticles = []
        for i in range(len(articleSoup)):
            anArticle = articleSoup[i].text
            allArticles.append(anArticle)

        return allArticles

        