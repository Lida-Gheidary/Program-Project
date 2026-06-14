import pandas as pd
import os

OUTPUT_DATA = "../Data-output/data/"
OUTPUT_SQL  = "../SQL/"
os.makedirs(OUTPUT_DATA, exist_ok=True)

# ── LOAD MASTER TABLE ─────────────────────────────────────────────────────────
df = pd.read_csv(OUTPUT_DATA + "master_channel_table.csv")

# ── TOP UNDERVALUED (Gainers, ranked by pct_delta desc) ──────────────────────
undervalued = df[df["attribution_class"] == "Gainer"].copy()
undervalued = undervalued.sort_values("pct_delta_alg_vs_last", ascending=False).head(5)
undervalued["finding"] = "Undervalued by last-touch"

# ── TOP OVERVALUED (Losers, ranked by pct_delta asc) ─────────────────────────
overvalued = df[df["attribution_class"] == "Loser"].copy()
overvalued = overvalued.sort_values("pct_delta_alg_vs_last", ascending=True).head(5)
overvalued["finding"] = "Overvalued by last-touch"

# ── COMBINE ───────────────────────────────────────────────────────────────────
memo = pd.concat([undervalued, overvalued], ignore_index=True)

memo["interpretation"] = memo.apply(lambda r: (
    f"{r['channel']} gains {r['pct_delta_alg_vs_last']*100:.1f}% more credit under algorithmic attribution. "
    f"Lifecycle role: {r['lifecycle_index']:+.4f}. Revenue per order: {r['revenue_per_order']:.0f} kr."
    if r["finding"] == "Undervalued by last-touch"
    else
    f"{r['channel']} loses {abs(r['pct_delta_alg_vs_last'])*100:.1f}% credit under algorithmic attribution. "
    f"Lifecycle role: {r['lifecycle_index']:+.4f}. Revenue per order: {r['revenue_per_order']:.0f} kr."
), axis=1)

# ── SELECT OUTPUT COLUMNS ─────────────────────────────────────────────────────
output = memo[[
    "finding", "channel", "attribution_class",
    "last_touch_30d", "algorithmic_30d",
    "pct_delta_alg_vs_last", "lifecycle_index",
    "total_revenue", "revenue_per_order",
    "interpretation"
]].rename(columns={
    "last_touch_30d":        "last_touch_orders",
    "algorithmic_30d":       "algorithmic_orders",
    "pct_delta_alg_vs_last": "pct_delta",
})

# ── PRINT ─────────────────────────────────────────────────────────────────────
print("=" * 80)
print("FINDINGS MEMO — Channel Valuation Under Last-Touch vs Algorithmic Attribution")
print("=" * 80)

for _, row in output.iterrows():
    print(f"\n[{row['finding'].upper()}] {row['channel']}")
    print(f"  Last-touch orders : {row['last_touch_orders']:,.0f}")
    print(f"  Algorithmic orders: {row['algorithmic_orders']:,.0f}")
    print(f"  % delta           : {row['pct_delta']*100:+.1f}%")
    print(f"  Lifecycle index   : {row['lifecycle_index']:+.4f}")
    print(f"  Total revenue     : {row['total_revenue']:,.0f} kr")
    print(f"  Revenue per order : {row['revenue_per_order']:,.0f} kr")
    print(f"  → {row['interpretation']}")

# ── SAVE ──────────────────────────────────────────────────────────────────────
output.to_csv(OUTPUT_DATA + "findings_memo.csv", index=False)
print("\nFindings memo saved to Data-output/data/findings_memo.csv")