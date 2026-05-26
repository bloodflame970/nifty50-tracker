import pandas as pd

def test_fetch():
    url = "https://raw.githubusercontent.com/abulbasar/data/master/nifty50-index.csv"
    print(f"Fetching Nifty 50 data from {url}...")
    try:
        df = pd.read_csv(url)
        print("Columns:", df.columns)
        print("Head:")
        print(df.head())
        print("Tail:")
        print(df.tail())
        print("Shape:", df.shape)
    except Exception as e:
        print("Error fetching URL:", e)

if __name__ == "__main__":
    test_fetch()
