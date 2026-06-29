TDW 6323 DATA WRANGLING AND VISUALISATION
GROUP PROJECT REPORT


Subject Code and Name: TDW 6323 Data Wrangling and Visualisation
Group Name: [YOUR GROUP NAME]
Members:
[Student ID] - [Full Name]
[Student ID] - [Full Name]
[Student ID] - [Full Name]
[Student ID] - [Full Name]


TABLE OF CONTENTS

1. Introduction
2. Dataset Selection and Business Understanding
3. Data Wrangling
4. Exploratory Data Analysis
5. Data Visualisation
6. Business Insights and Recommendations
7. Advanced Analysis and Innovation
8. Conclusion
9. References


1. INTRODUCTION

Malaysia is a developing nation that has experienced rapid economic growth over the past few decades. While this growth has brought improvements in income levels and living standards for many Malaysians, it has also come with rising prices across essential goods and services. For ordinary households, especially those in the lower income group, the question of whether their income is keeping up with rising costs has become increasingly important. This is commonly referred to as the cost of living problem, and it is one of the most frequently discussed economic issues in Malaysia today.

This project was undertaken as part of the TDW 6323 Data Wrangling and Visualisation course. The goal of this project is to analyse real Malaysian government data to understand how affordable life is across different states in Malaysia, and to identify which spending categories are contributing most to rising prices. Rather than simply describing what the data contains, this project attempts to answer a meaningful and practical question: In which Malaysian states is life getting less affordable, where are prices rising faster than income, and which spending categories are driving this trend?

To answer this question, we used two publicly available datasets from the Department of Statistics Malaysia, commonly known as DOSM, which is the official government body responsible for collecting and publishing national statistics. These datasets were downloaded from OpenDOSM, which is the open data platform provided by DOSM. The first dataset contains monthly consumer price index data broken down by state and spending category, while the second dataset contains household income, expenditure, poverty rates, and Gini coefficients for all 16 states in Malaysia for the year 2022.

The approach taken in this project reflects real-world data analysis practice. Instead of relying on a single dataset, we combined two separate datasets to create a richer and more meaningful picture of affordability across Malaysian states. This required careful data wrangling, including cleaning the data, standardising formats, aggregating monthly figures into annual figures, and merging the two datasets using the state as the common attribute. The result is a merged dataset with more than 200 rows that serves as the foundation for all the analysis and visualisations in this report.

This report is structured to walk the reader through the entire analysis process, from dataset selection and data cleaning all the way to insights and recommendations. All analysis was performed using Python, with the pandas library used for data manipulation, matplotlib and seaborn used for visualisation, and statsmodels used for the predictive forecasting component. An interactive Streamlit dashboard was also built as part of the advanced analysis component.


2. DATASET SELECTION AND BUSINESS UNDERSTANDING

2.1 Overview of the Datasets

For this project, two datasets were obtained from OpenDOSM, which is the open data portal maintained by the Department of Statistics Malaysia. Both datasets are publicly available at no cost and do not require any login or special access. The datasets were downloaded in both CSV and Parquet format. The CSV format was retained as the readable submission-friendly version, while the Parquet format was used for actual data processing due to its better performance and type preservation.

The first dataset is the State-Level Consumer Price Index dataset, identified as cpi_2d_state. This dataset records the monthly consumer price index for all 16 Malaysian states, broken down across 13 spending divisions and one overall category. The 13 divisions represent standard categories of household spending such as food and non-alcoholic beverages, housing and utilities, transport, education, health, and others. The data spans from January 2010 all the way to May 2026, giving us more than 15 years of monthly price data. In total, this dataset contains 44,128 rows and 4 columns, which are the state name, the date, the division code, and the CPI index value.

The second dataset is the Household Income and Expenditure Survey state-level dataset for 2022, identified as hies_state. This dataset provides a snapshot of household welfare across all 16 Malaysian states as of 2022. It contains information on the mean and median household income, mean household expenditure, Gini coefficient, and poverty rate for each state. This dataset has 16 rows and 7 columns. While it is smaller in size compared to the CPI dataset, it provides the income and welfare context that is essential for measuring affordability.

A third dataset was also loaded, which is the national household income time series from 1970 to 2022, identified as hh_income. However, this dataset does not contain a state column, which means it only provides national-level income figures. It was used to understand the long-term trend of income growth at the national level but could not be directly merged with the state-level CPI data.

Dataset Source Links:
- State CPI by Division: https://open.dosm.gov.my/data-catalogue/cpi_2d_state
- HIES State 2022: https://open.dosm.gov.my/data-catalogue/hies_state
- National Household Income: https://open.dosm.gov.my/data-catalogue/hh_income

2.2 Description of Key Attributes

The CPI dataset uses a numeric index to represent prices, where the base year is 2010. This means that a CPI value of 100 represents the price level in 2010, and any value above 100 indicates that prices have risen since then. For example, a CPI of 130 means that prices in that state for that category are 30 percent higher than they were in 2010. The 13 spending divisions are coded as 01 through 13, with division 01 representing food and non-alcoholic beverages, division 04 representing housing, water, electricity, and gas, and division 07 representing transport, among others. There is also an overall category that represents the combined weighted average across all divisions.

The HIES dataset contains income and expenditure figures in Malaysian Ringgit per month. The mean income is the average monthly household income across all households in that state, while the median income gives a better representation of the typical household as it is not distorted by very high earners. The Gini coefficient ranges from 0 to 1, where 0 means perfect equality and 1 means maximum inequality. The poverty rate is expressed as a percentage of households living below the official poverty line.

2.3 Justification for Dataset Choice

The combination of these two datasets is particularly well-suited to answering the research question because neither dataset alone can answer it. The CPI dataset tells us how much prices have changed over time in each state and in each spending category, but it says nothing about whether households can afford those prices. The HIES dataset tells us what households earn and spend, but it does not tell us how prices have moved over time. By combining the two, we can calculate a real measure of affordability that takes both income and price levels into account.

This approach reflects genuine data wrangling practice, where raw datasets from different sources are combined using a common attribute to produce richer analytical output. In this case, the common attribute is the state name, which appears in both datasets.

2.4 Real-World Problem Being Addressed

The real-world problem this project addresses is the erosion of purchasing power for Malaysian households, particularly in states with lower income levels. Nominal incomes have risen in Malaysia over the years, but so have prices. The critical question is not whether incomes have risen in absolute terms, but whether they have risen fast enough to keep pace with rising prices. When prices rise faster than income, the real purchasing power of households falls, which means they can afford less even if they earn more on paper.

This problem is especially relevant for the B40 income group, which refers to the bottom 40 percent of Malaysian households by income. These households spend a higher fraction of their income on essential goods such as food, housing, and utilities, which are also among the categories that have seen the fastest price increases. Identifying which states are most affected and which spending categories are driving the squeeze is the first step towards designing effective policy responses.

2.5 Scope of Analysis

The scope of this analysis covers all 16 Malaysian states and territories, including Johor, Kedah, Kelantan, Melaka, Negeri Sembilan, Pahang, Perak, Perlis, Pulau Pinang, Sabah, Sarawak, Selangor, Terengganu, W.P. Kuala Lumpur, W.P. Labuan, and W.P. Putrajaya. The CPI time series covers the period from January 2010 to the latest available data. The HIES income and expenditure data is anchored to the 2022 survey year, which is the most recent available.


3. DATA WRANGLING

3.1 Loading the Datasets

All three datasets were loaded from their locally stored Parquet files using the pandas library in Python. Parquet format was chosen for processing because it preserves data types correctly, which is particularly important for date columns that can otherwise be read as plain text strings. The loading process was encapsulated in a dedicated module called load.py inside the src folder, which contains three separate functions, one for each dataset. Each function reads the corresponding Parquet file and immediately converts the date column to a proper datetime format using the pandas to_datetime function.

The shapes confirmed at loading time were as follows. The national household income dataset had 21 rows and 3 columns. The HIES state dataset had 16 rows and 7 columns. The CPI dataset had 44,128 rows and 4 columns. All three datasets loaded without any errors.

3.2 Exploring Dataset Properties

After loading, each dataset was inspected for its basic properties including the number of rows and columns, the data types of each column, the count of missing values, and basic summary statistics.

For the national household income dataset, the three columns are the date, mean income, and median income. The data types were object for date and integer for both income columns. There were no missing values. The dates range from 1970 to 2022, giving 21 survey years in total.

For the HIES state dataset, the seven columns are date, state, mean income, median income, mean expenditure, Gini coefficient, and poverty rate. All 16 rows represent the 16 Malaysian states and territories for the year 2022. There were no missing values. Income and expenditure values are stored as integers while Gini and poverty rate are floating point numbers.

For the CPI dataset, the four columns are state, date, division, and index. The date column was already stored as a proper datetime type in the Parquet file. There were no missing values across all 44,128 rows. The 16 unique state names in the CPI dataset matched exactly with the 16 state names in the HIES dataset, which confirmed that no state name normalisation would be required before merging.

3.3 Data Quality Issues and Handling

Several data quality considerations were identified and addressed during the wrangling process.

The first issue concerns the scope of the national household income dataset. This dataset does not contain a state column and represents national-level aggregates only. This means it cannot be directly used for any state-level analysis. A note was added in the code to flag this clearly, and the dataset was used only for understanding the national income trend rather than for the state-level merge.

The second issue relates to historical methodology breaks within the national income dataset. Surveys conducted before 1976 covered only Peninsular Malaysia and did not include Sabah and Sarawak. From 1989 onwards, the income figures represent citizens only rather than all residents. Both of these breaks represent shifts in the survey methodology that make it inappropriate to treat the data as a single continuous series without flagging these differences. Two boolean flag columns were added to mark rows affected by each of these methodology breaks. These flags ensure that no one accidentally averages or compares figures across the methodology break without being aware of it.

The third issue is that all income figures in both the HIES and national income datasets are nominal values, meaning they have not been adjusted for inflation. This is actually a feature rather than a problem for this analysis, because we are deliberately comparing nominal income to the CPI index to derive a real measure of affordability. However, it is important to state this clearly so that the limitations are understood.

The fourth consideration is the addition of derived features to enhance the data for analysis. For the HIES dataset, a new column called exp_to_income_ratio was computed by dividing mean expenditure by mean income. This ratio tells us what fraction of a household's monthly income goes towards expenditure, and it is a useful proxy for financial stress. A higher ratio means households have less money left over at the end of the month. For the CPI dataset, a year column was extracted from the date column to enable annual aggregation, and a human-readable division label column was added by mapping the numeric division codes to their full descriptions.

3.4 Data Merging

The merge strategy for this project involved two main steps. The first step was to aggregate the monthly CPI data into annual means. Since the CPI is recorded monthly but the HIES income data is available only as an annual survey snapshot, it was necessary to reduce the monthly CPI data to an annual average before merging. This was done by grouping the CPI data by state, year, division, and division label, then computing the mean of the index values within each group. This produced a cleaned annual CPI dataset with one row per state per year per division.

The second step was the actual merge between the HIES 2022 snapshot and the 2022 annual CPI data. The HIES data has 16 rows representing the 16 states, and the 2022 annual CPI data has 14 rows per state representing the 13 divisions plus the overall category. Merging these two on the state column using an inner join resulted in 16 times 14, which equals 224 rows. This satisfies the requirement for the merged dataset to have more than 200 rows.

The merge was performed with explicit documentation of the row counts before and after the merge to verify that no rows were unexpectedly dropped or duplicated. The before counts were 16 rows for the HIES data and 224 rows for the 2022 CPI slice, and the after count was 224 rows as expected. This confirms that the merge was clean with no data loss.

The final merged dataset was exported as a CSV file to the data/processed folder under the filename merged_affordability_2022.csv. This file contains 224 rows and 13 columns, and it serves as the single source of truth for all subsequent analysis and the Streamlit dashboard.


4. EXPLORATORY DATA ANALYSIS

4.1 Summary Statistics

After merging the datasets, summary statistics were computed for all numerical variables to understand the distribution and range of values across the 16 Malaysian states.

For household income, the mean monthly household income across all 16 states ranged from a low of around RM 4,885 in Kelantan to a high of around RM 17,050 in W.P. Putrajaya. The national mean across all states was approximately RM 8,200 per month. The gap between the highest and lowest income states is substantial, with the richest state earning more than three times the amount of the poorest state. The median income figures are consistently lower than the mean income figures, which indicates that the income distribution within each state is positively skewed with some high earners pulling the average upward.

For household expenditure, the mean monthly expenditure ranged from around RM 3,505 in Kelantan to around RM 6,050 in Selangor. When expressed as a ratio of income, the expenditure-to-income ratio ranged from around 0.63 in W.P. Putrajaya to around 0.90 in some of the lower-income states. This means that households in the lower-income states are spending almost 90 cents of every ringgit they earn, leaving very little financial buffer for savings or unexpected expenses.

For the Gini coefficient, the values ranged from around 0.33 to 0.40 across the 16 states. The poverty rate ranged from less than 1 percent in W.P. Putrajaya to over 13 percent in Kelantan and over 20 percent in Sabah.

For the overall CPI in 2022, the values were broadly similar across all 16 states, ranging from approximately 119 to 125, which means that prices in 2022 were between 19 and 25 percent higher than they were in 2010 across all states.

4.2 The Affordability Index

The most important engineered feature in this analysis is the affordability index. This was calculated by dividing the mean household income of each state by its overall CPI value for 2022. This ratio gives us a measure of how much purchasing power each state's average household has relative to the price level in that state. The resulting values were then scaled so that the national mean equals 100, making it easy to see which states are above or below the national average.

A state with an affordability index above 100 means its households have relatively strong purchasing power compared to the national average. A state with an index below 100 means its households are more squeezed, with income not keeping pace with local price levels.

The results revealed a clear pattern. States in the northern peninsula and East Malaysia tend to have affordability indexes well below 100. Kelantan, for example, had one of the lowest affordability indexes, reflecting the combination of low household income and price levels that have converged upward towards the national average. In contrast, W.P. Kuala Lumpur, Selangor, and W.P. Putrajaya had affordability indexes well above 100, driven by significantly higher nominal incomes that more than compensate for their higher price levels.

4.3 Correlation Analysis

A correlation analysis was conducted on the key welfare indicators to understand the relationships between income, expenditure, the expenditure-to-income ratio, the Gini coefficient, poverty rate, and the affordability index.

The most striking finding from the correlation analysis is that income and expenditure are strongly positively correlated, which makes intuitive sense since richer states also tend to spend more in absolute terms. However, the affordability index is strongly positively correlated with income, which confirms that higher income is the main driver of better affordability rather than lower prices. This is an important finding because it suggests that price convergence across states has already largely occurred, and what is left is an income divergence problem rather than a price problem.

The poverty rate shows a strong negative correlation with the affordability index, meaning that states with lower affordability also tend to have higher poverty rates. The Gini coefficient, however, shows only a weak correlation with affordability, suggesting that inequality within a state is not a reliable predictor of how unaffordable that state is on average.

4.4 CPI Category Trends

Analysing the CPI data by division revealed that not all spending categories have inflated at the same rate since 2010. Some categories have seen dramatic price increases while others have barely moved. This is important because different income groups spend their money on different things, and understanding which categories have inflated fastest helps identify where the cost-of-living squeeze is hitting hardest.

Looking at cumulative CPI growth from 2010 to 2024, the highest inflating categories at the national level were restaurants and hotels, food and non-alcoholic beverages, and housing, water, electricity and gas. These three categories are notable because they are also the ones that lower-income households spend the greatest share of their budget on. In other words, the categories that have become most expensive are also the categories that B40 households can least afford to cut back on.

On the other hand, categories like communication and clothing and footwear showed much more modest price increases, with some even declining in relative terms. These are also categories where households have more flexibility to substitute or reduce spending.


5. DATA VISUALISATION

5.1 Figure 1 – Distribution of Household Income and Expenditure-to-Income Ratio

The first visualisation presents two charts side by side. The left chart is a histogram showing the distribution of mean household income across the 16 Malaysian states in 2022. The distribution is right-skewed, meaning that most states are clustered at the lower end of the income range while a small number of states with very high incomes, such as Selangor and W.P. Kuala Lumpur, pull the tail to the right. A vertical dashed line marks the national mean income, showing that more than half of the states fall below this average. This is a direct consequence of the skewed distribution and illustrates why using the national average as a benchmark for poverty or welfare policy can be misleading.

The right chart is a box plot showing the spread of the expenditure-to-income ratio across all states. The median ratio is approximately 0.70, meaning the typical Malaysian state sees its households spend 70 percent of their income on measured expenditure. The upper whisker extends close to 0.90, indicating that some states have households that are spending nearly all of their income. No states show a ratio above 1.0, meaning no state is spending more than it earns on average, but the states closest to 1.0 have very little financial resilience.

5.2 Figure 2 – Relationship Between Income and Expenditure with Poverty Rate

The second visualisation contains a scatter plot and a correlation heatmap. The scatter plot shows the relationship between mean income and mean expenditure for each state, with each data point coloured and sized according to its poverty rate. States with higher poverty rates appear as larger, darker dots. The dashed diagonal line represents the point where income equals expenditure. All states fall below this line, confirming that no state is spending more than it earns on average, but states with higher poverty rates are noticeably closer to the line, indicating a much thinner financial buffer.

The correlation heatmap uses a red-to-blue colour scale to show the strength and direction of correlations between all key variables. Dark red cells indicate strong positive correlations and dark blue cells indicate strong negative correlations. The heatmap clearly shows that the affordability index is strongly negatively correlated with poverty, confirming that affordability erosion and poverty co-occur in the same states.

5.3 Figure 3 – CPI Trend Lines by State Over Time

The third visualisation shows the overall CPI index for all 16 states from 2010 to the present, with each state represented by a separate coloured line. All lines are anchored at 100 in the base year of 2010. The chart reveals that all 16 states have followed a broadly similar upward trajectory, with prices rising consistently over the 15-year period. The lines are relatively close together, which confirms that price inflation has been largely uniform across states. This is a critical insight: price levels have converged across Malaysia, which means that income differences are the primary driver of the affordability gap between states rather than price differences.

5.4 Figure 4 – 13-Division CPI Heatmap

The fourth visualisation is the showpiece chart of the project. It is a heatmap with 13 spending divisions on the vertical axis and 16 states on the horizontal axis. Each cell shows the cumulative percentage price increase in that division in that state from 2010 to 2024. Darker orange and red cells indicate higher cumulative inflation.

The heatmap reveals a clear pattern where the darkest cells are concentrated in the restaurants and hotels category, the food and non-alcoholic beverages category, and the housing, water, electricity and gas category. These categories have seen the highest inflation across virtually all states. In contrast, the communication and clothing rows are much lighter, indicating minimal price increases. This visualisation is particularly powerful because it allows decision-makers to see at a glance which spending categories are driving the cost-of-living problem and whether the problem is uniform across states or concentrated in specific regions.

5.5 Figure 5 – Affordability Index and Expenditure-to-Income Ratio Ranking

The fifth visualisation presents two horizontal bar charts. The left chart ranks all 16 states by their affordability index, with states falling below the national average of 100 coloured in red and states above it coloured in blue. This chart immediately answers the central research question of the project by visually identifying which states have the worst affordability in Malaysia. The right chart ranks states by their expenditure-to-income ratio, with states above the median coloured in a warmer tone to indicate higher financial stress.

Together, these two charts tell a consistent story. The states that appear red in the affordability chart also tend to appear in the upper half of the expenditure-to-income chart, confirming that affordability is a multidimensional squeeze rather than a single-variable problem.


6. BUSINESS INSIGHTS AND RECOMMENDATIONS

6.1 Thesis Statement

The central finding of this project is that real purchasing power is not deteriorating equally across Malaysia. It is eroding most significantly in a specific group of states that combine relatively low household incomes with price levels that have risen in line with the national average. The states where affordability is most constrained include Kelantan, Kedah, Perlis, Sabah, and Terengganu. These states have affordability indexes well below the national average of 100, meaning their households are getting less value for every ringgit earned compared to the national norm.

6.2 Key Findings

The first key finding is that price inflation has been broadly uniform across all 16 Malaysian states since 2010. All states have seen their overall CPI rise by between 19 and 25 percent over this period. This means that the affordability gap between states is primarily driven by income differences rather than price differences. States that are unaffordable are unaffordable mainly because incomes are low, not because prices are exceptionally high.

The second key finding is that the spending categories that have inflated the most are also the ones that lower-income households spend the most on. Food and non-alcoholic beverages, restaurants and hotels, and housing, water, electricity and gas are the three highest-inflating divisions. These are not discretionary spending categories. Households cannot easily reduce spending on food, shelter, or utilities without significant lifestyle sacrifices. This means the inflation burden is disproportionately heavy for the B40 group.

The third key finding is that the states with the lowest affordability indexes also tend to have the highest poverty rates and the highest expenditure-to-income ratios. This creates a self-reinforcing vulnerability: households in these states earn less, spend a higher proportion of their income just to maintain basic living standards, have higher poverty rates, and face the same or similar price increases as wealthier states.

6.3 Recommendations

Based on the findings of this analysis, the following recommendations are offered for policy makers and relevant agencies.

First, federal assistance programmes such as direct cash transfers and targeted subsidies should be weighted more heavily towards the states identified as having the lowest affordability indexes. A uniform national assistance rate does not reflect the unequal distribution of affordability stress across states.

Second, category-specific interventions should be directed at food and housing costs, which are the two highest-inflating categories with the highest spending weights for lower-income households. Price controls or subsidised essential goods programmes targeting food staples in low-affordability states could provide meaningful relief. For housing, increased investment in affordable public housing in states like Kelantan, Kedah, and Sabah would help reduce the housing cost burden.

Third, the government should consider expanding the frequency of the Household Income and Expenditure Survey from once every few years to annually or biannually. The current gap in income data means that real-time affordability monitoring is impossible. Policy makers are essentially flying blind between survey years when it comes to understanding whether real purchasing power is improving or deteriorating.

6.4 Limitations of the Analysis

Every analysis has limitations, and it is important to be transparent about them. The first limitation is the sparseness of income data at the state level. The HIES survey provides state-level income and expenditure data only for specific survey years, with 2022 being the most recent. This means the analysis cannot track how state-level affordability has changed year by year over the full CPI time series. The affordability index is a cross-sectional snapshot for 2022, not a time series.

The second limitation is that all income figures are nominal and not inflation-adjusted. While the affordability index combines income and CPI in a way that approximates real purchasing power, it does not produce a formally deflated income series.

The third limitation concerns the CPI itself. The CPI is an index relative to a base year rather than an absolute price level measure. A state with a CPI of 130 is not necessarily more expensive in absolute terms than a state with a CPI of 125. It has simply inflated more since 2010. States that were already expensive in 2010 and inflated only modestly might still be more expensive in absolute terms than a state that was cheap in 2010 but inflated more.

The fourth limitation is the linear forecast used in the advanced analysis section. Linear trend models are simple and interpretable but they do not capture non-linear shocks such as commodity price spikes, exchange rate movements, or policy changes that can cause sudden jumps in the CPI.

6.5 Suggestions for Further Investigation

Future research could extend this analysis by incorporating labour market data at the state level, such as wages by sector and by industry, to better understand whether income growth is keeping pace with price growth within specific sectors rather than just at the household average level.

Additionally, access to household-level microdata from the HIES survey would allow within-state inequality analysis, revealing how affordability differs between the richest and poorest households within a single state.

Linking the PLI which stands for the Poverty Line Income to state-level CPI data would also help evaluate whether the official poverty threshold is set at a level that accurately reflects the actual cost of living in each state rather than being based on a single national figure.


7. ADVANCED ANALYSIS AND INNOVATION

7.1 CPI Forecasting with Trend Models

As part of the advanced analysis component, a linear trend model was applied to the overall CPI index for the five states with the lowest affordability indexes. The objective was to project the near-term trajectory of price levels in these states and assess whether the cost-of-living squeeze is likely to get better or worse in the coming years.

The forecasting was implemented using the statsmodels library in Python, which is a widely used library for statistical modelling and econometrics. An ordinary least squares regression was fitted to the annual CPI index series for each state, with the year as the independent variable and the CPI index as the dependent variable. The fitted model was then used to generate forecasts for the years 2025, 2026, and 2027.

The results show that all five of the lowest-affordability states are projected to see continued CPI growth through 2027 under the current linear trend. If income growth does not accelerate to match or exceed this projected price growth, these states will experience further deterioration in real purchasing power over the next two to three years. These forecasts should be interpreted as indicative projections based on historical trends, not as precise predictions, since they do not account for policy interventions, commodity price shocks, or changes in economic conditions.

7.2 Interactive Streamlit Dashboard

An interactive web-based dashboard was developed using the Streamlit library in Python. The dashboard reads directly from the same merged CSV file produced during the data wrangling phase, ensuring that the dashboard and the notebook analysis are always working from the same source of truth.

The dashboard is organised into several sections. At the top, a sidebar allows users to filter the analysis by selecting which states to include and which CPI spending division to view in the trend chart. Below the sidebar, a row of key performance indicator cards displays summary statistics for the selected states, including the number of states selected, the average mean income, the average expenditure-to-income ratio, and the average poverty rate.

The main body of the dashboard contains four charts. The first chart is a horizontal bar chart showing the affordability index for each selected state, coloured red for states below the national average and blue for states above it. The second chart shows the expenditure-to-income ratio for each selected state. The third chart shows the CPI trend over time for the selected division in each selected state. The fourth chart shows the cumulative overall CPI growth since 2010 for each selected state.

At the bottom of the dashboard, a full summary table displays all key metrics for the selected states in a formatted and colour-coded table. The affordability index column is colour-coded using a red-to-green gradient to make it immediately visible which states are most and least affordable.

The dashboard can be launched by running the command python -m streamlit run app/dashboard.py from the project root directory. It will open automatically in the default web browser.

The Streamlit dashboard serves as both a practical decision-support tool and a presentation aid. During the presentation, the dashboard can be used to demonstrate findings interactively by selecting different states and spending categories in real time, making the analysis more engaging and accessible to a non-technical audience.


8. CONCLUSION

This project set out to answer a single focused question: In which Malaysian states is life getting less affordable, and which spending categories are driving it? Using publicly available data from OpenDOSM, we combined two separate government datasets, applied data wrangling techniques to clean, aggregate, and merge the data, engineered a new affordability metric, and produced a set of visualisations and insights that directly address the research question.

The analysis found that price inflation has been broadly uniform across all 16 Malaysian states since 2010, with overall CPI rising by between 19 and 25 percent over the period. However, the impact of this price inflation on households varies enormously by state because household income levels differ so significantly. States with lower income levels, particularly in the northern peninsula and East Malaysia, are experiencing the most significant affordability squeeze. Their households spend a higher proportion of their income just to maintain basic living standards, and they face the same rising prices as wealthier states without the income buffer to absorb the impact.

The spending categories that have inflated the most since 2010 are food and non-alcoholic beverages, restaurants and hotels, and housing, water, electricity and gas. These are also the categories that lower-income households spend the most on, making the inflation burden disproportionately heavy for the B40 group.

The affordability index developed in this project, which compares income to CPI at the state level, revealed that states like Kelantan, Kedah, Perlis, Sabah, and Terengganu are the most affordability-constrained in Malaysia. These states require targeted policy attention in the form of income support programmes, category-specific price interventions in food and housing, and more frequent income monitoring through expanded survey coverage.

This project demonstrates the value of combining and wrangling multiple datasets to generate insights that neither dataset could produce alone. The merged dataset, the engineered features, the visualisations, and the interactive dashboard together form a complete data analytics product that can support real-world decision-making on one of the most pressing socioeconomic issues facing Malaysia today.


9. REFERENCES

Department of Statistics Malaysia. (2024). Consumer Price Index Malaysia, 2024. DOSM. https://www.dosm.gov.my

Department of Statistics Malaysia. (2023). Household Income and Expenditure Survey (HIES) 2022. DOSM. https://www.dosm.gov.my

Department of Statistics Malaysia. (2024). OpenDOSM Data Catalogue. https://open.dosm.gov.my

Department of Statistics Malaysia. (2024). State-level CPI by Division (cpi_2d_state). OpenDOSM. https://open.dosm.gov.my/data-catalogue/cpi_2d_state

Department of Statistics Malaysia. (2024). HIES State 2022 (hies_state). OpenDOSM. https://open.dosm.gov.my/data-catalogue/hies_state

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science and Engineering, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55

McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 56–61.

Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference, 57–61.

Streamlit Inc. (2024). Streamlit documentation. https://docs.streamlit.io

Waskom, M. L. (2021). Seaborn: Statistical data visualization. Journal of Open Source Software, 6(60), 3021. https://doi.org/10.21105/joss.03021
