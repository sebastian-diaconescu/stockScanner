from finvizfinance.quote import finvizfinance
import requests
from bs4 import BeautifulSoup

class FinVizHelper:
    def getStockPE(self, ticker):
        #TODO: try to optimize calls 
        stock = finvizfinance(ticker)
        fundament = stock.TickerFundament()
        return fundament

    def loadNews(self, ticker):
        #url = "https://finviz.com/quote.ashx?t="
        #page = url + ticker
        pageURl = "https://finviz.com/quote.ashx?t=gme"
        #TODO: use random list of useragents 
        headers={'User-Agent': 'Mozilla/5.0'}
        #TODO: move this into a method to optimize number of calls to finviz
        response = requests.get(pageURl, headers=headers)
        if (response.status_code != 200):
            return "no response from page " + response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        newsTable = soup.find(id="news-table").find_all("tr")
        allArticles = []
        for i in range(len(newsTable)):
            anArticle = newsTable[i].text
            allArticles.append(anArticle)

        return allArticles
        
        
        