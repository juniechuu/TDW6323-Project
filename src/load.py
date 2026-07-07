import pandas as pd
from pathlib import Path

# (parquet = a compressed, typed binary format — faster and more reliable than CSV for the pipeline to read; the CSVs are kept separately just for human/Excel viewing per the submission rubric).
DATA_DIR = Path(__file__).parent.parent / "data" / "parquet"


def load_hh_income() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "hh_income.parquet")
    # Converts the date column to a proper datetime type
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_hies_state() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "hies_state.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_cpi() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "cpi_2d_state.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df
