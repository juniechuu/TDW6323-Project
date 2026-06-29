import pandas as pd

DIVISION_LABELS = {
    "01": "Food & Non-Alcoholic Beverages",
    "02": "Alcoholic Beverages & Tobacco",
    "03": "Clothing & Footwear",
    "04": "Housing, Water, Electricity & Gas",
    "05": "Furnishings & Household Equipment",
    "06": "Health",
    "07": "Transport",
    "08": "Communication",
    "09": "Recreation & Culture",
    "10": "Education",
    "11": "Restaurants & Hotels",
    "12": "Insurance & Financial Services",
    "13": "Personal Care & Miscellaneous",
    "overall": "Overall CPI",
}


def clean_hh_income(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    # Pre-1976: Peninsular Malaysia only; 1989+: citizens only — flag, do not blend
    df["peninsular_only"] = df["year"] < 1976
    df["citizens_only"] = df["year"] >= 1989
    return df


def clean_hies_state(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    # Key derived metric: what fraction of income goes to expenditure
    df["exp_to_income_ratio"] = df["expenditure_mean"] / df["income_mean"]
    return df


def clean_cpi(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["division_label"] = df["division"].map(DIVISION_LABELS).fillna(df["division"])
    return df
