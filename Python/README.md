# How Attribution Shapes Reported Channel Performance

A descriptive study of how attribution settings shape the assessment of marketing channel performance. The analysis compares last-touch, linear, and algorithmic order credit across 16 channels using Adobe Customer Journey Analytics (CJA) demo exports for May 2026.

Attribution assigns credit for a conversion to preceding marketing interactions. Last-touch assigns all credit to the final eligible interaction. My starting concern was how much that final-interaction rule influences the performance picture presented by a channel report.

## Research question

**How does using last-touch attribution shape the assessment of marketing channel performance, and how does that assessment change under alternative models and lookback windows?**

Last-touch is the comparison baseline in this study. Linear and algorithmic attribution are alternative allocations; the exports do not establish which model represents a channel's true incremental contribution.

## Main findings

All percentage changes below compare an alternative model with last-touch within the same lookback window.

| Observation | Evidence from the demo exports |
| --- | --- |
| Model choice can change the direction of a comparison. | Paid Search receives **12.09% more** algorithmic credit but **5.71% less** linear credit at 30 days. |
| Credit change and channel rank can tell different stories. | Email receives **43.90% less** algorithmic credit at 30 days, yet ranks first by attributed orders under all six settings. |
| A large relative increase can begin from a small baseline. | Direct Mail receives **182.78% more** algorithmic credit at 30 days, while moving from 14th to 13th by attributed orders. |
| The window can change the magnitude and classification. | SMS receives **7.10% less** algorithmic credit at 14 days and **17.47% less** at 30 days, crossing the study's descriptive −10% boundary. |

These findings suggest that attribution settings, baseline order volume, and consistency across settings are relevant considerations when interpreting reported channel performance. Changes in allocated credit do not themselves measure changes in actual orders caused by a channel.

## Data and scope

- **Source:** Adobe CJA's Omni-Channel - Multi-Industry demo.
- **Reporting period:** May 1–31, 2026.
- **Metric and scope:** Total Orders, using the Person attribution container.
- **Comparisons:** Last-touch, linear, and algorithmic attribution, each with 14-day and 30-day lookbacks.
- **Channel mix:** All 16 channels, including digital advertising, messaging, search, and offline channels.

Four exports in [Data-raw](Data-raw/) are used:

| Export | Contribution |
| --- | --- |
| `AP Marketing Channel Performance - Comparing models and lookback windows.csv` | Attributed orders under all six settings |
| `MP Marketing Acquisition vs- Closure.csv` | Exported acquisition, closure, and Lifecycle Index metrics |
| `MP Marketing Performance by Channel.csv` | Last-touch orders and reported revenue |
| `MP Marketing Performance by Conversion Channel.csv` | Orders completed through Mobile App, Website, Mobile Web, Point of Sale, and Call Center |

The lookback window is measured backwards from each conversion, rather than defining a different reporting month. Model totals agree within each window: **231,678** orders at 14 days and **236,183** at 30 days. The difference between windows is **4,505**, or **1.94%** relative to the 14-day total. The aggregate exports do not explain this difference, so an identical conversion cohort cannot be assumed across windows.

## Method and outputs

Python cleans the exports, trims channel names, removes totals and breakdown-label rows, and joins the four sources by channel. The resulting master table has 16 unique channels and 26 complete fields. SQLite provides a second implementation of selected comparisons using that same table.

Relative credit change is:

```text
100 × (alternative attributed orders − last-touch attributed orders)
    / last-touch attributed orders
```

Both inputs use the same window. Calculations use full-precision values; reported percentages are rounded for display. Order-volume ranks are calculated separately for each model and window.

| Script in [Python](Python/) | Main outputs |
| --- | --- |
| `01_clean_and_build.py` | `master_channel_table.csv` |
| `02_attribution_analysis.py` | `attribution_ranking.csv`, `model_comparison.csv` |
| `03_lifecycle_correlation.py` | `lifecycle_correlation.csv`, `lifecycle_correlation_summary.csv` |
| `04_conversion_context.py` | `conversion_context.csv` |
| `05_charts.py` | Attribution-change, acquisition-versus-closure, and conversion-environment charts |
| `06_sql_analysis.py` | Four query results in [SQL](SQL/) |
| `07_findings_memo.py` | `findings_memo.csv` |

Tables are saved to [Data-output/data](Data-output/data/). The revised chart filenames are `chart1_attribution_delta.png`, `chart2_acquisition_vs_closure.png`, and `chart3_conversion_environment.png` in [Data-output/charts](Data-output/charts/).

The Python and SQL summary comparisons focus on the 30-day window. The standalone web case study presents order credit and rankings across both windows. Its embedded dataset must be updated if the underlying exports change.

The master table retains the code labels `Gainer`, `Loser`, and `Stable`: they mean at least 10% higher, at least 10% lower, and within ±10% algorithmic credit relative to 30-day last-touch. They are descriptive credit bands, not judgments of channel effectiveness. The master fields `pct_delta_alg_vs_last` and `pct_delta_linear_vs_last` store relative fractions; presentation fields such as `algorithmic_change_pct` express percentages.

Supporting analysis describes reported revenue, conversion environments, and lifecycle metrics. The Lifecycle Index has a Pearson correlation of **0.547** and a Spearman correlation of **0.335** with 30-day algorithmic credit change across 16 channels. These associations do not explain the allocation differences or establish a channel's journey role.

## Run the analysis

Use Python 3 with pandas, NumPy, and Matplotlib. SQLite is included in Python's standard library.

From the **repository root**, install the dependencies and run the scripts in order:

```shell
python -m pip install pandas numpy matplotlib
cd Python
python 01_clean_and_build.py
python 02_attribution_analysis.py
python 03_lifecycle_correlation.py
python 04_conversion_context.py
python 05_charts.py
python 06_sql_analysis.py
python 07_findings_memo.py
```

If the terminal is already inside `Python`, start with the script commands. The scripts use paths relative to that directory and regenerate their CSV and chart outputs.

## Iterative development with AI

The implementation was generated and revised with AI assistance. **Claude Sonnet** was used for the initial coding, and **ChatGPT-6.1 Sol** was used to review and revise the project.

I set the analytical question, supplied the exports, and worked through the implementation in successive steps: describe a task, obtain proposed code, run it in VS Code, inspect the outputs, report issues, and request revisions. This cycle covered data preparation, calculations, SQL queries, charts, and the written interpretation.

The revision addressed percentage units, chart labels, correlation reporting, the SQL revenue benchmark, and the distinction between changes in attributed credit and claims about effectiveness. The research narrative was also revised to describe sensitivity to attribution settings without assuming that last-touch had been proven wrong. The project documents an AI-assisted analytical workflow rather than unaided authorship of the code.

## Interpretation limits

This is one month of aggregate demo data. It does not establish campaign performance for a real business or support generalisation across organisations. The project compares exported CJA allocations; it does not train or reproduce Adobe's algorithmic model.

Acquisition and closure metric definitions, identity configuration, channel rules, and the revenue metric's detailed attribution settings are not fully documented in the exports. Revenue units are unspecified. There are no journey-level records, advertising costs, margins, or controlled experiments, so these results cannot determine CPA, ROAS, profitability, causal lift, or an optimal budget allocation.

## Reference documentation

- [Adobe CJA attribution components](https://experienceleague.adobe.com/en/docs/analytics-platform/using/cja-workspace/attribution/models)
- [Adobe CJA algorithmic attribution](https://experienceleague.adobe.com/en/docs/analytics-platform/using/cja-workspace/attribution/algorithmic)
