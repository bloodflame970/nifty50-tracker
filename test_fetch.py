import yfinance as yf
import pandas as pd

def test_fetch():
    print("Fetching Nifty 50 (^NSEI) historical data...")
    ticker = "^NSEI"
    
    # Fetch max history for daily
    print("Daily data:")
    df_daily = yf.download(ticker, period="max", interval="1d")
    print(df_daily.head(5))
    print("Daily date range:", df_daily.index[0], "to", df_daily.index[-1])
    print("Daily shape:", df_daily.shape)
    
    # Fetch weekly data
    print("\nWeekly data:")
    df_weekly = yf.download(ticker, period="max", interval="1wk")
    print(df_weekly.head(5))
    print("Weekly date range:", df_weekly.index[0], "to", df_weekly.index[-1])
    print("Weekly shape:", df_weekly.shape)
    
    # Fetch monthly data
    print("\nMonthly data:")
    df_monthly = yf.download(ticker, period="max", interval="1mo")
    print(df_monthly.head(5))
    print("Monthly date range:", df_monthly.index[0], "to", df_monthly.index[-1])
    print("Monthly shape:", df_monthly.shape)

if __name__ == "__main__":
    test_fetch()
