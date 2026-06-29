# TDW6323 — Malaysian Cost of Living Analysis

**Subject:** TDW 6323 Data Wrangling and Visualisation  
**Research question:** In which Malaysian states is life getting less affordable, and which spending categories are driving it?

---

## Project Structure

```
.
├── notebooks/
│   └── analysis.ipynb          ← Main graded notebook (run this)
├── src/
│   ├── load.py                 ← Dataset loaders
│   ├── clean.py                ← Cleaning + feature engineering
│   └── merge.py                ← Aggregation + merge logic
├── app/
│   └── dashboard.py            ← Streamlit interactive dashboard
├── data/
│   ├── csv/                    ← Raw CSVs (Excel-openable, submission copy)
│   ├── parquet/                ← Raw parquets (what the pipeline reads)
│   └── processed/
│       └── merged_affordability_2022.csv   ← Final merged dataset (>200 rows)
├── figures/                    ← Exported chart PNGs (fig1–fig6)
├── requirements.txt
└── extras/                     ← Drafts and dev files (not part of submission)
```

---

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas fastparquet seaborn matplotlib statsmodels streamlit jupyter
```

**2. Verify data files are present**

The following files must exist before running the notebook:

```
data/parquet/hh_income.parquet
data/parquet/hies_state.parquet
data/parquet/cpi_2d_state.parquet
```

These are the raw downloads from OpenDOSM. They are included in the submission.

---

## Running the Notebook

```bash
jupyter notebook
```

Then open `notebooks/analysis.ipynb` and run all cells top to bottom (**Kernel > Restart & Run All**).

The notebook will:
- Load and clean all three datasets
- Merge HIES 2022 × CPI 2022 into `data/processed/merged_affordability_2022.csv`
- Generate and save all 6 figures to `figures/`
- Print the affordability index, correlation matrix, and key findings

---

## Running the Streamlit Dashboard

```bash
python -m streamlit run app/dashboard.py
```

The dashboard reads from `data/processed/merged_affordability_2022.csv` — make sure the notebook has been run at least once first so that file exists.

It will open automatically in your browser at `http://localhost:8501`.

---

## Things to Note

**Data paths are relative**  
The notebook uses `../data/` and `../figures/` relative to the `notebooks/` folder. Run the notebook from inside Jupyter (not as a script) or the paths will break.

**Run the notebook before the dashboard**  
The Streamlit app reads the processed CSV. If you haven't run the notebook yet, the file won't exist and the dashboard will error.

**Python version**  
Tested on Python 3.11+. The `fastparquet` engine is required to read the `.parquet` files — `pyarrow` will not work as a drop-in because the DOSM parquet files use a specific encoding.

**hh_income has no state column**  
The national household income dataset (`hh_income.parquet`) is a national aggregate only — it has no state breakdown. It is loaded and used for context but is not part of the state-level merge. This is expected, not a bug.

**CPI base year is 2010**  
All CPI index values are relative to 2010 = 100. A value of 130 means prices are 30% higher than 2010, not that absolute prices are 130.

**Merged dataset is cross-sectional, not a time series**  
The final `merged_affordability_2022.csv` is anchored to 2022 because HIES income data is only available for that snapshot year. The affordability index is a point-in-time comparison, not a trend.

---

## Data Sources

All data downloaded from [OpenDOSM](https://open.dosm.gov.my) — public, no login required.

| Dataset | ID | Description |
|---|---|---|
| State CPI by Division | `cpi_2d_state` | Monthly CPI, 16 states × 13 divisions, Jan 2010–May 2026 |
| HIES State 2022 | `hies_state` | Household income, expenditure, Gini, poverty by state (2022) |
| National Household Income | `hh_income` | National mean/median income, 1970–2022 |
