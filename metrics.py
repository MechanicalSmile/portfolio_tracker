import numpy as np
import pandas as pd

def calculate_daily_returns(prices):
    return prices.pct_change().dropna()

def calculate_yearly_return(prices):
    # Get price at the beginning and at the end of the year
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    return ((end_price - start_price) / start_price) * 100

def calculate_average_daily_return(prices):
    daily_returns = prices.pct_change().dropna()
    return daily_returns.mean() * 100  # Return in percentage

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    excess_return = returns - risk_free_rate / 252
    return np.sqrt(252) * (excess_return.mean() / excess_return.std())

def calculate_volatility(returns):
    return returns.std() * np.sqrt(252)

def calculate_max_drawdown(prices):
    cumulative = (1 + prices.pct_change().fillna(0)).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    excess_return = returns - risk_free_rate / 252
    downside = excess_return[excess_return < 0]
    downside_std = downside.std()
    if downside_std == 0:
        return np.nan
    return np.sqrt(252) * excess_return.mean() / downside_std
