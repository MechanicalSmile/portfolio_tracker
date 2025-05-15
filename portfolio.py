import pandas as pd
from metrics import calculate_daily_returns, calculate_average_daily_return, calculate_yearly_return, calculate_sharpe_ratio, calculate_volatility

class Portfolio:
    def __init__(self, price_data):
        self.price_data = price_data
        self.one_year_data = self.price_data[self.price_data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365))]
        self.three_year_data = self.price_data[self.price_data.index >= (pd.Timestamp.today() - pd.Timedelta(days=365*3))]

    def total_value(self, data):
        if isinstance(data.columns, pd.MultiIndex):
            total = data.xs('Close', axis=1, level=1).sum(axis=1)
        else:
            total = data['Close'].sum(axis=1)
        return total

    def analyze(self):
        one_year_value = self.total_value(self.one_year_data)
        
        three_year_value = self.total_value(self.three_year_data)
        
        five_year_value = self.total_value(self.price_data)
        
        returns = calculate_daily_returns(one_year_value)
        average_daily_return = calculate_average_daily_return(one_year_value)
        one_year_return = calculate_yearly_return(one_year_value)
        three_year_return = calculate_yearly_return(three_year_value)
        five_year_return = calculate_yearly_return(five_year_value)
        
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
