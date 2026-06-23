import pandas as pd
import numpy as np
import os

os.makedirs("../Data-output/data", exist_ok=True)

# Load master table
master = pd.read_csv("../Data-output/data/master_channel_table.csv")

print("Loaded:", master.shape)

# ── CONVERSION ENVIRONMENT DISTRIBUTION ──────────────────────────────────────
conv_cols = ["orders_mobile_app", "orders_website", 
             "orders_mobile_web", "orders_pos", "orders_call_center"]

conv_pct = master[["channel", "attribution_class"] + conv_cols].copy()

# Calculate row totals FIRST before modifying anything
row_totals = conv_pct[conv_cols].sum(axis=1)

# Now calculate percentages
for col in conv_cols:
    conv_pct[col] = (conv_pct[col] / row_totals * 100).round(1)

# Add top environment
conv_pct["top_env"] = conv_pct[conv_cols].idxmax(axis=1).str.replace("orders_", "").str.replace("_", " ").str.title()
conv_pct["top_env_share"] = conv_pct[conv_cols].max(axis=1).round(1)

print("\nConversion environment distribution (% of orders):")
print(conv_pct.to_string(index=False))

# Save
conv_pct.to_csv("../Data-output/data/conversion_context.csv", index=False)
print("\nConversion context saved.")

# ── ENVIRONMENT PROFILE BY CLASS ─────────────────────────────────────────────
env_by_class = conv_pct.groupby("attribution_class")[conv_cols].mean().round(1)
print("\nAverage environment distribution by attribution class (%):")
print(env_by_class.to_string())