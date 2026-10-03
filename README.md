# Marketing Attribution Analysis in Adobe CJA

This repository contains the code, analysis workflow, and outputs for a project examining why some marketing channels appear undervalued under last-touch attribution in Adobe Customer Journey Analytics (CJA).

The project uses exported CSV data from Adobe CJA’s Omni-Channel Multi-Industry demo environment and compares last-touch, linear, and algorithmic attribution across 16 marketing channels. The analysis also uses lifecycle metrics, conversion environment data, revenue context, and chart-based reporting.

## Project question

Why are some marketing channels undervalued under last-touch attribution in Adobe Customer Journey Analytics?

## Project goal

The purpose of the project is to show how attribution model choice affects channel valuation, and to examine whether lifecycle role and conversion context help explain these differences.

## Data sources

The analysis is based on exported CSV files from Adobe CJA Omni-Channel Multi-Industry demo data for May 2026, including:

- Marketing Channel Performance - Comparing models and lookback windows
- Marketing Acquisition vs. Closure
- Marketing Performance by Channel
- Marketing Performance by Conversion Channel

## Workflow

The project was developed step by step in Python and SQLite.

### 1. Data cleaning and master table creation
`01_clean_and_build.py`

This script:
- loads the raw CSV files,
- skips descriptive header lines in the Adobe exports,
- standardizes channel names,
- merges the datasets into one master table,
- creates derived variables such as:
  - `delta_alg_vs_last`
  - `pct_delta_alg_vs_last`
  - `delta_linear_vs_last`
  - `revenue_per_order`
  - `order_share_pct`
- classifies channels into:
  - `Gainer`
  - `Loser`
  - `Stable`

Output:
- `master_channel_table.csv`

### 2. Attribution analysis
`02_attribution_analysis.py`

This script:
- ranks channels by attribution change,
- compares algorithmic vs. last-touch,
- compares linear vs. last-touch,
- exports summary tables for interpretation.

Outputs:
- `attribution_ranking.csv`
- `model_comparison.csv`

### 3. Lifecycle analysis
`03_lifecycle_correlation.py`

This script:
- examines lifecycle index by attribution class,
- summarizes channel-level lifecycle patterns,
- exports lifecycle detail for reporting.

Output:
- `lifecycle_correlation.csv`

### 4. Conversion context analysis
`04_conversion_context.py`

This script:
- calculates channel-level conversion environment shares,
- identifies each channel’s dominant conversion environment,
- creates supporting context for result interpretation.

Output:
- `conversion_context.csv`

### 5. Charts
`05_charts.py`

This script creates charts used in the report, including:
- acquisition vs closure rate by channel,
- conversion environment by channel.

Chart files:
- `chart2_lifecycle_scatter.png`
- `chart3_conversion_environment.png`

### 6. SQL validation and second analysis method
`06_sql_analysis.py`

This script:
- loads the processed data into an in-memory SQLite database,
- validates the Python findings through SQL queries,
- ranks channels,
- links lifecycle metrics to attribution change,
- compares revenue context and conversion environment.

Outputs:
- `q1_attribution_ranking.csv`
- `q2_lifecycle_vs_delta.csv`
- `q3_conversion_dependence.csv`
- `q4_revenue_vs_attribution.csv`

### 7. Findings memo
`07_findings_memo.py`

This script generates a short memo highlighting the most undervalued and overvalued channels under last-touch attribution.

Output:
- `findings_memo.csv`

## Main findings

The analysis shows that attribution model choice changes channel valuation substantially.

- Several channels gain credit under algorithmic attribution, especially Direct Mail, Social Referrals, and Print.
- Email, LLM, In-App Messaging, and SMS lose credit under algorithmic attribution compared with last-touch.
- Lifecycle metrics help explain part of the pattern.
- Conversion environment concentration adds further context, especially for channels such as In-App Messaging and Email.
- Revenue context shows that attribution change is not the same as business importance.

## Tools used

- Python
- pandas
- matplotlib
- SQLite
- VS Code
- GitHub

## Use of AI

AI was used as a support tool during the project.

It was used to:
- discuss suitable analytical approaches for the research question,
- support step-by-step code development,
- help troubleshoot outputs during the coding process,
- improve wording and language in the written report.

The scripts were developed iteratively: prompts were used to explore the next coding step, the suggested code was tested in VS Code, outputs were reviewed, and adjustments were made before continuing. The final codebase was then collected and uploaded to GitHub.

## Limitations

This project is based on demo data exported from Adobe CJA for one time period. The findings should therefore be interpreted as a structured analytical case rather than as universal evidence for all marketing environments.

## Repository purpose

This repository documents both the analytical results and the development process behind the thesis project.
