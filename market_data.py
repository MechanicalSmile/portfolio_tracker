import yfinance as yf

class MarketData:
    def __init__(self, tickers, period='5y', interval='1d'):
        self.tickers = tickers
        self.period = period
        self.interval = interval

    def fetch_data(self):
        return yf.download(self.tickers, period=self.period, interval=self.interval, group_by='ticker', auto_adjust=True)

    def get_fundamentals(self, ticker):
        info = yf.Ticker(ticker).info

        return {
            'pe_ratio': info.get('trailingPE'),
            'pb_ratio': info.get('priceToBook'),
            'dividend_yield': info.get('dividendYield'),
            'dividend_rate': info.get('dividendRate'),
            'beta': info.get('beta'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            'roe': info.get('returnOnEquity'),
            'free_cash_flow': info.get('freeCashflow')
        }

