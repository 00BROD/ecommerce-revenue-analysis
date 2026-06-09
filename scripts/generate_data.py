"""
Generate a realistic synthetic ecommerce dataset and load it into SQLite.

The data has real structure baked in so the analysis surfaces a genuine,
non-obvious business finding rather than noise:

  - Acquisition channel drives very different customer quality. Customers
    acquired on a first-order discount ("Discount") convert cheaply but
    retain and spend far less over 90 days than organically acquired ones.
  - Seasonality (Q4 lift), a Pareto revenue concentration, and realistic
    AOV / order-frequency distributions.

Everything is seeded for reproducibility.
"""
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

RNG = np.random.default_rng(42)
DB = Path(__file__).resolve().parents[1] / "data" / "ecommerce.db"
START = datetime(2024, 1, 1)
DAYS = 540  # ~18 months

CHANNELS = ["Organic", "Paid Search", "Paid Social", "Referral", "Discount"]
CHANNEL_MIX = [0.30, 0.22, 0.20, 0.10, 0.18]

# Per-channel customer quality. Discount: cheap to acquire, poor retention/spend.
QUALITY = {
    "Organic":     dict(repeat=0.55, aov=78, life=210),
    "Referral":    dict(repeat=0.58, aov=82, life=220),
    "Paid Search": dict(repeat=0.42, aov=70, life=150),
    "Paid Social": dict(repeat=0.38, aov=64, life=130),
    "Discount":    dict(repeat=0.22, aov=49, life=70),   # the trap
}
CATEGORIES = ["Apparel", "Home", "Beauty", "Electronics", "Outdoor"]


def seasonal_weight(d: datetime) -> float:
    # Q4 holiday lift + mild summer dip
    m = d.month
    return {11: 1.6, 12: 1.8, 1: 0.8, 7: 0.9, 8: 0.9}.get(m, 1.0)


def main():
    n_customers = 6000
    signup_offsets = RNG.integers(0, DAYS - 90, n_customers)  # leave room for repeat orders
    channels = RNG.choice(CHANNELS, size=n_customers, p=CHANNEL_MIX)

    customers, orders, items = [], [], []
    oid = 1
    for cid in range(1, n_customers + 1):
        ch = channels[cid - 1]
        q = QUALITY[ch]
        signup = START + timedelta(days=int(signup_offsets[cid - 1]))
        customers.append((cid, ch, signup.strftime("%Y-%m-%d"),
                          RNG.choice(["US", "CA", "UK", "AU"], p=[0.6, 0.15, 0.15, 0.1])))

        # First order at signup
        n_orders = 1 + RNG.poisson(q["repeat"] * 2.0)
        last = signup
        for k in range(n_orders):
            if k > 0:
                gap = int(RNG.exponential(q["life"] / 2.5))
                last = last + timedelta(days=max(3, gap))
                if (last - signup).days > q["life"] * 1.8:
                    break
            sw = seasonal_weight(last)
            order_total = 0.0
            n_lines = 1 + RNG.poisson(1.1)
            order_date = last.strftime("%Y-%m-%d")
            for _ in range(n_lines):
                cat = RNG.choice(CATEGORIES)
                price = round(max(8, RNG.normal(q["aov"] / 1.6, q["aov"] / 4)), 2)
                qty = 1 + RNG.poisson(0.5)
                line = round(price * qty * sw, 2)
                order_total += line
                items.append((oid, cat, qty, price))
            # discount-acquired first orders carry a discount flag
            discount = 1 if (ch == "Discount" and k == 0) else int(RNG.random() < 0.12)
            orders.append((oid, cid, order_date, round(order_total, 2), discount))
            oid += 1

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS customers; DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS order_items;
        CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, acquisition_channel TEXT, signup_date TEXT, country TEXT);
        CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, order_total REAL, is_discounted INTEGER);
        CREATE TABLE order_items (order_id INTEGER, category TEXT, quantity INTEGER, unit_price REAL);
        CREATE INDEX idx_orders_cust ON orders(customer_id);
        CREATE INDEX idx_orders_date ON orders(order_date);
    """)
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)
    cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?)", items)
    con.commit()

    print(f"customers={len(customers):,}  orders={len(orders):,}  order_items={len(items):,}")
    print(f"db -> {DB}")
    con.close()


if __name__ == "__main__":
    main()
