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
        pageURl = "https://finviz.com/quote.ashx?t=" + ticker
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

    def mockLoadNews(self, ticker):
        return [
                "Feb-27-21 06:06AM  Ignore GameStop and AMC: These Growth Stocks Are Poised to Double Motley Fool",
                "03:15AM  [video]Kass: Time to Introduce a Financial Transaction Tax and End Weekly Stock Options TheStreet.com",
                "Feb-26-21 11:24PM  Robinhood to Plan Confidential IPO Filing as Soon as March Bloomberg -6.43%",
                "06:36PM  These Are The Best Robinhood Stocks To Buy Or Watch Now Investor's Business Daily",
                "06:31PM  Why GameStop Stock Traders Should Beware The 'Law Of Twos And Threes' Benzinga",
                "05:34PM  The Best Online Brokers for 2021: The Rise of the Individual Investor and Fintech Apps Barrons.com",
                "04:39PM  GameStop Stock Surged Again This Week. Why Analysts Dont Think It Will Last. Barrons.com",
                "04:34PM  GameStop stock gains 150% on week for only its second best week ever MarketWatch",
                "04:13PM  GameStop Posts Best Week in a Month Fueled by Reddit Frenzy Bloomberg",
                "03:12PM  SEC Is Examining Robinhoods Trading Halts, Options Practices Barrons.com",
                "03:04PM  GameStop saga illustrates rising noise-trader risk that could feed market volatility, warns quantitative analyst MarketWatch",
                "02:04PM  The Short Selling Environment Has Never Been Worse Bloomberg",
                "02:01PM  Jim Cramer: This GameStop Nonsense Has Gotten Out of Hand TheStreet.com",
                "01:42PM  Dow Slips As Dems Move To Pass Stimulus Bill; Pelosi Says This Is 'Necessary'; Apple Rebounds Investor's Business Daily",
                "01:10PM  Dow Jones Dips, Nasdaq Rallies As Tech Stocks Rebound; House To Vote On Stimulus Bill Investor's Business Daily",
                "12:21PM  GameStop Stock Volatility Could Get Even Worse. Heres Why. Barrons.com",
                "11:46AM  Why BofA Is Bearish On GameStop Stock: 'Turnarounds Are Tough' Benzinga",
                "11:40AM  Here We Go Again: GameStop, 10 Most Shorted Stocks Back In Play Investor's Business Daily",
                "11:38AM  Will This IPO Be the Ultimate Reddit Stock? Motley Fool"]
                
        
        
        