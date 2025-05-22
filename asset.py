from metrics import (
    calculate_daily_returns, calculate_average_daily_return, calculate_yearly_return,
    calculate_sharpe_ratio, calculate_sortino_ratio,
    calculate_volatility, calculate_max_drawdown,
)
from market_data import MarketData
import pandas as pd

class Asset:
    def __init__(self, ticker, price_data):
        """
        Initialize an Asset instance for analysis of a single stock or ETF.

        Parameters:
        - ticker (str): Ticker symbol of the asset (e.g., 'AAPL')
        - price_data (pd.DataFrame): Price data for one or more assets, with either:
            - MultiIndex columns: (ticker, field), e.g. ('AAPL', 'Close')
            - Single asset: flat column index with 'Close'
        """
        self.ticker = ticker

        # Extract close prices based on whether data is multi-asset or single-asset
        if isinstance(price_data.columns, pd.MultiIndex):
            self.data = price_data[ticker]['Close']
        else:
            self.data = price_data['Close']

        # Time-sliced versions of the data for return calculation windows
        self.one_year_data = self.data[
            self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365))
        ]
        self.three_year_data = self.data[
            self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365 * 3))
        ]

        # Instantiate MarketData for fundamental lookup (single ticker)
        self.market_data = MarketData([ticker])

    def analyze(self):
        """
        Perform quantitative and fundamental analysis of the asset.

        Returns:
        - dict: Dictionary containing risk/return metrics, return history,
                and selected fundamental ratios.
        """

        # Compute daily returns from one-year price history
        returns = calculate_daily_returns(self.one_year_data)

        # Build dictionary of quantitative metrics
        analysis = {
            'ticker': self.ticker,
            'sharpe_ratio': float(calculate_sharpe_ratio(returns)),
            'sortino_ratio': float(calculate_sortino_ratio(returns)),
            'volatility': float(calculate_volatility(returns)),
            'max_drawdown': float(calculate_max_drawdown(self.one_year_data)),

            # Total return metrics for different time windows
            'one_year_return': float(calculate_yearly_return(self.one_year_data)),
            'three_year_return': float(calculate_yearly_return(self.three_year_data)),
            'five_year_return': float(calculate_yearly_return(self.data)),

            # Mean of daily percentage changes
            'avg_daily_return': float(calculate_average_daily_return(self.one_year_data))
        }

        # Lookup of fundamental financial metrics via yfinance
        fundamentals = self.market_data.get_fundamentals(self.ticker)

        # Combine time-series and fundamentals into a unified dictionary
        return {**analysis, **fundamentals}
