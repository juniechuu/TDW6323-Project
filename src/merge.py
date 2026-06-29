import pandas as pd


def aggregate_cpi_annual(cpi_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly CPI to annual mean per state × division."""
    return (
        cpi_df.groupby(["state", "year", "division", "division_label"], as_index=False)["index"]
        .mean()
        .rename(columns={"index": "cpi_mean"})
    )


def build_cpi_index(cpi_annual: pd.DataFrame, base_year: int = 2010) -> pd.DataFrame:
    """
    Re-base CPI to a fixed year so divisions/states are comparable.
    Returns overall-only rows with an added `cpi_index` column (base year = 100).
    """
    overall = cpi_annual[cpi_annual["division"] == "overall"].copy()
    base = (
        overall[overall["year"] == base_year][["state", "cpi_mean"]]
        .rename(columns={"cpi_mean": "cpi_base"})
    )
    out = overall.merge(base, on="state", how="left")
    out["cpi_index"] = out["cpi_mean"] / out["cpi_base"] * 100
    return out


def merge_hies_cpi(hies_df: pd.DataFrame, cpi_annual: pd.DataFrame, year: int = 2022) -> pd.DataFrame:
    """
    Cross-sectional merge: HIES 2022 state snapshot × CPI annual means for all divisions.
    Result: 16 states × 14 divisions = 224 rows  (satisfies the >200 row requirement).
    """
    before_hies = len(hies_df)
    cpi_year = cpi_annual[cpi_annual["year"] == year].copy()

    merged = hies_df.merge(cpi_year, on="state", how="inner")

    after = len(merged)
    assert after > 200, (
        f"Merged dataset has only {after} rows — expected >200. "
        f"hies rows={before_hies}, cpi rows for {year}={len(cpi_year)}"
    )
    print(f"Merge complete: {before_hies} HIES rows x {len(cpi_year)} CPI rows -> {after} merged rows")
    return merged
