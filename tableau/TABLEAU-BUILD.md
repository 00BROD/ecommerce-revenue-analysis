# Tableau Public dashboard — build guide

Build an executive **"Ecommerce Revenue Overview"** dashboard from `orders_flat.csv`, then publish to Tableau Public. ~30 minutes. No prior workbook needed.

> The data is the same ecommerce dataset as the SQL analysis in this repo — so the dashboard *visually confirms the SQL findings* (discount channel underperforms, revenue concentrates, Q4 seasonality). That coherence is the point.

---

## 0. Setup
1. Download **Tableau Public** (free): https://public.tableau.com/en-us/s/download
2. Create a free Tableau Public account (needed to publish).
3. Open Tableau Public → **Connect → Text file →** select `orders_flat.csv`.
4. On the Data Source tab, confirm types:
   - `order_date`, `signup_date` → **Date**
   - `order_total` → **Number (decimal)**
   - `is_discounted`, `is_first_order`, `months_since_signup` → **Number (whole)**
   - everything else → String.

## 1. Calculated fields
Create these (Analysis → Create Calculated Field):

| Name | Formula |
|---|---|
| `Revenue` | `[Order Total]` *(alias for clarity)* |
| `AOV` | `SUM([Order Total]) / COUNTD([Order Id])` |
| `Customers` | `COUNTD([Customer Id])` |
| `New Customer Revenue` | `SUM(IF [Is First Order] = 1 THEN [Order Total] END)` |
| `Discount Order` | `IF [Is Discounted] = 1 THEN "Discounted" ELSE "Full price" END` |

## 2. Build the sheets

### Sheet 1 — "KPIs" (tiles)
Make four one-number sheets (or use a single sheet w/ Measure Names). Each: drag the measure to **Text**, format big.
- Total Revenue → `SUM(Revenue)`, format currency $#,##0
- Orders → `COUNTD(Order Id)`
- Customers → `Customers`
- AOV → `AOV`, currency

### Sheet 2 — "Revenue by Channel" (bar)  ← the headline
- Columns: `SUM(Revenue)`  ·  Rows: `Acquisition Channel`
- Sort descending. Drag `Acquisition Channel` to **Color**.
- **Manually color `Discount` red**, the rest a single green/teal — mirrors the finding.
- Add `AOV` to **Tooltip** so the AOV gap shows on hover.

### Sheet 3 — "Monthly Revenue Trend" (line)
- Columns: `Order Date` → set to **continuous Month** (right-click → Month, the green one)
- Rows: `SUM(Revenue)`
- You'll see the Q4 spike. Add a trend line (Analytics → Trend Line).

### Sheet 4 — "Cohort Retention" (heatmap)  ← the impressive one
- Columns: `Months Since Signup` (discrete, filter to 0–5)
- Rows: `Cohort Month` (discrete)
- Marks = **Square**. Drag `Customers` to **Color** (use a sequential green palette).
- Label with `Customers`. This is the retention triangle as a heatmap.

### Sheet 5 — "Revenue by Category" (bar or treemap)
- `SUM(Revenue)` by `Category`. Treemap = Marks → Square, Category to Color + Label, Revenue to Size.

## 3. Assemble the dashboard
1. New **Dashboard**, size **1200 × 900** (or Automatic).
2. Layout (drag sheets in):
   ```
   ┌───────────────────────────────────────────┐
   │  Title: Ecommerce Revenue Overview        │
   ├──────────┬──────────┬──────────┬──────────┤
   │ Revenue  │ Orders   │ Customers│  AOV     │   ← KPI tiles
   ├──────────┴──────────┴──────────┴──────────┤
   │ Revenue by Channel   │ Monthly Revenue     │
   ├──────────────────────┼─────────────────────┤
   │ Cohort Retention     │ Revenue by Category │
   └──────────────────────┴─────────────────────┘
   ```
3. Add **filters** (right-click field on a sheet → Show Filter, then Dashboard → "Apply to all using this data source"):
   - `Order Date` (range)  ·  `Acquisition Channel`  ·  `Country`
4. Add a **title** text object: "Ecommerce Revenue Overview" + a one-line subtitle:
   *"Discount channel drives volume but lowest value — see Revenue by Channel."*
5. Tidy: hide gridlines, consistent fonts, dark or light theme (pick one, stay consistent).

## 4. Publish
1. **File → Save to Tableau Public As…** → sign in → name it `Ecommerce Revenue Overview`.
2. It opens in the browser. Copy the public URL.
3. On the Tableau Public viz page, set a clear caption + your name.

## 5. Wire it into the portfolio
Send me the published URL and I will:
- Add a **"Dashboard"** link to your GitHub profile README.
- Link it from this repo's README (so the SQL analysis and the dashboard cross-reference).

---

### Quick-win tips
- If a sheet looks empty, check the date filter isn't excluding everything.
- Keep colors to **two** (a neutral + one accent). Recruiters read restraint as taste.
- The cohort heatmap is the "wow" sheet — make sure it's prominent.
