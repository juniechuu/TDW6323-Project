import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "parquet"


def load_hh_income() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "hh_income.parquet")
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
