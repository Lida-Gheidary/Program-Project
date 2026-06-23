import pandas as pd
import numpy as np
import os

os.makedirs("../Data-output/data", exist_ok=True)

# Load master table built in step 01
master = pd.read_csv("../Data-output/data/master_channel_table.csv")

print("Loaded:", master.shape)
print(master["attribution_class"].value_counts())

# ── RANKING TABLE ─────────────────────────────────────────────────────────────
ranking = master[["channel", "attribution_class",
                  "last_touch_30d", "algorithmic_30d",
                  "delta_alg_vs_last", "pct_delta_alg_vs_last",
                  "revenue_per_order", "order_share_pct"]].copy()

# Round for readability
ranking["pct_delta_alg_vs_last"] = (ranking["pct_delta_alg_vs_last"] * 100).round(1)
ranking["delta_alg_vs_last"]     = ranking["delta_alg_vs_last"].round(0)
ranking["revenue_per_order"]     = ranking["revenue_per_order"].round(0)
ranking["order_share_pct"]       = ranking["order_share_pct"].round(1)

# Rename for clarity
ranking.columns = ["channel", "class", "last_touch_orders",
                   "algorithmic_orders", "delta_orders",
                   "pct_delta", "revenue_per_order", "order_share_pct"]

print(ranking.to_string(index=False))

# ── EXPORT ────────────────────────────────────────────────────────────────────
ranking.to_csv("../Data-output/data/attribution_ranking.csv", index=False)
print("\nRanking table saved to Data-output/data/")

# ── LINEAR VS ALGORITHMIC COMPARISON ─────────────────────────────────────────
model_compare = master[["channel", "attribution_class",
                         "pct_delta_linear_vs_last",
                         "pct_delta_alg_vs_last"]].copy()

model_compare["pct_delta_linear_vs_last"] = (model_compare["pct_delta_linear_vs_last"] * 100).round(1)
model_compare["pct_delta_alg_vs_last"]    = (model_compare["pct_delta_alg_vs_last"] * 100).round(1)

model_compare.columns = ["channel", "class", 
                          "pct_delta_linear", 
                          "pct_delta_algorithmic"]

print("\nModel comparison (% change vs last-touch):")
print(model_compare.to_string(index=False))

# Save
model_compare.to_csv("../Data-output/data/model_comparison.csv", index=False)
print("\nModel comparison saved.")