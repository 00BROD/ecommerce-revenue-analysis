"""Run every SQL file against the SQLite DB, print results, and render charts."""
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "ecommerce.db"
SQL = ROOT / "sql"
CHARTS = ROOT / "charts"

plt.rcParams.update({
    "figure.facecolor": "#0b0f17", "axes.facecolor": "#121826",
    "text.color": "#cbd5e1", "axes.labelcolor": "#cbd5e1",
    "xtick.color": "#94a3b8", "ytick.color": "#94a3b8",
    "axes.edgecolor": "#334155", "font.size": 11,
})
ACCENT = "#6ee7b7"


def q(con, name):
    sql = (SQL / name).read_text()
    df = pd.read_sql_query(sql, con)
    print(f"\n=== {name} ===")
    print(df.to_string(index=False))
    return df


def main():
    con = sqlite3.connect(DB)
    ch = q(con, "01_channel_quality.sql")
    coh = q(con, "02_cohort_retention.sql")
    rfm = q(con, "03_rfm_segmentation.sql")
    par = q(con, "04_revenue_concentration.sql")

    # Chart 1 — channel 90-day value (the headline)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    colors = [ACCENT if c != "Discount" else "#f87171" for c in ch["channel"]]
    ax.bar(ch["channel"], ch["avg_90d_revenue"], color=colors)
    ax.set_title("90-day revenue per customer by acquisition channel", color="#fff")
    ax.set_ylabel("Avg 90-day revenue ($)")
    for i, v in enumerate(ch["avg_90d_revenue"]):
        ax.text(i, v + 1, f"${v:.0f}", ha="center", fontsize=9)
    fig.tight_layout(); fig.savefig(CHARTS / "channel_value.png", dpi=150); plt.close(fig)

    # Chart 2 — retention curves (avg across cohorts)
    avg = coh.groupby("month_offset")["retention_pct"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(avg["month_offset"], avg["retention_pct"], marker="o", color=ACCENT, lw=2)
    ax.set_title("Average cohort retention by month after signup", color="#fff")
    ax.set_xlabel("Months since signup"); ax.set_ylabel("Retention (%)")
    ax.grid(color="#1f2937")
    fig.tight_layout(); fig.savefig(CHARTS / "retention.png", dpi=150); plt.close(fig)

    # Chart 3 — Pareto cumulative revenue
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(par["top_pct_of_customers"], par["cum_pct_of_revenue"], marker="o", color=ACCENT, lw=2)
    ax.axhline(80, ls="--", color="#f87171", lw=1)
    ax.set_title("Revenue concentration (Pareto)", color="#fff")
    ax.set_xlabel("Top % of customers"); ax.set_ylabel("Cumulative % of revenue")
    ax.grid(color="#1f2937")
    fig.tight_layout(); fig.savefig(CHARTS / "pareto.png", dpi=150); plt.close(fig)

    con.close()
    print("\ncharts -> charts/*.png")


if __name__ == "__main__":
    main()
