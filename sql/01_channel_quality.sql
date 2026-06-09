-- HEADLINE ANALYSIS — customer quality by acquisition channel
-- Question: discount acquisition has the lowest CAC, but is it actually profitable?
-- We measure realised value in each customer's first 90 days (a fair, equal window
-- for every cohort regardless of when they signed up).

WITH first_90d AS (
    SELECT
        c.customer_id,
        c.acquisition_channel,
        SUM(o.order_total)                                   AS rev_90d,
        COUNT(o.order_id)                                    AS orders_90d,
        MAX(CASE WHEN o.seq > 1 THEN 1 ELSE 0 END)           AS repeated
    FROM customers c
    JOIN (
        SELECT
            customer_id, order_id, order_total, order_date,
            ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS seq,
            MIN(order_date) OVER (PARTITION BY customer_id)                  AS first_order
        FROM orders
    ) o
      ON o.customer_id = c.customer_id
     AND julianday(o.order_date) - julianday(o.first_order) <= 90
    GROUP BY c.customer_id, c.acquisition_channel
)
SELECT
    acquisition_channel                                  AS channel,
    COUNT(*)                                             AS customers,
    ROUND(AVG(rev_90d), 2)                               AS avg_90d_revenue,
    ROUND(100.0 * AVG(repeated), 1)                      AS repeat_rate_pct,
    ROUND(AVG(orders_90d), 2)                            AS avg_orders,
    ROUND(SUM(rev_90d), 0)                               AS total_90d_revenue
FROM first_90d
GROUP BY acquisition_channel
ORDER BY avg_90d_revenue DESC;
