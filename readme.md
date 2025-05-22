# 📈 Portfolio Tracker

A Python-based financial analysis tool that allows you to evaluate the historical performance and risk profile of a portfolio of assets. It uses market data from **Yahoo Finance** to calculate key portfolio metrics and fundamentals for each asset.

---

## 🔧 Features

- Load asset tickers from an Excel file
- Fetch historical market data (default: 5 years, daily)
- Compute portfolio-level metrics:
  - Sharpe Ratio
  - Volatility
  - Average Daily Return
  - 1Y / 3Y / 5Y Cumulative Returns
- Analyze individual assets with:
  - Performance metrics (returns, drawdown, volatility)
  - Risk ratios (Sharpe, Sortino)
  - Fundamentals (P/E, P/B, Beta, ROE, Dividend Yield/Rate, Revenue/Earnings Growth, FCF)

---

## 📁 Project Structure

```
portfolio_tracker/
├── main.py               # Entry point
├── data/portfolio.xlsx   # Excel file containing tickers in a column named 'Ticker'
├── asset.py              # Asset-level analysis logic
├── portfolio.py          # Portfolio-level aggregation & analysis
├── metrics.py            # Core financial metric calculations
├── market_data.py        # Market data and fundamentals via yfinance
├── data_loader.py        # Load tickers from Excel
└── README.md             # Documentation
```

---

## 🧠 How It Works

1. **Ticker Load**:  
   Loads tickers from `data/portfolio.xlsx`.

2. **Market Data Fetch**:  
   Retrieves historical price data for all tickers using [`yfinance`](https://github.com/ranaroussi/yfinance).

3. **Portfolio Analysis**:  
   Computes aggregate returns, volatility, and Sharpe ratio.

4. **Asset Analysis**:  
   Iterates through each ticker to compute:
   - Time-based returns
   - Risk metrics (Sharpe, Sortino, Max Drawdown)
   - Fundamental ratios (e.g., P/E, P/B, Dividend, FCF)

5. **Formatted Output**:  
   Cleanly prints all results to the console.

---

## 📥 Requirements

Install required packages using pip:

```bash
pip install pandas yfinance openpyxl numpy
```

---

## 📊 Example Input

Your Excel file should look like:

| Ticker |
|--------|
| AAPL   |
| MSFT   |
| TSLA   |

File path: `data/portfolio.xlsx`

---

## ▶️ Running the Program

```bash
python main.py
```

---

## 📌 Notes

- Market data comes from Yahoo Finance and may occasionally contain missing or stale values.
- All returns are calculated using **adjusted close prices** and assume equal weighting across assets.
- Handles `None` values gracefully for missing fundamentals like dividends or free cash flow.

---

## 📘 License

MIT License
