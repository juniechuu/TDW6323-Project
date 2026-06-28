# CLAUDE.md — TDW6323 Group Project

## Plain-language summary (read this first)

This is a university group project for **TDW6323 Data Wrangling & Visualisation** (MMU), graded out of 40.
The whole task in one sentence: **take real Malaysian government data, clean it, make charts, and say
something useful with it.**

To avoid making ten unrelated charts that add up to nothing, the project answers ONE question:

> **In which Malaysian states is life getting less affordable — where are prices rising faster than
> income — and which spending categories are driving it?**

We chose this question on purpose: answering it forces us to merge two *different* government datasets
(prices + income) and engineer a new metric from them. That combine-and-compute work is exactly what
this course grades hardest, so it scores higher than a simpler one-dataset question.

This file governs the **technical build only**. The written report and presentation slides are
**out of scope for now** — do not generate report prose, cover pages, TOC, or slide content unless asked.

## The domain (Business Understanding — graded 5%)

"Cost of living" in Malaysia = the gap between what households *earn* and what they must *spend* to
maintain a basic standard, and how that gap differs by state. Nominal incomes have risen, but so have
prices, and they don't move together across states or across spending categories.

Decision-makers this informs: DOSM / EPU (welfare policy), state governments (federal allocation
arguments), agencies targeting **B40** assistance and setting the **Poverty Line Income (PLI)**.

Standard vocabulary to anchor in (signals domain literacy): **B40 / M40 / T20** income tiers, **PLI**,
**Gini** (inequality), and the **13 CPI groups** (biggest: food & beverages, housing/utilities, transport).

## Research objectives

**Headline (the thesis the project argues):**
1. **Is cost outrunning income?** Build an affordability index (income relative to CPI) and identify the
   states where real purchasing power is eroding fastest. *This is the headline because the metric exists
   in NO single dataset — it only appears after merging price + income data and engineering a feature.*

**Supporting layers:**
2. **What's driving it?** Across the 13 CPI groups, which categories inflate fastest, and is that uniform
   across states or concentrated? (This is the visual showpiece: 13 groups × 16 states = heatmaps,
   small-multiples, faceted trend lines.)
3. **Where is the squeeze worst right now?** Rank states by expenditure-to-income ratio, poverty, and Gini
   using the latest snapshot.
4. **(bonus, 2%)** Project the near-term CPI trend to flag states heading toward a tighter squeeze.

**Narrative arc:** "Real affordability is eroding fastest in states X, Y, Z" → "here's which spending
categories are driving it" → "so target support here." One thesis, layered evidence, actionable ending.

**Scope:** all 16 Malaysian states; CPI time range from data availability; HIES welfare snapshot (2022).

## What the data can and can't do (respect this — don't fight it)

- **CPI is dense in time** (monthly, by state, by 13 groups) → use it for *trend* and *which-category* questions.
- **HIES income/expenditure/poverty/Gini is sparse** (survey years only; rich 2022 snapshot) → use it for
  *cross-sectional* comparison.
- We therefore **cannot** tell a clean month-by-month affordability story over decades — income doesn't
  update monthly. The honest design: two complementary lenses joined by a bridge metric (the affordability
  index at overlapping years). Handling this mismatch explicitly (annual CPI aggregation; interpolation
  flagged as an assumption; or index anchored to overlapping years only) is itself impressive wrangling.

## Datasets (OpenDOSM — downloaded manually, stored locally)

Source: OpenDOSM (https://open.dosm.gov.my / https://data.gov.my/data-catalogue). Public, no key needed.
Each dataset is downloaded in **both** CSV and Parquet and stored locally — we do NOT read live from the
server (frozen for reproducibility + offline demo).

| Role | Dataset | OpenDOSM page | Notes |
|------|---------|---------------|-------|
| Income | Household income by state, 1970–2022 | https://open.dosm.gov.my/data-catalogue/hh_income | mean & median income |
| Welfare snapshot | HIES state-level 2022 | https://open.dosm.gov.my/data-catalogue/hies_state | expenditure, poverty, Gini |
| Price spine | State CPI, 13 main groups (monthly) | confirm exact `id` on https://data.gov.my/data-catalogue | the time-series engine |

Storage convention (same raw downloads in two formats — keep them in sync, same scope for both):
```
data/
├── csv/         # downloaded CSVs — Excel-openable, matches the "must be CSV" rubric wording
├── parquet/     # downloaded parquets — what the pipeline READS (faster, types preserved)
└── processed/   # final MERGED dataset, exported as CSV — this is the graded submission dataset
```

Download notes:
- Pick **full** scope, not the "latest" preview (we need full history for trends).
- The pipeline reads from `data/parquet/`; the **submitted** dataset is the merged CSV in `data/processed/`.

Confirmed real (sample row from the live API earlier): household expenditure returns fields like
`date`, `state`, `parlimen`, `expenditure` (e.g. Perlis 2022 = RM3584). **Confirm exact column names and
the CPI dataset `id` from the downloaded files before coding — do not assume them.**

Read pattern (local file):
```python
import pandas as pd
df = pd.read_parquet("data/parquet/hh_income.parquet")
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
```

## STEP 0 — confirm the data before building anything

After downloading all three (CSV + Parquet) into `data/`, run this to see real shapes/columns
(replaces all guessing):
```python
# peek.py
import pandas as pd
for name in ["hh_income", "hies_state", "cpi_state"]:   # fix cpi name once confirmed
    df = pd.read_parquet(f"data/parquet/{name}.parquet")
    print(f"\n=== {name} ===")
    print(df.shape)
    print(df.columns.tolist())
    print(df.head())
```
```bash
pip install pandas fastparquet seaborn matplotlib statsmodels streamlit
python peek.py
```
Then lock the real column names into this file before writing the pipeline.

## Data quality issues to handle explicitly (these earn wrangling marks)

- Income 1970 & 1974 = Peninsular Malaysia only; Sabah/Sarawak from 1976.
- From 1989 onward, figures are citizens-only — a methodology break; flag it, don't average across it blindly.
- Income values are **nominal** (not inflation-adjusted) — directly relevant when comparing to CPI.
- DOSM `state` strings are inconsistent (`W.P. Kuala Lumpur` vs `Kuala Lumpur`) — normalise before merging.

## Merge strategy

- Aggregate monthly CPI → **annual mean** per state per year (this is the spine).
- Join income + HIES on `state` (+ `year` where survey years overlap).
- Use **merge, not concat**, with explicit `how=` and a **row-count assertion** before/after.
- Final merged working dataset must have **>200 rows** and **>=2 columns** — export to `data/processed/` as CSV.

## Visualisation plan (important ordering)

Two separate deliverables, in this order:
1. **Notebook charts FIRST** — this is the graded 5% Data Visualisation mark. Static matplotlib/seaborn,
   each chart titled, axis-labelled, and followed by a 1–2 sentence interpretation cell ("what does this reveal?").
   Cover: distributions (hist/box), relationships (scatter/heatmap), CPI trend lines, affordability-gap chart.
2. **Streamlit dashboard SECOND** — this is the 2% innovation bonus + the presentation demo. It reads the
   SAME `data/processed/` CSV (one source of truth). Use Streamlit (not Next.js) because the brief requires
   "all Python files" — a Python app counts as a graded deliverable and demos in one `streamlit run`.

## Tech stack & conventions

- Python 3, **pandas**, **fastparquet** (DOSM parquet), **matplotlib** + **seaborn**.
- Bonus forecast: **statsmodels** (linear trend or simple ARIMA).
- Primary graded deliverable = a **Jupyter notebook** (`.ipynb`).
- Shared loaders/cleaners live in `src/`, imported into the notebook. Pure, reusable functions.
- Fixed random seed anywhere randomness appears.

## Anti-hallucination rules (critical)

- **Never invent a statistic, column name, ringgit figure, or dataset URL.** If unsure a field/dataset
  exists, stop and confirm against the live catalogue — do not guess a parquet path.
- Every number in any output must trace to a `df` we actually loaded. No remembered "≈RMx".
- If a URL 404s or a column is missing, surface the error; never silently fabricate a fallback.

## Suggested file layout

```
.
├── CLAUDE.md
├── requirements.txt
├── peek.py                   # Step 0 schema check
├── notebooks/
│   └── analysis.ipynb        # the graded end-to-end narrative
├── src/
│   ├── load.py               # DOSM parquet loaders
│   ├── clean.py              # cleaning + state normalisation
│   └── merge.py              # the multi-dataset merge
├── app/
│   └── dashboard.py          # Streamlit app (bonus + demo)
├── data/
│   ├── csv/                  # downloaded CSVs (Excel-openable, submission-friendly)
│   ├── parquet/              # downloaded parquets (what the pipeline reads)
│   └── processed/            # final merged CSV (>200 rows) — the submission dataset
└── figures/                  # exported PNGs
```

## Phased plan & checklist

Status: **nothing started yet.** Deadline **29 Jun 2026, 10:00 AM** (~8 days). Group of up to 4 — split
work where marked `[parallel]`. Tick boxes as you go. Phases 0–6 are the technical build (this file's
focus); 7–9 are documented later but listed so the whole project is trackable.

### Phase 0 — Setup & data confirmation  *(Day 1 · graded: enables Business Understanding 5%)*
- [ ] Create repo with the file layout above; commit the raw `data/csv/` + `data/parquet/` files (small, keeps it reproducible)
- [ ] `pip install pandas fastparquet seaborn matplotlib statsmodels streamlit requests`
- [ ] Run `peek.py` on `hh_income`, `hies_state`, and the CPI dataset
- [ ] Confirm the exact CPI dataset `id` on https://data.gov.my/data-catalogue
- [ ] Write the **real** column names back into the Datasets table in this file (kill all placeholders)
- [ ] Write the Business Understanding notes: problem, dataset justification, scope (objectives are already drafted above)

### Phase 1 — Data wrangling  *(Day 2–3 · graded 5%)* `[parallel: one dataset per person]`
- [ ] `src/load.py`: loaders that read all three from `data/parquet/`
- [ ] Print shape, dtypes, null counts, summary stats for each
- [ ] `src/clean.py`: parse dates, normalise `state` strings, handle missing/invalid/duplicate rows
- [ ] Handle the methodology breaks: pre-1976 Peninsular-only, 1989 citizens-only (flag, don't blend)
- [ ] Document **every** cleaning step in a markdown cell (required for marks)

### Phase 2 — Merge  *(Day 3 · part of wrangling mark)*
- [ ] Aggregate monthly CPI → annual mean per state per year
- [ ] `src/merge.py`: join income + HIES + CPI on `state` (+ `year`), explicit `how=`
- [ ] Assert final row count **> 200**; print before/after shapes
- [ ] Export merged CSV to `data/processed/` (this is the submission dataset)

### Phase 3 — Exploratory Data Analysis  *(Day 4 · graded 5%)*
- [ ] Summary stats for numeric + categorical variables (mean, median, std, mode)
- [ ] Income-vs-CPI **correlation** analysis
- [ ] Engineer the **affordability index** (income relative to CPI) — the headline metric
- [ ] Identify squeezed states, trends, anomalies; write what each finding means for Malaysia

### Phase 4 — Notebook visualisation  *(Day 5 · graded 5%)* `[parallel: split chart types]`
- [ ] Distributions: histogram / box plot of a numeric variable
- [ ] Relationships: scatter + correlation heatmap
- [ ] CPI trend lines over time (per state / per category)
- [ ] Category showpiece: 13-group heatmap or small-multiples
- [ ] Affordability-gap chart (the headline visual)
- [ ] Every chart: title, axis labels, legend, **+ a 1–2 sentence interpretation cell**

### Phase 5 — Business insights & recommendations  *(Day 5–6 · graded 5%)*
- [ ] Translate findings into the thesis: which states' real affordability is eroding fastest
- [ ] Actionable recommendations (e.g. target B40 support / watch which price categories where)
- [ ] State the limitations (sparse income data, nominal values, survey gaps, assumptions made)
- [ ] Suggest further investigations

### Phase 6 — Advanced analysis / innovation  *(Day 6 · graded 2% bonus)*
- [ ] CPI forecast with statsmodels (linear trend or simple ARIMA)
- [ ] `app/dashboard.py`: Streamlit dashboard reading the SAME processed CSV (state filter, trend, index)
- [ ] Confirm `streamlit run app/dashboard.py` launches clean

--- technical build ends here · everything below is the later documentation pass ---

### Phase 7 — Report (PDF)  *(Day 7 · graded 5%)* — NOT started yet
- [ ] Cover page (subject code+name, group name, IDs+names), TOC, intro, all C-sections, conclusion
- [ ] APA in-text citations + reference list
- [ ] Export to PDF

### Phase 8 — Presentation  *(Day 8 · graded 8%)* `[parallel: everyone presents a part]`
- [ ] Slides covering dataset → wrangling → analysis → viz → insights
- [ ] Assign sections per member; rehearse to **10 minutes**; prep Q&A

### Phase 9 — Package & submit  *(before 29 Jun 10:00 AM)*
- [ ] Completed Group Project Declaration Form
- [ ] One zip: declaration form + report (PDF) + all `.py`/`.ipynb` files + slides
- [ ] Open the zip on a clean machine to confirm it's not corrupt (no resubmission allowed)
- [ ] Upload to eBwise **before** the deadline (−5%/day late)

## Definition of done (technical only)

- Notebook runs top-to-bottom, clean environment, no errors.
- Merged CSV with >200 rows in `data/processed/`.
- Every figure labelled with an interpretation cell.
- Streamlit app launches and reads the processed CSV.
- No fabricated numbers; everything traces to loaded data.

## NOT in scope yet

- Report writing, cover page, table of contents, APA references.
- Slide deck content.
- Any prose written as if for submission. (Documentation handled in a later pass.)