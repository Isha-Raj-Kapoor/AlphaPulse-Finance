import logging
import os
import pandas as pd

from data.fetch_data import fetch_stock_data
from data.clean_data import clean_data
from analysis.returns import calculate_returns
from analysis.correlation import calculate_correlation
from analysis.monte_carlo import monte_carlo_simulation
from utils.config import PROCESSED_PATH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

raw = fetch_stock_data()
clean = clean_data(raw)
returns = calculate_returns(clean)

returns.to_csv(os.path.join(PROCESSED_PATH, "returns.csv"))

corr = calculate_correlation(returns)
corr.to_csv(os.path.join(PROCESSED_PATH, "correlation.csv"))

mc = monte_carlo_simulation(returns)
pd.DataFrame(mc, columns=["Return", "Risk"]).to_csv(
    os.path.join(PROCESSED_PATH, "monte_carlo.csv"),
    index=False
)

logging.info("Pipeline completed successfully")
print("✅ Done")