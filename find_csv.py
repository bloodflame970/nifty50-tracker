import pandas as pd
import requests

def test_urls():
    candidates = [
        "https://raw.githubusercontent.com/BennyThadikaran/eod2/master/data/NIFTY50.csv",
        "https://raw.githubusercontent.com/BennyThadikaran/eod2/main/data/NIFTY50.csv",
        "https://raw.githubusercontent.com/kalilurrahman/NIFTY_50_STOCK_DATA/master/NIFTY50.csv",
        "https://raw.githubusercontent.com/kalilurrahman/NIFTY_50_STOCK_DATA/main/NIFTY50.csv",
        "https://raw.githubusercontent.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/main/Nifty_50.csv",
        "https://raw.githubusercontent.com/neha01/Automate-Scrap-Nse-Data/master/Nifty50.csv",
        "https://raw.githubusercontent.com/neha01/Automate-Scrap-Nse-Data/main/Nifty50.csv",
        "https://raw.githubusercontent.com/shreyasbapat/nifty50-data/master/data/nifty50.csv",
        "https://raw.githubusercontent.com/shreyasbapat/nifty50-data/main/data/nifty50.csv",
        "https://raw.githubusercontent.com/anirban-m/nifty50-historical-data/master/nifty50.csv",
        "https://raw.githubusercontent.com/anirban-m/nifty50-historical-data/main/nifty50.csv",
        "https://raw.githubusercontent.com/Sdaas/nifty-analysis/master/Nifty50.csv",
        "https://raw.githubusercontent.com/Sdaas/nifty-analysis/main/Nifty50.csv",
    ]
    
    for url in candidates:
        print(f"Trying: {url}")
        try:
            # check headers first
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print("FOUND! Downloading and checking...")
                df = pd.read_csv(url)
                print("Columns:", df.columns)
                print("Shape:", df.shape)
                # print first few dates and last few dates
                # print row 0 and last row
                print("Start row:")
                print(df.iloc[0])
                print("End row:")
                print(df.iloc[-1])
                print("-" * 50)
            else:
                print(f"Status code: {r.status_code}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    test_urls()
