import pandas as pd
import numpy as np
import os

os.makedirs("../Data-output/data", exist_ok=True)

# Load master table
master = pd.read_csv("../Data-output/data/master_channel_table.csv")

print("Loaded:", master.shape)
# ── CORRELATION: Lifecycle index vs attribution change ──────────────────────
corr_data = master[["lifecycle_index", "pct_delta_alg_vs_last"]].copy()
corr_data = corr_data.replace([np.inf, -np.inf], np.nan).dropna()

if len(corr_data) < 2 or (corr_data.nunique() < 2).any():
    raise ValueError(
        "Correlation requires at least two valid channels "
        "and variation in both variables."
    )

pearson_r = corr_data["lifecycle_index"].corr(
    corr_data["pct_delta_alg_vs_last"]
)

# Correlation of average ranks gives Spearman correlation.
ranked = corr_data.rank(method="average")
spearman_rho = ranked["lifecycle_index"].corr(
    ranked["pct_delta_alg_vs_last"]
)

correlation_summary = pd.DataFrame({
    "method": ["Pearson", "Spearman"],
    "n_channels": [len(corr_data), len(corr_data)],
    "coefficient": [pearson_r, spearman_rho],
    "x_variable": ["lifecycle_index"] * 2,
    "y_variable": ["pct_delta_alg_vs_last"] * 2
})

correlation_summary.to_csv(
    "../Data-output/data/lifecycle_correlation_summary.csv",
    index=False
)

print("\nLifecycle index vs algorithmic attribution change (30 days):")
print(
    correlation_summary[["method", "n_channels", "coefficient"]]
    .round(4).to_string(index=False)
)
print("Descriptive association across channels; this does not establish causation.")

# ── LIFECYCLE INDEX BY CLASS ──────────────────────────────────────────────────
lifecycle_summary = master.groupby("attribution_class")["lifecycle_index"].agg(
    count="count",
    mean="mean",
    min="min",
    max="max"
).round(4)

print("\nLifecycle index by attribution class:")
print(lifecycle_summary.to_string())

# ── CHANNEL DETAIL VIEW ───────────────────────────────────────────────────────
detail = master[["channel", "attribution_class", 
                 "lifecycle_index",
                 "acquisition_rate", 
                 "closure_rate",
                 "pct_delta_alg_vs_last"]].copy()

detail["pct_delta_alg_vs_last"] = (detail["pct_delta_alg_vs_last"] * 100).round(2)
detail["lifecycle_index"]       = detail["lifecycle_index"].round(4)
detail["acquisition_rate"]      = (detail["acquisition_rate"] * 100).round(2)
detail["closure_rate"]          = (detail["closure_rate"] * 100).round(2)

detail = detail.rename(columns={
    "pct_delta_alg_vs_last": "algorithmic_change_pct",
    "acquisition_rate": "acquisition_rate_pct",
    "closure_rate": "closure_rate_pct"
})

print("\nChannel lifecycle detail:")
print(detail.to_string(index=False))

# Save
detail.to_csv("../Data-output/data/lifecycle_correlation.csv", index=False)
print("\nLifecycle correlation saved.")