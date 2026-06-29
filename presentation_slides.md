# TDW 6323 — Presentation Slide Points
# Malaysian Cost of Living Analysis
# 10 minutes total — suggested timing included

---

## SLIDE 1 — COVER SLIDE
**(30 seconds)**

**Title:** Malaysian Cost of Living Analysis
**Subtitle:** Which States Are Getting Less Affordable — and Why?

- Subject: TDW 6323 Data Wrangling and Visualisation
- Group Name: [YOUR GROUP NAME]
- Members: [List all names and IDs]
- Date: June 2026

---

## SLIDE 2 — THE PROBLEM
**(45 seconds)**

**Title:** Why Does This Matter?

- Prices in Malaysia go up every year
- But salaries do not always keep up
- When prices rise faster than income — life gets harder even if you earn more
- This affects the **B40 group the most** — the bottom 40% of Malaysian households
- Government agencies like DOSM and EPU need to know **which states** to target for support

**Say this out loud:**
"Our project answers one question — in which Malaysian states is life getting less affordable, and which spending categories are driving it?"

---

## SLIDE 3 — THE DATASETS
**(1 minute)**

**Title:** Where Did Our Data Come From?

All data from **OpenDOSM** — the official open data platform by the Department of Statistics Malaysia. Free, public, no login needed.

| Dataset | What It Contains | Size |
|---|---|---|
| cpi_2d_state | Monthly CPI by state and 13 categories, 2010–2026 | 44,128 rows |
| hies_state | Income, expenditure, poverty, Gini by state (2022) | 16 rows |
| hh_income | National household income 1970–2022 | 21 rows |

**Key point to say:**
"No single dataset could answer our question. We had to combine the price data and the income data together — that is what data wrangling is all about."

---

## SLIDE 4 — DATA WRANGLING
**(1 minute 30 seconds)**

**Title:** How We Cleaned and Prepared the Data

**Step 1 — Loaded** all 3 datasets from Parquet files using Python and pandas

**Step 2 — Cleaned:**
- Flagged methodology breaks in income data (pre-1976 = Peninsular only, 1989+ = citizens only)
- Added new column: **Expenditure-to-Income Ratio** (expenditure ÷ income)
- Added human-readable category labels to CPI division codes

**Step 3 — Aggregated:**
- CPI was monthly — income data is yearly
- Averaged 12 monthly CPI readings into 1 annual figure per state per category

**Step 4 — Merged:**
- Joined HIES 2022 income data × 2022 annual CPI data using **state name** as the key
- Result: **224 rows, 13 columns** — satisfies the >200 row requirement

> Think of the merge like a VLOOKUP in Excel — match each state's income to that state's price level

---

## SLIDE 5 — THE AFFORDABILITY INDEX
**(1 minute)**

**Title:** Our Key Innovation — The Affordability Index

This number does not exist in any dataset. We created it.

```
Affordability Index = (State Income ÷ State CPI) ÷ National Average × 100
```

| Score | Meaning |
|---|---|
| Above 100 | More affordable than national average ✅ |
| Exactly 100 | At the national average |
| Below 100 | Less affordable — income not keeping up with prices ❌ |

**Why this matters:**
- A state can have HIGH income but still be unaffordable if prices are even higher
- A state can have LOW income but still be okay if prices are also very low
- The index captures BOTH at once

---

## SLIDE 6 — KEY FINDING 1 (show Chart 7 — Affordability Index bars)
**(1 minute)**

**Title:** Which States Are Most Squeezed?

**[Insert fig5_affordability_gap.png here]**

- Red bars = below national average = more financially squeezed
- Blue bars = above national average = more comfortable

**Most squeezed states:**
- Kelantan
- Kedah
- Perlis
- Sabah
- Terengganu

**Most comfortable states:**
- W.P. Putrajaya
- W.P. Kuala Lumpur
- Selangor

**Say this:**
"The reason these red states are struggling is not because prices are higher there — it is because incomes are significantly lower while prices have risen at the same rate as everywhere else."

---

## SLIDE 7 — KEY FINDING 2 (show Chart 5 — CPI trend lines)
**(45 seconds)**

**Title:** Price Inflation Is Almost the Same Everywhere

**[Insert fig3_cpi_trend.png here]**

- All 16 states have seen prices rise by roughly **20–30%** since 2010
- The trend lines are very close together
- No single state has dramatically higher or lower inflation

**The insight:**
- The affordability gap between states is **NOT caused by price differences**
- It is caused by **income differences**
- Policy should therefore focus on **raising incomes** in low-affordability states — not on controlling prices

---

## SLIDE 8 — KEY FINDING 3 (show Chart 6 — 13 Category Heatmap)
**(1 minute)**

**Title:** What Is Driving Prices Up?

**[Insert fig4_cpi_heatmap.png here]**

- 13 spending categories × 16 states
- Darker = higher inflation in that category in that state

**Top 3 highest inflating categories:**
1. Restaurants & Hotels
2. Food & Non-Alcoholic Beverages
3. Housing, Water, Electricity & Gas

**Why this is the most important finding:**
These three categories are the ones that B40 households spend the MOST on.
They are not optional. You cannot skip eating. You cannot skip housing.
So the categories inflating the fastest are hitting the poorest the hardest.

---

## SLIDE 9 — ADVANCED ANALYSIS (Forecast + Dashboard)
**(1 minute)**

**Title:** Advanced Analysis — Forecasting and Interactive Dashboard

**CPI Forecast:**
- Used `statsmodels` linear trend model in Python
- Projected CPI for the 5 least affordable states through 2027
- Result: prices will keep rising if no intervention happens
- These states need policy action NOW before the squeeze gets worse

**Streamlit Dashboard:**
- Built an interactive web dashboard using the Streamlit Python library
- Reads the same merged CSV — one source of truth
- Features: state filter, spending category selector, affordability index chart,
  expenditure-to-income ratio chart, CPI trend chart, summary table
- Can demo live during presentation

> [DEMO MOMENT — switch to browser and show the dashboard here]

---

## SLIDE 10 — RECOMMENDATIONS
**(45 seconds)**

**Title:** What Should Be Done?

**Recommendation 1 — Target support geographically**
Federal assistance (cash transfers, subsidies) should be weighted more to Kelantan, Kedah, Sabah, Perlis, and Terengganu — not distributed equally across all states.

**Recommendation 2 — Focus on food and housing costs**
These two categories have inflated the most and are non-negotiable for B40 households.
Price controls on essential food items and more affordable public housing in low-affordability states.

**Recommendation 3 — Expand income monitoring**
HIES survey is only done every few years. By the time we get data, it is already 2-3 years old.
Annual surveys would allow real-time affordability tracking so policies can respond faster.

---

## SLIDE 11 — LIMITATIONS
**(30 seconds)**

**Title:** Limitations of Our Analysis

- HIES income data is **2022 only** — we cannot track how affordability changed year by year
- All income figures are **nominal** (not inflation-adjusted)
- CPI is an index relative to 2010 — not an absolute price level
- Linear forecast is simple — does not account for economic shocks or policy changes
- National income dataset (hh_income) had no state breakdown so it could only be used for national trends

---

## SLIDE 12 — CONCLUSION
**(30 seconds)**

**Title:** Summary

- We merged **price data and income data** from DOSM using state as the common key
- We created an **Affordability Index** that shows which states are most squeezed
- **Kelantan, Kedah, Perlis, Sabah, and Terengganu** are the least affordable states
- The squeeze is driven by **food, housing, and restaurants** inflating the most
- Price inflation is **uniform** across all states — so income growth is the solution, not price control
- We built a **Streamlit dashboard** and **CPI forecast** as advanced analysis

**Closing line to say:**
"This project shows how combining two government datasets and engineering a single new metric can answer a real policy question that neither dataset could answer alone."

---

## SLIDE 13 — THANK YOU / Q&A
**(buffer)**

**Title:** Thank You

- Questions?
- Dashboard demo available if needed
- All code and data available in the project repository

---

# PRESENTATION TIPS

**Time breakdown (10 minutes total):**
- Slides 1-2: 1 min 15 sec (intro and problem)
- Slides 3-5: 3 min 30 sec (data and method)
- Slides 6-8: 2 min 45 sec (findings — the most important part)
- Slides 9-10: 1 min 45 sec (advanced analysis and recommendations)
- Slides 11-12: 1 min (limitations and conclusion)
- Buffer for Q&A transition: 15 sec

**Who presents what (suggestion for 4 members):**
- Member 1: Slides 1, 2, 3 — Intro, problem, datasets
- Member 2: Slides 4, 5 — Data wrangling and affordability index
- Member 3: Slides 6, 7, 8 — Key findings and charts
- Member 4: Slides 9, 10, 11, 12 — Advanced analysis, recommendations, conclusion

**During the dashboard demo (Slide 9):**
1. Open the browser with the dashboard already running
2. Start with all 16 states selected — show the affordability index
3. Deselect all states except Kelantan, Kedah, Perlis, Sabah, Terengganu
4. Switch the CPI Division dropdown to "Food & Non-Alcoholic Beverages"
5. Point out how food prices have risen steadily in these states since 2010

**Likely Q&A questions and short answers:**

Q: Why did you use CPI instead of actual prices in ringgit?
A: CPI is what DOSM officially publishes for price tracking. It is also a relative measure which makes it easier to compare across states and over time.

Q: Why is the HIES data only for 2022?
A: DOSM only conducts the HIES survey every few years. 2022 is the most recent available. This is a limitation we acknowledged in our report.

Q: How did you create the affordability index?
A: We divided mean household income by the overall CPI for each state, then scaled the result so the national mean equals 100. Any state below 100 is less affordable than the national average.

Q: Why is Putrajaya so affordable?
A: W.P. Putrajaya is dominated by government employees who tend to have higher and more stable incomes. The income level there is among the highest in Malaysia, which pushes the affordability index well above 100 even though prices are similar to other states.
