import pandas as pd
import numpy as np
import os

os.makedirs("../Data-output/data", exist_ok=True)

# Load master table
master = pd.read_csv("../Data-output/data/master_channel_table.csv")

print("Loaded:", master.shape)

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

detail["pct_delta_alg_vs_last"] = (detail["pct_delta_alg_vs_last"] * 100).round(1)
detail["lifecycle_index"]       = detail["lifecycle_index"].round(4)
detail["acquisition_rate"]      = (detail["acquisition_rate"] * 100).round(1)
detail["closure_rate"]          = (detail["closure_rate"] * 100).round(1)

print("\nChannel lifecycle detail:")
print(detail.to_string(index=False))

# Save
detail.to_csv("../Data-output/data/lifecycle_correlation.csv", index=False)
print("\nLifecycle correlation saved.")