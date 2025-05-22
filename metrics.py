import numpy as np
import pandas as pd

def calculate_daily_returns(prices):
    """
    Compute daily percentage returns from price series.

    Parameters:
    - prices (pd.Series or pd.DataFrame): Time-indexed price data.

    Returns:
    - Daily return series or DataFrame (% change, excluding NaNs).
    """
    return prices.pct_change().dropna()

def calculate_yearly_return(prices):
    """
    Compute total return over a 1-year period based on price appreciation.

    Parameters:
    - prices (pd.Series): Daily or periodic prices for ~1 year.

    Returns:
    - Total return over the period in percentage.
    """
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    return ((end_price - start_price) / start_price) * 100

def calculate_average_daily_return(prices):
    """
    Calculate mean daily return (arithmetic), annualized by scalar.

    Parameters:
    - prices (pd.Series): Time series of prices.

    Returns:
    - Average daily return (in percentage).
    """
    daily_returns = prices.pct_change().dropna()
    return daily_returns.mean() * 100

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """
    Compute the Sharpe Ratio: excess return per unit of total risk.

    Parameters:
    - returns (pd.Series): Daily return series.
    - risk_free_rate (float): Annualized risk-free rate (e.g., 0.01 = 1%).

    Returns:
    - Sharpe Ratio (float): Annualized.
    
    Notes:
    - Assumes 252 trading days per year.
    - Uses standard deviation of total returns (not downside risk).
    """
    excess_return = returns - risk_free_rate / 252  # Daily excess return
    return np.sqrt(252) * (excess_return.mean() / excess_return.std())

def calculate_volatility(returns):
    """
    Calculate annualized volatility (standard deviation of returns).

    Parameters:
    - returns (pd.Series): Daily return series.

    Returns:
    - Annualized volatility (float).
    """
    return returns.std() * np.sqrt(252)

def calculate_max_drawdown(prices):
    """
    Calculate the maximum drawdown: the worst peak-to-trough drop.

    Parameters:
    - prices (pd.Series): Time series of prices.

    Returns:
    - Max drawdown (float): Negative decimal (e.g., -0.35 for -35%).

    Method:
    - Computes cumulative returns.
    - Tracks peak values.
    - Measures largest relative decline from peak.
    """
    cumulative = (1 + prices.pct_change().fillna(0)).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    """
    Calculate the Sortino Ratio: excess return per unit of downside risk.

    Parameters:
    - returns (pd.Series): Daily return series.
    - risk_free_rate (float): Annualized risk-free rate.

    Returns:
    - Sortino Ratio (float): Annualized.

    Notes:
    - Only considers downside deviation (returns < 0).
    - More appropriate than Sharpe for skewed distributions.
    """
    excess_return = returns - risk_free_rate / 252
    downside = excess_return[excess_return < 0]
    downside_std = downside.std()
    
    # Avoid division by zero
    if downside_std == 0:
        return np.nan

    return np.sqrt(252) * excess_return.mean() / downside_std
