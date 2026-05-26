from nsepy import get_history
from datetime import date
import pandas as pd

def test_nsepy():
    print("Testing nsepy...")
    try:
        data = get_history(symbol="NIFTY 50",
                           start=date(2005, 1, 1),
                           end=date(2005, 1, 10),
                           index=True)
        print("Success!")
        print("Data:")
        print(data)
        print("Shape:", data.shape)
    except Exception as e:
        print("Failed to fetch with nsepy:", e)

if __name__ == "__main__":
    test_nsepy()
