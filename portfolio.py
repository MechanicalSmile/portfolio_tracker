import pandas as pd
from metrics import (
    calculate_daily_returns,
    calculate_average_daily_return,
    calculate_yearly_return,
    calculate_sharpe_ratio,
    calculate_volatility
)

class Portfolio:
    def __init__(self, price_data):
        """
        Initialize the Portfolio object with historical price data.

        Parameters:
        - price_data (pd.DataFrame): A time-indexed DataFrame.
          - If multiple tickers: columns = MultiIndex (ticker, field), e.g., ('AAPL', 'Close')
          - If single ticker: columns = regular index with fields (e.g., 'Close')
        """
        self.price_data = price_data

        # Subsets of data based on recency for time-windowed analysis
        self.one_year_data = self.price_data[
            self.price_data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365))
        ]

        self.three_year_data = self.price_data[
            self.price_data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365 * 3))
        ]

    def total_value(self, data):
        """
        Aggregate the total portfolio value at each point in time.

        Parameters:
        - data (pd.DataFrame): Subset of price data (1Y, 3Y, or full).

        Returns:
        - pd.Series: Portfolio total value per day (sum of all assets' Close prices).

        Notes:
        - Supports both single-ticker (flat) and multi-ticker (MultiIndex) structures.
        """
        if isinstance(data.columns, pd.MultiIndex):
            # For multi-asset portfolios, extract 'Close' prices and sum across tickers
            total = data.xs('Close', axis=1, level=1).sum(axis=1)
        else:
            # For single asset, just use its 'Close' value
            total = data['Close'].sum(axis=1)
        return total

    def analyze(self):
        """
        Perform full portfolio analysis over multiple timeframes and metrics.

        Returns:
        - dict: A summary of key performance and risk statistics:
            - Average daily return (1Y)
            - Sharpe ratio (1Y)
            - Volatility (1Y)
            - Cumulative returns over 1Y, 3Y, and 5Y windows
        """
        # Compute total portfolio value across each window
        one_year_value = self.total_value(self.one_year_data)
        three_year_value = self.total_value(self.three_year_data)
        five_year_value = self.total_value(self.price_data)

        # Risk and return metrics on daily return stream
        returns = calculate_daily_returns(one_year_value)
        average_daily_return = calculate_average_daily_return(one_year_value)

        # Total return for each time window
        one_year_return = calculate_yearly_return(one_year_value)
        three_year_return = calculate_yearly_return(three_year_value)
        five_year_return = calculate_yearly_return(five_year_value)

        # Risk metrics
        sharpe = calculate_sharpe_ratio(returns)
        vol = calculate_volatility(returns)

        return {
            'sharpe_ratio': sharpe,
            'volatility': vol,
            'average_daily_return': average_daily_return,
            'one_year_return': one_year_return,
            'three_year_return': three_year_return,
            'five_year_return': five_year_return
        }
