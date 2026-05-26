import requests
import json
import pandas as pd
import sys

def search_github():
    print("Searching GitHub for Nifty repositories...", flush=True)
    url = "https://api.github.com/search/repositories?q=nifty50+index"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        print(f"Status Code: {r.status_code}", flush=True)
        if r.status_code == 200:
            repos = r.json().get("items", [])
            print(f"Found {len(repos)} repositories.", flush=True)
            for repo in repos[:15]:
                name = repo["full_name"]
                branch = repo["default_branch"]
                print(f"Repo: {name} (branch: {branch})", flush=True)
                
                # Check typical paths
                paths = [
                    "nifty50.csv", "NIFTY50.csv", "Nifty50.csv", 
                    "nifty_50.csv", "Nifty_50.csv",
                    "nifty50_index.csv", "NIFTY50_index.csv",
                    "data/nifty50.csv", "data/NIFTY50.csv",
                    "data/Nifty50.csv", "data/nifty50_index.csv"
                ]
                for p in paths:
                    raw_url = f"https://raw.githubusercontent.com/{name}/{branch}/{p}"
                    try:
                        resp = requests.head(raw_url, timeout=3)
                        if resp.status_code == 200:
                            print(f"  FOUND FILE: {raw_url}", flush=True)
                            df = pd.read_csv(raw_url)
                            print(f"    Columns: {list(df.columns)}", flush=True)
                            print(f"    Shape: {df.shape}", flush=True)
                            # look for a column that represents date
                            date_col = None
                            for col in df.columns:
                                if 'date' in col.lower():
                                    date_col = col
                                    break
                            if date_col:
                                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                                df = df.dropna(subset=[date_col]).sort_values(by=date_col)
                                print(f"    Date range: {df[date_col].min()} to {df[date_col].max()}", flush=True)
                            else:
                                print(f"    First row: {list(df.iloc[0])}", flush=True)
                                print(f"    Last row: {list(df.iloc[-1])}", flush=True)
                            print("-" * 30, flush=True)
                    except Exception as e:
                        pass
        else:
            print(f"Search API failed with status {r.status_code}: {r.text}", flush=True)
    except Exception as e:
        print("Error:", e, flush=True)

if __name__ == "__main__":
    search_github()
