import pandas as pd

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_tickers(self):
        df = pd.read_excel(self.filepath)
        return df['Ticker'].dropna().tolist()
