import yfinance as yf
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STOCKS, START_DATE, END_DATE, RAW_DATA_PATH

def create_folders():
    """Create all necessary folders if they don't exist."""
    folders = [
        'data/raw',
        'data/processed',
        'data/exports',
        'outputs/charts',
        'outputs/reports'
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ All folders created successfully.")

def download_stock_data():
    """Download historical stock data using yfinance."""
    print(f"\n📥 Downloading data for: {STOCKS}")
    print(f"📅 Date range: {START_DATE} → {END_DATE}\n")

    try:
        raw_data = yf.download(STOCKS, start=START_DATE, end=END_DATE, auto_adjust=True)

        close_prices = raw_data['Close']

        close_prices.dropna(how='all', inplace=True)

        close_prices.ffill(inplace=True)

        close_prices.to_csv(RAW_DATA_PATH)
        print(f"✅ Stock data saved to: {RAW_DATA_PATH}")
        print(f"📊 Shape: {close_prices.shape[0]} days × {close_prices.shape[1]} stocks\n")

        print("--- Preview (first 5 rows) ---")
        print(close_prices.head())
        print("\n--- Latest Prices ---")
        print(close_prices.tail(1).T.rename(columns={close_prices.index[-1]: 'Latest Price ($)'}))

        return close_prices

    except Exception as e:
        print(f"❌ Error downloading data: {e}")
        print("💡 Tip: Check your internet connection or try again later.")
        return None

if __name__ == "__main__":
    create_folders()
    data = download_stock_data()
    if data is not None:
        print("\n✅ Week 1 Step 1 COMPLETE! Now run: 02_returns_calculation.py")
