"""
TDW6323 — Malaysian Cost of Living Dashboard
Streamlit app reading data/processed/merged_affordability_2022.csv

Run: streamlit run app/dashboard.py  (from project root)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import matplotlib
matplotlib.use('Agg')  # force non-interactive backend before any other matplotlib import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from load import load_cpi
from clean import clean_cpi, DIVISION_LABELS
from merge import aggregate_cpi_annual, build_cpi_index

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title='TDW6323 — Malaysian Affordability',
    page_icon='🇲🇾',
    layout='wide',
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_processed():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'merged_affordability_2022.csv')
    return pd.read_csv(path)

@st.cache_data
def load_cpi_data():
    cpi_raw = load_cpi()
    cpi = clean_cpi(cpi_raw)
    cpi_annual = aggregate_cpi_annual(cpi)
    cpi_indexed = build_cpi_index(cpi_annual, base_year=2010)
    return cpi_annual, cpi_indexed

merged = load_processed()
cpi_annual, cpi_indexed = load_cpi_data()

# ── Derive affordability index ────────────────────────────────────────────────
overall = merged[merged['division'] == 'overall'].copy()
overall['raw_afford'] = overall['income_mean'] / overall['cpi_mean']
overall['affordability_index'] = overall['raw_afford'] / overall['raw_afford'].mean() * 100

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title('🇲🇾 Filters')
all_states = sorted(overall['state'].unique())
selected_states = st.sidebar.multiselect('Select states', all_states, default=all_states)

cpi_div_options = {v: k for k, v in DIVISION_LABELS.items() if k != 'overall'}
selected_div_label = st.sidebar.selectbox('CPI Division (trend chart)', list(cpi_div_options.keys()))
selected_div = cpi_div_options[selected_div_label]

# ── Header ────────────────────────────────────────────────────────────────────
st.title('Malaysian Cost of Living — Affordability Dashboard')
st.caption('Data: OpenDOSM | HIES 2022 + CPI by State 2010–2026 | TDW6323 Group Project')

# ── KPI row ───────────────────────────────────────────────────────────────────
filtered = overall[overall['state'].isin(selected_states)]
col1, col2, col3, col4 = st.columns(4)
col1.metric('States analysed', len(filtered))
col2.metric('Avg mean income (RM)', f"{filtered['income_mean'].mean():,.0f}")
col3.metric('Avg exp/income ratio', f"{filtered['exp_to_income_ratio'].mean():.2%}")
col4.metric('Avg poverty rate (%)', f"{filtered['poverty'].mean():.1f}")

st.markdown('---')

# ── Row 1 — Affordability index ───────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Affordability Index by State')
    st.caption('Income relative to overall CPI — national mean = 100. Below 100 = more squeezed.')
    fig, ax = plt.subplots(figsize=(7, 5))
    srt = filtered.sort_values('affordability_index')
    colours = ['#e05c5c' if x < 100 else '#4c8bb0' for x in srt['affordability_index']]
    ax.barh(srt['state'], srt['affordability_index'], color=colours, edgecolor='white', height=0.7)
    ax.axvline(100, color='black', linestyle='--', linewidth=1)
    ax.set_xlabel('Affordability Index')
    for i, (val, bar) in enumerate(zip(srt['affordability_index'], ax.patches)):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2, f'{val:.1f}', va='center', fontsize=8)
    st.pyplot(fig)
    plt.close(fig)

with col_b:
    st.subheader('Expenditure-to-Income Ratio')
    st.caption('Fraction of income spent on living costs — higher = less financial buffer.')
    fig, ax = plt.subplots(figsize=(7, 5))
    srt2 = filtered.sort_values('exp_to_income_ratio', ascending=False)
    ax.barh(srt2['state'], srt2['exp_to_income_ratio'], color='#e0895c', edgecolor='white', height=0.7)
    ax.axvline(filtered['exp_to_income_ratio'].median(), color='black', linestyle='--', linewidth=1, label='Median')
    ax.set_xlabel('Expenditure ÷ Income')
    ax.legend(fontsize=8)
    st.pyplot(fig)
    plt.close(fig)

st.markdown('---')

# ── Row 2 — CPI trend + heatmap ───────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader(f'CPI Trend — {selected_div_label}')
    st.caption('Annual mean CPI index (2010 = 100) for selected division.')
    fig, ax = plt.subplots(figsize=(7, 5))
    palette = sns.color_palette('tab20', len(selected_states))
    for i, state in enumerate(sorted(selected_states)):
        d = cpi_annual[(cpi_annual['state'] == state) & (cpi_annual['division'] == selected_div)].sort_values('year')
        if not d.empty:
            ax.plot(d['year'], d['cpi_mean'], label=state, color=palette[i], linewidth=1.4)
    ax.set_xlabel('Year')
    ax.set_ylabel('CPI Mean')
    ax.legend(fontsize=6, ncol=2)
    st.pyplot(fig)
    plt.close(fig)

with col_d:
    st.subheader('Overall CPI Growth — 2010 → 2024')
    st.caption('Cumulative % price rise by state (overall CPI index).')
    d2024 = cpi_indexed[cpi_indexed['year'] == 2024][['state', 'cpi_index']].copy()
    d2024 = d2024[d2024['state'].isin(selected_states)].sort_values('cpi_index', ascending=False)
    d2024['pct_rise'] = d2024['cpi_index'] - 100
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(d2024['state'], d2024['pct_rise'], color='#9b72cf', edgecolor='white', height=0.7)
    ax.set_xlabel('CPI % Rise Since 2010')
    for i, (val, bar) in enumerate(zip(d2024['pct_rise'], ax.patches)):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2, f'+{val:.1f}%', va='center', fontsize=8)
    st.pyplot(fig)
    plt.close(fig)

st.markdown('---')

# ── Row 3 — State detail table ────────────────────────────────────────────────
st.subheader('State-Level Summary Table (2022)')
display_cols = ['state', 'income_mean', 'income_median', 'expenditure_mean',
                'exp_to_income_ratio', 'gini', 'poverty', 'affordability_index']
table = filtered[display_cols].copy()
table = table.rename(columns={
    'state': 'State',
    'income_mean': 'Mean Income (RM)',
    'income_median': 'Median Income (RM)',
    'expenditure_mean': 'Mean Expenditure (RM)',
    'exp_to_income_ratio': 'Exp/Income',
    'gini': 'Gini',
    'poverty': 'Poverty Rate (%)',
    'affordability_index': 'Afford. Index',
})
table = table.sort_values('Afford. Index').set_index('State')
st.dataframe(
    table.style.format({
        'Mean Income (RM)': 'RM {:,.0f}',
        'Median Income (RM)': 'RM {:,.0f}',
        'Mean Expenditure (RM)': 'RM {:,.0f}',
        'Exp/Income': '{:.2%}',
        'Gini': '{:.3f}',
        'Poverty Rate (%)': '{:.1f}%',
        'Afford. Index': '{:.1f}',
    }).background_gradient(subset=['Afford. Index'], cmap='RdYlGn'),
    use_container_width=True,
)

st.caption('Source: DOSM OpenDOSM — hies_state 2022, cpi_2d_state 2010–2026. TDW6323 Group Project.')
