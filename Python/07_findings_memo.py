import pandas as pd
import os

OUTPUT_DATA = "../Data-output/data/"
os.makedirs(OUTPUT_DATA, exist_ok=True)

df = pd.read_csv(OUTPUT_DATA + "master_channel_table.csv")

# Select up to five channels per group by relative credit change.
gainers = df[df["attribution_class"] == "Gainer"].copy()
gainers = gainers.sort_values(
    "pct_delta_alg_vs_last", ascending=False
).head(5)
gainers["finding"] = "Higher algorithmic credit"

losers = df[df["attribution_class"] == "Loser"].copy()
losers = losers.sort_values(
    "pct_delta_alg_vs_last", ascending=True
).head(5)
losers["finding"] = "Lower algorithmic credit"

memo = pd.concat([gainers, losers], ignore_index=True)
memo["algorithmic_change_pct"] = (
    memo["pct_delta_alg_vs_last"] * 100
).round(2)

def interpret(row):
    change = row["algorithmic_change_pct"]
    direction = "more" if change > 0 else "less"
    return (
        f"{row['channel']} receives {abs(change):.2f}% {direction} "
        f"attributed order credit under algorithmic attribution than "
        f"under last-touch (30-day lookback). "
        f"Lifecycle index: {row['lifecycle_index']:+.4f}. "
        f"Revenue per last-touch attributed order: "
        f"{row['revenue_per_order']:.2f}."
    )

memo["interpretation"] = memo.apply(interpret, axis=1)

output = memo[[
    "finding", "channel", "attribution_class",
    "last_touch_30d", "algorithmic_30d",
    "algorithmic_change_pct", "lifecycle_index",
    "total_revenue", "revenue_per_order", "interpretation"
]].rename(columns={
    "last_touch_30d": "last_touch_orders",
    "algorithmic_30d": "algorithmic_orders"
})

print("FINDINGS MEMO — Attribution Credit Shifts (30 Days)")
print("Selection: up to five Gainers and five Losers by percentage change.")

for _, row in output.iterrows():
    print(f"\n[{row['finding'].upper()}] {row['channel']}")
    print(f"  Last-touch order credit : {row['last_touch_orders']:,.2f}")
    print(f"  Algorithmic order credit: {row['algorithmic_orders']:,.2f}")
    print(f"  Attribution change      : {row['algorithmic_change_pct']:+.2f}%")
    print(f"  Lifecycle index         : {row['lifecycle_index']:+.4f}")
    print(f"  Total revenue           : {row['total_revenue']:,.2f}")
    print(f"  Revenue per order       : {row['revenue_per_order']:,.2f}")
    print(f"  {row['interpretation']}")

output.to_csv(OUTPUT_DATA + "findings_memo.csv", index=False)
print("\nFindings memo saved to Data-output/data/findings_memo.csv")
print("Revenue currency is not specified in the CSV exports.")