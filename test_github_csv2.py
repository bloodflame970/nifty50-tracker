

import pandas as pd

def test_fetch():
    urls = [
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/main/Nifty_50.csv",
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/main/Nifty%2050.csv",
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/main/NIFTY50.csv",
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/master/Nifty_50.csv",
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/master/NIFTY50.csv",
    ]
    for url in urls:
        print(f"Trying {url}...")
        try:
            df = pd.read_csv(url)
            print("SUCCESS!")
            print("Columns:", df.columns)
            print("Head:")
            print(df.head(2))
            print("Tail:")
            print(df.tail(2))
            print("Shape:", df.shape)
            break
        except Exception as e:
            print("Failed:", e)

if __name__ == "__main__":
    test_fetch()
