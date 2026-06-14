import pandas as pd
import sqlite3
import os

OUTPUT_DATA = "../Data-output/data/"
OUTPUT_SQL  = "../SQL/"
os.makedirs(OUTPUT_SQL, exist_ok=True)

# ── LOAD CLEANED DATA ─────────────────────────────────────────────────────────
master   = pd.read_csv(OUTPUT_DATA + "master_channel_table.csv")
conv_pct = pd.read_csv(OUTPUT_DATA + "conversion_context.csv")

# ── CREATE IN-MEMORY SQLITE DATABASE ─────────────────────────────────────────
con = sqlite3.connect(":memory:")

master.to_sql("channels", con, index=False, if_exists="replace")
conv_pct.to_sql("conversion_env", con, index=False, if_exists="replace")

print("Tables loaded into SQLite:")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con)
print(tables.to_string(index=False))
print("\nchannels columns:")
print(pd.read_sql("PRAGMA table_info(channels)", con)[["name","type"]].to_string(index=False))

# ── QUERY 1: Rank channels by algorithmic uplift over last-touch ──────────────
q1 = pd.read_sql("""
    SELECT
        channel,
        attribution_class,
        ROUND(last_touch_30d, 2)       AS last_touch,
        ROUND(algorithmic_30d, 2)      AS algorithmic,
        ROUND(delta_alg_vs_last, 2)    AS delta,
        ROUND(pct_delta_alg_vs_last, 4) AS pct_delta
    FROM channels
    ORDER BY pct_delta_alg_vs_last DESC
""", con)
print("\nQuery 1 — Channel ranking by algorithmic uplift:")
print(q1.to_string(index=False))
q1.to_csv(OUTPUT_SQL + "q1_attribution_ranking.csv", index=False)

# ── QUERY 2: Lifecycle index joined to attribution delta ──────────────────────
q2 = pd.read_sql("""
    SELECT
        channel,
        attribution_class,
        ROUND(lifecycle_index, 4)          AS lifecycle_index,
        ROUND(pct_delta_alg_vs_last, 4)    AS pct_delta,
        CASE
            WHEN lifecycle_index > 0.005  THEN 'Acquisition-oriented'
            WHEN lifecycle_index < -0.005 THEN 'Closure-oriented'
            ELSE 'Neutral'
        END AS lifecycle_role
    FROM channels
    ORDER BY lifecycle_index DESC
""", con)
print("\nQuery 2 — Lifecycle role vs attribution delta:")
print(q2.to_string(index=False))
q2.to_csv(OUTPUT_SQL + "q2_lifecycle_vs_delta.csv", index=False)

# ── QUERY 3: Conversion environment dependence by channel ─────────────────────
q3 = pd.read_sql("""
    SELECT
        c.channel,
        c.attribution_class,
        ROUND(e.orders_mobile_app, 1)    AS mobile_app_pct,
        ROUND(e.orders_website, 1)       AS website_pct,
        ROUND(e.orders_call_center, 1)   AS call_center_pct,
        ROUND(e.orders_pos, 1)           AS pos_pct,
        e.top_env,
        e.top_env_share
    FROM channels c
    JOIN conversion_env e ON c.channel = e.channel
    ORDER BY c.pct_delta_alg_vs_last DESC
""", con)
print("\nQuery 3 — Conversion environment by channel:")
print(q3.to_string(index=False))
q3.to_csv(OUTPUT_SQL + "q3_conversion_dependence.csv", index=False)

# ── QUERY 4: High revenue but low algorithmic gain (and vice versa) ───────────
q4 = pd.read_sql("""
    SELECT
        channel,
        attribution_class,
        ROUND(total_revenue, 0)            AS total_revenue,
        ROUND(pct_delta_alg_vs_last, 4)    AS pct_delta,
        ROUND(revenue_per_order, 2)        AS revenue_per_order,
        CASE
            WHEN total_revenue > 500000 AND pct_delta_alg_vs_last < 0
                THEN 'High revenue, over-credited by last-touch'
            WHEN total_revenue < 200000 AND pct_delta_alg_vs_last > 0.005
                THEN 'Low revenue, under-credited by last-touch'
            WHEN total_revenue > 500000 AND pct_delta_alg_vs_last > 0.005
                THEN 'High revenue, under-credited by last-touch'
            ELSE 'Neutral'
        END AS business_interpretation
    FROM channels
    ORDER BY total_revenue DESC
""", con)
print("\nQuery 4 — Revenue vs attribution shift:")
print(q4.to_string(index=False))
q4.to_csv(OUTPUT_SQL + "q4_revenue_vs_attribution.csv", index=False)

print("\nAll SQL queries saved to SQL folder.")
con.close()