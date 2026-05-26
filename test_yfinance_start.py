import yfinance as yf

def test_yfinance_start():
    print("Testing yfinance with explicit start date...")
    try:
        data = yf.download("^NSEI", start="1995-11-03", end="2026-05-25")
        print("Success!")
        print("Data columns:", data.columns)
        print("Data shape:", data.shape)
        if not data.empty:
            print("First date:", data.index[0])
            print("Last date:", data.index[-1])
            print("First row:\n", data.iloc[0])
    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    test_yfinance_start()
