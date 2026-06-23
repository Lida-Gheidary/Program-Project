import pandas as pd
import numpy as np
import os

os.makedirs("../Data-output/data", exist_ok=True)

# Load attribution comparison file (primary dataset)
attr = pd.read_csv(
    "../Data-raw/AP Marketing Channel Performance - Comparing models and lookback windows.csv",
    skiprows=10
)

# Rename columns
attr.columns = ["channel", "sessions",
                "last_touch_30d", "last_touch_14d",
                "linear_30d", "linear_14d",
                "algorithmic_30d", "algorithmic_14d"]

# Remove the totals row
attr = attr[attr["channel"] != "Marketing Channel"].copy()

# Clean up
attr["channel"] = attr["channel"].str.strip()
attr = attr.reset_index(drop=True)


# Load lifecycle / acquisition vs closure
lc = pd.read_csv(
    "../Data-raw/MP Marketing Acquisition vs- Closure.csv",
    skiprows=10
)
lc.columns = ["channel", "acquisition_rate", "closure_rate", "lifecycle_index"]
lc = lc[lc["channel"] != "Marketing Channel"].copy()
lc["channel"] = lc["channel"].str.strip()
lc = lc.reset_index(drop=True)

# Load channel performance (orders + revenue)
perf = pd.read_csv(
    "../Data-raw/MP Marketing Performance by Channel.csv",
    skiprows=10
)
perf.columns = ["channel", "orders_last_touch_30d", "total_revenue"]
perf = perf[perf["channel"] != "Marketing Channel"].copy()
perf["channel"] = perf["channel"].str.strip()
perf = perf.reset_index(drop=True)

# Load conversion channel distribution
conv = pd.read_csv(
    "../Data-raw/MP Marketing Performance by Conversion Channel.csv",
    skiprows=10
)
conv.columns = ["channel", "orders_mobile_app", "orders_website",
                "orders_mobile_web", "orders_pos", "orders_call_center"]
conv = conv[conv["channel"] != "Marketing Channel"].copy()
conv = conv.dropna(subset=["channel"])
conv["channel"] = conv["channel"].str.strip()
conv = conv.reset_index(drop=True)

print("attr:", attr.shape)
print("lc:  ", lc.shape)
print("perf:", perf.shape)
print("conv:", conv.shape)

# ── BUILD MASTER TABLE ────────────────────────────────────────────────────────
master = attr.merge(lc, on="channel", how="left") \
             .merge(perf, on="channel", how="left") \
             .merge(conv, on="channel", how="left")

print("Master table:", master.shape)
print(master.columns.tolist())

# ── DERIVED VARIABLES ─────────────────────────────────────────────────────────

# Attribution shift metrics
master["delta_alg_vs_last"]        = master["algorithmic_30d"] - master["last_touch_30d"]
master["delta_linear_vs_last"]     = master["linear_30d"]      - master["last_touch_30d"]
master["pct_delta_alg_vs_last"]    = master["delta_alg_vs_last"]    / master["last_touch_30d"]
master["pct_delta_linear_vs_last"] = master["delta_linear_vs_last"] / master["last_touch_30d"]

# Business context
master["revenue_per_order"]             = master["total_revenue"] / master["orders_last_touch_30d"]
master["order_share_pct"]               = master["last_touch_30d"] / master["last_touch_30d"].sum() * 100
master["attribution_sensitivity_score"] = master["pct_delta_alg_vs_last"].abs()

print("Master table with variables:", master.shape)

# ── CLASSIFICATION ────────────────────────────────────────────────────────────
def classify_channel(pct):
    if pct >= 0.10:     return "Gainer"
    elif pct <= -0.10:  return "Loser"
    else:               return "Stable"

master["attribution_class"] = master["pct_delta_alg_vs_last"].apply(classify_channel)

# Sort by pct_delta descending (biggest gainers first)
master = master.sort_values("pct_delta_alg_vs_last", ascending=False).reset_index(drop=True)

print("\nClassification results:")
print(master[["channel", "pct_delta_alg_vs_last", "attribution_class"]].to_string(index=False))

# ── EXPORT ────────────────────────────────────────────────────────────────────
master.to_csv("../Data-output/data/master_channel_table.csv", index=False)
print("\nMaster table saved to Data-output/data/")