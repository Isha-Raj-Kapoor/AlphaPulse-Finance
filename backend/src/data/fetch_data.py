import yfinance as yf
import os
from utils.config import STOCKS, START_DATE, RAW_PATH

def fetch_stock_data():
    data = yf.download(STOCKS, start=START_DATE)

    if "Adj Close" in data:
        data = data["Adj Close"]
    else:
        data = data["Close"]

    print("Downloaded Data Preview:")
    print(data.head())

    # ✅ Ensure directory exists
    os.makedirs(RAW_PATH, exist_ok=True)

    # ✅ Correct path handling
    file_path = os.path.join(RAW_PATH, "stock_data.csv")

    data.to_csv(file_path)

    return data