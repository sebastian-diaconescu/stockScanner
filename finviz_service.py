from finvizfinance.quote import finvizfinance


class FinVizHelper:
    def getStockPE(ticker):
        stock = finvizfinance(ticker)
        fundament = stock.TickerFundament()
        return fundament