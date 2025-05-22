import pandas as pd

class DataLoader:
    def __init__(self, filepath):
        """
        Initialize the DataLoader with a path to the input Excel file.

        Parameters:
        - filepath (str): Path to the Excel file containing portfolio data.
        """
        self.filepath = filepath

    def load_tickers(self):
        """
        Load ticker symbols from the Excel file.

        Assumes:
        - The Excel file has a column labeled 'Ticker'.
        - Each row contains a valid ticker or NaN.

        Returns:
        - list[str]: Cleaned list of non-null ticker symbols.
        """
        df = pd.read_excel(self.filepath)  # Load spreadsheet into DataFrame
        return df['Ticker'].dropna().tolist()  # Drop empty cells and return as list
