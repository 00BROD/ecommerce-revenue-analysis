-- RFM SEGMENTATION — score every customer 1-4 on Recency, Frequency, Monetary
-- with NTILE, then bucket into actionable segments. Reference date = latest order.

WITH base AS (
    SELECT
        c.customer_id,
        c.acquisition_channel,
        julianday((SELECT MAX(order_date) FROM orders)) - julianday(MAX(o.order_date)) AS recency_days,
        COUNT(o.order_id)        AS frequency,
        SUM(o.order_total)       AS monetary
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.acquisition_channel
),
scored AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r,   -- lower recency_days = better → score 4
        NTILE(4) OVER (ORDER BY frequency)         AS f,
        NTILE(4) OVER (ORDER BY monetary)          AS m
    FROM base
),
segmented AS (
    SELECT *,
        CASE
            WHEN r >= 3 AND f >= 3 AND m >= 3 THEN 'Champions'
            WHEN r >= 3 AND f >= 2            THEN 'Loyal'
            WHEN r >= 3 AND f = 1            THEN 'New / Promising'
            WHEN r = 2                        THEN 'At Risk'
            ELSE 'Lapsed'
        END AS segment
    FROM scored
)
SELECT
    segment,
    COUNT(*)                                  AS customers,
    ROUND(AVG(monetary), 2)                   AS avg_lifetime_revenue,
    ROUND(SUM(monetary), 0)                   AS total_revenue,
    ROUND(100.0 * SUM(monetary) / (SELECT SUM(monetary) FROM segmented), 1) AS pct_of_revenue
FROM segmented
GROUP BY segment
ORDER BY total_revenue DESC;
