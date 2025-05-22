# Import custom modules for data handling, market data retrieval, portfolio analysis, and individual asset analysis
from data_loader import DataLoader
from market_data import MarketData
from portfolio import Portfolio
from asset import Asset

def main():
    # Step 1: Load tickers from an Excel file using the custom DataLoader class
    loader = DataLoader('data/portfolio.xlsx')
    tickers = loader.load_tickers()  # Returns a list of stock tickers (e.g., ['AAPL', 'MSFT'])

    # Step 2: Fetch historical market data for the tickers
    market = MarketData(tickers)     # Initialize market data interface
    data = market.fetch_data()       # Pull historical price and possibly fundamental data

    # Step 3: Analyze the entire portfolio based on aggregated market data
    print("Analyzing Portfolio...")
    portfolio = Portfolio(data)            # Create Portfolio instance with full dataset
    portfolio_result = portfolio.analyze() # Compute risk/return metrics over different periods

    # Step 4: Display portfolio-level analysis results
    print(
        f"Portfolio Analysis (1-Year Risk Metrics):"
        f"\n\tAverage Daily Return = {portfolio_result['average_daily_return']:.2f}%"
        f"\n\tSharpe Ratio = {portfolio_result['sharpe_ratio']:.2f}"
        f"\n\tVolatility = {portfolio_result['volatility'] * 100:.2f}%"

        f"\n\nPortfolio Performance:"
        f"\n\tOne Year Return = {portfolio_result['one_year_return']:.2f}%"
        f"\n\tThree Year Return = {portfolio_result['three_year_return']:.2f}%"
        f"\n\tFive Year Return = {portfolio_result['five_year_return']:.2f}%"
    )

    # Step 5: Analyze each individual asset in the portfolio
    print("\nAnalyzing Individual Assets...")
    for ticker in tickers:
        asset = Asset(ticker, data)   # Create Asset instance for each ticker
        result = asset.analyze()      # Perform financial and risk analysis

        # Format free cash flow nicely or show "N/A" if not available
        fcf = result.get("free_cash_flow")
        if fcf is not None:
            fcf_formatted = f"${fcf:,.0f}"  # Format with commas and no decimals
        else:
            fcf_formatted = "N/A"
        
        # Extract dividend yield and dividend rate from the result dictionary.
        # These values may be None if the data source (e.g., yfinance) does not provide them.
        div_yield = result['dividend_yield']
        div_rate = result['dividend_rate']

        # Format dividend yield as a percentage string with 2 decimal places,
        # or show 'N/A' if the value is missing (None).
        div_yield_str = f"{div_yield:.2f}%" if div_yield is not None else "N/A"

        # Format dividend rate as a dollar string with 2 decimal places,
        # or show 'N/A' if the value is missing (None).
        div_rate_str = f"${div_rate:.2f}" if div_rate is not None else "N/A"


        # Step 6: Print out detailed metrics per asset, including performance, risk, and fundamentals
        print(
            f"{result['ticker']}: "
            f"\nPortfolio Performance:"
            f"\n\tOne Year Return = {result['one_year_return']:.2f}%"
            f"\n\tThree Year Return = {result['three_year_return']:.2f}%"
            f"\n\tFive Year Return = {result['five_year_return']:.2f}%"

            f"\n\nPortfolio Analysis (1-Year Risk Metrics):"
            f"\n\tAverage Daily Return = {result['avg_daily_return']:.2f}%"
            f"\n\tSharpe = {result['sharpe_ratio']:.2f}, "
            f"\n\tSortino = {result['sortino_ratio']:.2f}, "
            f"\n\tVolatility = {result['volatility']*100:.2f}%, "
            f"\n\tMDD = {result['max_drawdown']*100:.2f}%"  # MDD = Maximum Drawdown

            f"\n\nFundamentals:"
            f"\n\tP/E = {result['pe_ratio']}, "             # Price-to-Earnings ratio
            f"\n\tP/B = {result['pb_ratio']}, "             # Price-to-Book ratio
            f"\n\tBeta = {result['beta']},"                 # Systematic risk measure
            f"\n\tDividend = {div_yield_str} | {div_rate_str}, "  # Yield and actual dividend
            f"\n\tRev Growth = {result['revenue_growth']}, "       # Revenue growth rate
            f"\n\tEPS Growth = {result['earnings_growth']},"       # Earnings per share growth
            f"\n\tROE = {result['roe']}, "                          # Return on Equity
            f"\n\tFCF = {fcf_formatted}\n"                          # Free Cash Flow
        )

# Ensure this script runs only when executed directly (not when imported as a module)
if __name__ == "__main__":
    main()