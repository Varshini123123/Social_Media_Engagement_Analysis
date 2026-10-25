from pathlib import Path

import pandas as pd

from config import RAW_DATA_DIR, SAMPLE_DATA_FILE


def find_dataset_file():
    raw_dir = Path(RAW_DATA_DIR)
    candidates = sorted(raw_dir.glob("*"))
    csv_or_excel = [path for path in candidates if path.suffix.lower() in {".csv", ".xlsx", ".xls"}]
    if csv_or_excel:
        return csv_or_excel[0]
    if Path(SAMPLE_DATA_FILE).exists():
        return Path(SAMPLE_DATA_FILE)
    raise FileNotFoundError(f"No dataset found in {raw_dir}. Place a CSV or Excel file in data/raw/ or use the sample file.")


def load_dataset(path):
    file_path = Path(path)
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file format: {file_path.suffix}")
