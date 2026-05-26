import os
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nifty50.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables for daily, weekly, and monthly data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Daily table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nifty_daily (
        date TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
    """)
    
    # Weekly table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nifty_weekly (
        date TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
    """)
    
    # Monthly table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nifty_monthly (
        date TEXT PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

def update_nifty_data():
    """Fetch maximum available data from yfinance and update the SQLite tables."""
    ticker = "^NSEI"
    print(f"Fetching historical Nifty 50 data from yfinance ({ticker})...")
    
    # Initialize DB tables if they don't exist
    init_db()
    
    conn = get_db_connection()
    
    intervals = {
        'daily': ('1d', 'nifty_daily'),
        'weekly': ('1wk', 'nifty_weekly'),
        'monthly': ('1mo', 'nifty_monthly')
    }
    
    success_status = {}
    
    for name, (interval, table_name) in intervals.items():
        try:
            print(f"Downloading {name} data (interval={interval})...")
            df = yf.download(ticker, period="max", interval=interval)
            
            if df.empty:
                print(f"No data returned for {name} interval.")
                success_status[name] = False
                continue
            
            # Reset index to bring Date column in
            df = df.reset_index()
            
            # Standardize column names (yfinance returns MultiIndex or SingleIndex columns depending on version)
            # Flatten columns if MultiIndex
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
                
            # Rename columns to match db schema
            df = df.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Clean data: drop rows with missing date or close prices
            df = df.dropna(subset=['date', 'close'])
            
            # Convert date to string format YYYY-MM-DD
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            # Select relevant columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
            # Write to database (UPSERT style or replace)
            # Since SQLite doesn't have native upsert in simple pandas to_sql,
            # we can insert into a temporary table or insert with OR REPLACE
            cursor = conn.cursor()
            
            # Use OR REPLACE for pandas write
            # A clean way is to delete existing dates to avoid duplicate key violations or use execute_many
            records = df.to_dict('records')
            
            cursor.execute(f"BEGIN TRANSACTION;")
            for r in records:
                cursor.execute(f"""
                INSERT OR REPLACE INTO {table_name} (date, open, high, low, close, volume)
                VALUES (:date, :open, :high, :low, :close, :volume)
                """, r)
            conn.commit()
            
            print(f"Successfully updated {name} data. Record count: {len(records)}")
            success_status[name] = True
            
        except Exception as e:
            print(f"Error updating {name} data: {e}")
            success_status[name] = False
            
    conn.close()
    return success_status

def get_nifty_data(interval='daily', start_date=None, end_date=None, limit=None):
    """Retrieve Nifty 50 data from the database."""
    conn = get_db_connection()
    table_map = {
        'daily': 'nifty_daily',
        'weekly': 'nifty_weekly',
        'monthly': 'nifty_monthly'
    }
    table_name = table_map.get(interval, 'nifty_daily')
    
    query = f"SELECT date, open, high, low, close, volume FROM {table_name} WHERE 1=1"
    params = []
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
        
    query += " ORDER BY date ASC"
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
        
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_summary_metrics():
    """Calculate key performance indicators (KPIs) for Nifty 50."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the latest daily record
    cursor.execute("SELECT * FROM nifty_daily ORDER BY date DESC LIMIT 2")
    rows = cursor.fetchall()
    
    metrics = {
        'current_close': 0.0,
        'change_val': 0.0,
        'change_pct': 0.0,
        'prev_close': 0.0,
        'high_52week': 0.0,
        'low_52week': 0.0,
        'all_time_high': 0.0,
        'all_time_low': 0.0,
        'ytd_return': 0.0,
        'three_year_return': 0.0,
        'five_year_return': 0.0,
        'ten_year_return': 0.0,
        'last_updated': ''
    }
    
    if len(rows) > 0:
        latest = rows[0]
        metrics['current_close'] = latest['close']
        metrics['open'] = latest['open']
        metrics['high'] = latest['high']
        metrics['low'] = latest['low']
        metrics['volume'] = latest['volume']
        metrics['last_updated'] = latest['date']
        
        if len(rows) > 1:
            prev = rows[1]
            metrics['prev_close'] = prev['close']
            metrics['change_val'] = latest['close'] - prev['close']
            metrics['change_pct'] = (metrics['change_val'] / prev['close']) * 100
            
        # 52-week High/Low (approx 252 trading days)
        cursor.execute("""
            SELECT MAX(high) as h52, MIN(low) as l52 
            FROM nifty_daily 
            WHERE date >= date(?, '-1 year')
        """, (latest['date'],))
        row_52 = cursor.fetchone()
        if row_52:
            metrics['high_52week'] = row_52['h52'] if row_52['h52'] else 0.0
            metrics['low_52week'] = row_52['l52'] if row_52['l52'] else 0.0
            
        # All-time High/Low
        cursor.execute("SELECT MAX(high) as ath, MIN(low) as atl FROM nifty_daily")
        row_ath = cursor.fetchone()
        if row_ath:
            metrics['all_time_high'] = row_ath['ath'] if row_ath['ath'] else 0.0
            metrics['all_time_low'] = row_ath['atl'] if row_ath['atl'] else 0.0
            
        # YTD Return (from the start of the latest year)
        latest_year = latest['date'][:4]
        cursor.execute("""
            SELECT close FROM nifty_daily 
            WHERE date >= ? 
            ORDER BY date ASC LIMIT 1
        """, (f"{latest_year}-01-01",))
        ytd_row = cursor.fetchone()
        if ytd_row:
            metrics['ytd_return'] = ((latest['close'] - ytd_row['close']) / ytd_row['close']) * 100
            
        # Long-term returns
        for years, key in [(3, 'three_year_return'), (5, 'five_year_return'), (10, 'ten_year_return')]:
            cursor.execute("""
                SELECT close FROM nifty_daily 
                WHERE date <= date(?, ?) 
                ORDER BY date DESC LIMIT 1
            """, (latest['date'], f"-{years} year"))
            hist_row = cursor.fetchone()
            if hist_row:
                metrics[key] = ((latest['close'] - hist_row['close']) / hist_row['close']) * 100
                
    conn.close()
    return metrics
