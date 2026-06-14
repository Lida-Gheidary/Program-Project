import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ── STYLE ─────────────────────────────────────────────────────────────────────
COLORS = {
    "Gainer":  "#3B8A7F",
    "Loser":   "#c04657",
    "Stable":  "#5c5850",
    "neutral": "#7a7266",
    "grid":    "#dcd9d5",
    "bg":      "#f5f3ef",
    "text":    "#28251d",
}

plt.rcParams.update({
    "font.family":       "Inter",
    "axes.facecolor":    COLORS["bg"],
    "figure.facecolor":  COLORS["bg"],
    "axes.edgecolor":    COLORS["grid"],
    "grid.color":        COLORS["grid"],
    "text.color":        COLORS["text"],
    "axes.labelcolor":   COLORS["text"],
    "xtick.color":       COLORS["text"],
    "ytick.color":       COLORS["text"],
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

OUTPUT = "../Data-output/charts/"
import os; os.makedirs(OUTPUT, exist_ok=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
master   = pd.read_csv("../Data-output/data/master_channel_table.csv")
conv_pct = pd.read_csv("../Data-output/data/conversion_context.csv")

print("Loaded:", master.shape, conv_pct.shape)
print(master.columns.tolist())

# ── CHART 2: Acquisition vs Closure rate by channel ──────────────────────────
import matplotlib.ticker as mtick

df2 = master.sort_values(["attribution_class", "acquisition_rate"], ascending=[True, False])

x = np.arange(len(df2))
w = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - w/2, df2["acquisition_rate"] * 100, width=w, color=COLORS["Gainer"], label="Acquisition Rate")
ax.bar(x + w/2, df2["closure_rate"] * 100,     width=w, color=COLORS["Loser"],   label="Closure Rate")

ax.set_xticks(x)
ax.set_xticklabels(df2["channel"], rotation=35, ha="right", fontsize=9)
ax.set_ylabel("Rate (%)", labelpad=10)
ax.set_title("Acquisition vs Closure Rate by Channel\nWhat role does each channel play in the customer journey?",
             fontsize=13, fontweight="bold", pad=16, loc="left")
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))
ax.grid(axis="y", linewidth=0.5)
ax.set_axisbelow(True)
ax.legend(framealpha=0, fontsize=9)

classes = df2["attribution_class"].values
for i in range(1, len(classes)):
    if classes[i] != classes[i-1]:
        ax.axvline(i - 0.5, color=COLORS["grid"], linewidth=1.2, linestyle="--")

plt.tight_layout()
plt.savefig(OUTPUT + "chart2_lifecycle_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved.")  

# ── CHART 3: Conversion environment stacked bar ──────────────────────────────
env_cols   = ["orders_mobile_app", "orders_website", "orders_mobile_web",
              "orders_pos", "orders_call_center"]
env_labels = ["Mobile App", "Website", "Mobile Web", "POS", "Call Center"]
env_colors = ["#3B8A7F", "#5c8a6e", "#7a7266", "#a89880", "#c04657"]

df3 = conv_pct.set_index("channel")[env_cols]
df3 = df3.loc[master.sort_values("pct_delta_alg_vs_last", ascending=True)["channel"]]

fig, ax = plt.subplots(figsize=(12, 8))
left = np.zeros(len(df3))

for col, label, color in zip(env_cols, env_labels, env_colors):
    ax.barh(df3.index, df3[col], left=left, color=color, label=label, height=0.6)
    left += df3[col].values

ax.set_xlabel("% of Orders by Conversion Environment", labelpad=10)
ax.set_title("Conversion Environment by Channel\nWhere do orders actually close?",
             fontsize=13, fontweight="bold", pad=16, loc="left")
ax.set_xlim(0, 100)
ax.grid(axis="x", linewidth=0.5)
ax.set_axisbelow(True)
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", framealpha=0, fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT + "chart3_conversion_environment.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved.")