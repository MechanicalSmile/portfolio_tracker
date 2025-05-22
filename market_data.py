# Import the Yahoo Finance API wrapper (yfinance) to retrieve market and fundamental data
import yfinance as yf

class MarketData:
    def __init__(self, tickers, period='5y', interval='1d'):
        """
        Initialize the MarketData object.
        
        Parameters:
        - tickers (list or str): List of ticker symbols (e.g., ['AAPL', 'GOOGL']) or a single string.
        - period (str): Time span for historical data (default is '5y' for 5 years).
        - interval (str): Data granularity (e.g., '1d' = daily prices, '1wk' = weekly).
        """
        self.tickers = tickers          # Stock tickers to analyze
        self.period = period            # Historical window to fetch data over
        self.interval = interval        # Frequency of time series data (e.g., daily)

    def fetch_data(self):
        """
        Downloads historical price data for the provided tickers using yfinance.

        Returns:
        - A DataFrame with multi-level columns if multiple tickers are provided,
          or a single-index DataFrame for a single ticker.
        """
        return yf.download(
            self.tickers,
            period=self.period,
            interval=self.interval,
            group_by='ticker',      # Group data under each ticker if multiple tickers
            auto_adjust=True        # Adjust prices for splits/dividends (more realistic)
        )

    def get_fundamentals(self, ticker):
        """
        Retrieves fundamental data for a given ticker symbol using yfinance's `.info` attribute.

        Parameters:
        - ticker (str): Single ticker symbol to analyze (e.g., 'AAPL').

        Returns:
        - A dictionary containing key valuation and performance metrics. All keys are optional;
          missing data will return None if not available via Yahoo Finance.
        """
        info = yf.Ticker(ticker).info   # Fetch metadata and financial info from Yahoo

        return {
            'pe_ratio': info.get('trailingPE'),          # Price-to-Earnings Ratio
            'pb_ratio': info.get('priceToBook'),         # Price-to-Book Ratio
            'dividend_yield': info.get('dividendYield'), # Dividend Yield (as a decimal, e.g., 0.015 = 1.5%)
            'dividend_rate': info.get('dividendRate'),   # Annual dividend amount per share
            'beta': info.get('beta'),                    # Beta coefficient (volatility vs market)
            'revenue_growth': info.get('revenueGrowth'), # Revenue growth rate (YoY)
            'earnings_growth': info.get('earningsGrowth'), # Earnings growth rate (YoY)
            'roe': info.get('returnOnEquity'),           # Return on Equity (Net Income / Equity)
            'free_cash_flow': info.get('freeCashflow')   # Free Cash Flow (operating - capital expenses)
        }
