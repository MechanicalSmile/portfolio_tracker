from metrics import (
    calculate_daily_returns, calculate_average_daily_return, calculate_yearly_return,
    calculate_sharpe_ratio, calculate_sortino_ratio,
    calculate_volatility, calculate_max_drawdown,
)
from market_data import MarketData
import pandas as pd

class Asset:
    def __init__(self, ticker, price_data):
        self.ticker = ticker
        if isinstance(price_data.columns, pd.MultiIndex):
            self.data = price_data[ticker]['Close']
            self.one_year_data = self.data[self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365))]
            self.three_year_data = self.data[self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365*3))]
        else:
            self.data = price_data['Close']
            self.one_year_data = self.data[self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365))]
            self.three_year_data = self.data[self.data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365*3))]
        self.market_data = MarketData([ticker])  # Use a single-ticker instance

    def analyze(self):
        returns = calculate_daily_returns(self.one_year_data)
        analysis = {
            'ticker': self.ticker,
            'sharpe_ratio': float(calculate_sharpe_ratio(returns)),
            'sortino_ratio': float(calculate_sortino_ratio(returns)),
            'volatility': float(calculate_volatility(returns)),
            'max_drawdown': float(calculate_max_drawdown(self.one_year_data)),
            'one_year_return': float(calculate_yearly_return(self.one_year_data)),
            'three_year_return': float(calculate_yearly_return(self.three_year_data)),
            'five_year_return': float(calculate_yearly_return(self.data)),
            'avg_daily_return': float(calculate_average_daily_return(self.one_year_data))
        }

        fundamentals = self.market_data.get_fundamentals(self.ticker)
        return {**analysis, **fundamentals}
