TDW6323 - Malaysian Cost of Living Analysis


How to Run

1. Install dependencies
   pip install -r requirements.txt

2. Open and run the notebook
   jupyter notebook
   Then open notebooks/analysis.ipynb and select Kernel > Restart & Run All.

3. Launch the dashboard (optional)
   python -m streamlit run app/dashboard.py
   Note: Run the notebook first before launching the dashboard, otherwise the dashboard will not find the processed data file.


Other Files

notebooks/analysis.ipynb   - Main analysis notebook. This is the primary graded deliverable.
src/load.py                 - Functions to load the raw datasets from data/parquet/
src/clean.py                - Data cleaning and feature engineering logic
src/merge.py                - Aggregation and merge logic
app/dashboard.py            - Interactive Streamlit dashboard
data/csv/                   - Raw downloaded CSVs from OpenDOSM (Excel-openable)
data/parquet/               - Raw downloaded parquets (what the notebook reads)
data/processed/             - Final merged dataset exported by the notebook (merged_affordability_2022.csv)
figures/                    - Chart images exported by the notebook (fig1 to fig6)
extras/                     - Draft files and dev notes, not part of the submission
