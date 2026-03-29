import os
from utils.helpers import save_csv
from utils.config import PROCESSED_PATH


def clean_data(data):
    data = data.dropna()

    # ✅ Ensure folder exists
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # ✅ Proper path handling
    file_path = os.path.join(PROCESSED_PATH, "clean_data.csv")

    save_csv(data, file_path)

    return data