-- REVENUE CONCENTRATION (Pareto) — how much revenue comes from the top customers.
-- Cumulative running share via window function ordered by customer spend.

WITH cust_rev AS (
    SELECT customer_id, SUM(order_total) AS rev
    FROM orders GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id, rev,
        SUM(rev) OVER (ORDER BY rev DESC ROWS UNBOUNDED PRECEDING) AS cum_rev,
        SUM(rev) OVER ()                                           AS total_rev,
        ROW_NUMBER() OVER (ORDER BY rev DESC)                      AS rn,
        COUNT(*)   OVER ()                                         AS n
    FROM cust_rev
)
SELECT
    decile,
    ROUND(100.0 * MIN(rn) / n, 0)               AS top_pct_of_customers,
    ROUND(100.0 * MAX(cum_rev) / total_rev, 1)  AS cum_pct_of_revenue
FROM (
    SELECT *, NTILE(10) OVER (ORDER BY rev DESC) AS decile FROM ranked
)
GROUP BY decile
ORDER BY decile;
