import pandas as pd
import numpy as np
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAW_DATA_PATH, LOG_RETURNS_PATH, TABLEAU_EXPORT_PATH

def calculate_log_returns():
    """Calculate daily log returns from closing prices."""

    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ File not found: {RAW_DATA_PATH}")
        print("💡 Please run 01_data_collection.py first!")
        return None

    print(f"📂 Loading stock data from: {RAW_DATA_PATH}\n")
    close_prices = pd.read_csv(RAW_DATA_PATH, index_col=0, parse_dates=True)

    log_returns = np.log(close_prices / close_prices.shift(1))
    log_returns.dropna(inplace=True)   

    log_returns.to_csv(LOG_RETURNS_PATH)
    print(f"✅ Log returns saved to: {LOG_RETURNS_PATH}")

    print("\n--- Daily Return Statistics (%) ---")
    stats = (log_returns * 100).describe().round(4)
    print(stats)

    print("\n--- Best Single Day Returns ---")
    print((log_returns * 100).max().sort_values(ascending=False).round(2))

    print("\n--- Worst Single Day Returns ---")
    print(((log_returns * 100).min().sort_values()).round(2))

    close_prices_reset = close_prices.copy()
    close_prices_reset.index.name = 'Date'

    prices_long = close_prices.reset_index().melt(id_vars='Date', var_name='Stock', value_name='Close_Price')
    returns_long = log_returns.reset_index().melt(id_vars='Date', var_name='Stock', value_name='Log_Return')

    tableau_df = pd.merge(prices_long, returns_long, on=['Date', 'Stock'])
    tableau_df['Daily_Return_Pct'] = tableau_df['Log_Return'] * 100
    tableau_df.to_csv(TABLEAU_EXPORT_PATH, index=False)
    print(f"\n✅ Tableau export saved to: {TABLEAU_EXPORT_PATH}")

    return log_returns

if __name__ == "__main__":
    returns = calculate_log_returns()
    if returns is not None:
        print("\n✅ Week 2 Step 1 COMPLETE! Now run: 03_monte_carlo.py")
