import pandas as pd
import requests

def test_urls():
    candidates = [
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/master/NIFTY50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/main/NIFTY50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/master/Nifty50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/main/Nifty50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/master/data/Nifty50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/main/data/Nifty50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/master/Nifty_50.csv",
        "https://raw.githubusercontent.com/Stock-Market-Network/Nifty-50-Historical-Data/main/Nifty_50.csv",
    ]
    
    for url in candidates:
        print(f"Trying: {url}")
        try:
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print("FOUND!")
                df = pd.read_csv(url)
                print("Columns:", df.columns)
                print("Shape:", df.shape)
                print("Start row:\n", df.iloc[0])
                print("End row:\n", df.iloc[-1])
                print("-" * 50)
            else:
                print(f"Status code: {r.status_code}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    test_urls()
