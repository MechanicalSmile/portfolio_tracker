from data_loader import DataLoader
from market_data import MarketData
from portfolio import Portfolio
from asset import Asset

def main():
    loader = DataLoader('data/portfolio.xlsx')
    tickers = loader.load_tickers()

    market = MarketData(tickers)
    data = market.fetch_data()

    print("Analyzing Portfolio...")
    portfolio = Portfolio(data)
    portfolio_result = portfolio.analyze()
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

    print("\nAnalyzing Individual Assets...")
    for ticker in tickers:
        asset = Asset(ticker, data)
        result = asset.analyze()
        fcf = result.get("free_cash_flow")
        if fcf is not None:
            fcf_formatted = f"${fcf:,.0f}"  # Format with commas, no decimals
        else:
            fcf_formatted = "N/A"  # Use "N/A" if no value is found
            
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
            f"\n\tMDD = {result['max_drawdown']*100:.2f}%"
            
            f"\n\nFundamentals:"
            f"\n\tP/E = {result['pe_ratio']}, "
            f"\n\tP/B = {result['pb_ratio']}, "
            f"\n\tBeta = {result['beta']},"
            f"\n\tDividend = {result['dividend_yield']:.2f}% | ${result['dividend_rate']}, "
            f"\n\tRev Growth = {result['revenue_growth']}, "
            f"\n\tEPS Growth = {result['earnings_growth']},"
            f"\n\tROE = {result['roe']}, "
            f"\n\tFCF = {fcf_formatted}\n"
        )



if __name__ == "__main__":
    main()