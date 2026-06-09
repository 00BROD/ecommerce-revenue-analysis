"""
Export a single denormalised, Tableau-friendly CSV from the SQLite DB.
One row per order with all customer dimensions joined + a few derived fields
Tableau can't easily compute on load (cohort month, days-since-signup).
Tableau works best with flat, tall data — this is exactly that shape.
"""
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
con = sqlite3.connect(ROOT / "data" / "ecommerce.db")

df = pd.read_sql_query("""
    SELECT
        o.order_id,
        o.order_date,
        o.order_total,
        o.is_discounted,
        c.customer_id,
        c.acquisition_channel,
        c.country,
        c.signup_date
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
""", con)

# Item-level category (most-expensive line as the order's primary category)
items = pd.read_sql_query("""
    SELECT order_id, category
    FROM order_items oi
    WHERE oi.unit_price = (SELECT MAX(unit_price) FROM order_items x WHERE x.order_id = oi.order_id)
    GROUP BY order_id
""", con)
df = df.merge(items, on="order_id", how="left")
con.close()

df["order_date"] = pd.to_datetime(df["order_date"])
df["signup_date"] = pd.to_datetime(df["signup_date"])
df["cohort_month"] = df["signup_date"].dt.to_period("M").astype(str)
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df["months_since_signup"] = ((df["order_date"].dt.year - df["signup_date"].dt.year) * 12
                             + (df["order_date"].dt.month - df["signup_date"].dt.month))
first_dt = df.groupby("customer_id")["order_date"].transform("min")
df["is_first_order"] = (df["order_date"] == first_dt).astype(int)

cols = ["order_id", "order_date", "order_month", "order_total", "is_discounted",
        "category", "customer_id", "acquisition_channel", "country",
        "signup_date", "cohort_month", "months_since_signup", "is_first_order"]
out = ROOT / "tableau" / "orders_flat.csv"
out.parent.mkdir(exist_ok=True)
df[cols].to_csv(out, index=False)
print(f"rows={len(df):,}  cols={len(cols)}  ->  {out}")
print(df[cols].head().to_string(index=False))
