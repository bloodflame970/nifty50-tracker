import pandas as pd
import requests

def test_sudarshan():
    url = "https://raw.githubusercontent.com/sudarshan-ko/nifty-50-data/master/nifty50.csv"
    print(f"Trying: {url}")
    try:
        r = requests.head(url, timeout=5)
        print("Status code:", r.status_code)
        if r.status_code == 200:
            df = pd.read_csv(url)
            print("Columns:", df.columns)
            print("Shape:", df.shape)
            print("Head:")
            print(df.head(2))
            print("Tail:")
            print(df.tail(2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_sudarshan()
