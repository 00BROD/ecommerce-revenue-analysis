-- COHORT RETENTION — by signup month, what % of customers place an order in
-- month-offset 0..5 after signup. Classic retention triangle via date math + window.

WITH cohort AS (
    SELECT customer_id,
           strftime('%Y-%m', signup_date) AS cohort_month,
           signup_date
    FROM customers
),
activity AS (
    SELECT
        co.cohort_month,
        co.customer_id,
        CAST((julianday(strftime('%Y-%m-01', o.order_date))
              - julianday(strftime('%Y-%m-01', co.signup_date))) / 30.4 AS INT) AS month_offset
    FROM cohort co
    JOIN orders o ON o.customer_id = co.customer_id
    WHERE o.order_date >= co.signup_date
),
sizes AS (
    SELECT cohort_month, COUNT(*) AS cohort_size
    FROM cohort GROUP BY cohort_month
)
SELECT
    a.cohort_month,
    s.cohort_size,
    a.month_offset,
    COUNT(DISTINCT a.customer_id)                                          AS active,
    ROUND(100.0 * COUNT(DISTINCT a.customer_id) / s.cohort_size, 1)        AS retention_pct
FROM activity a
JOIN sizes s ON s.cohort_month = a.cohort_month
WHERE a.month_offset BETWEEN 0 AND 5
GROUP BY a.cohort_month, a.month_offset
ORDER BY a.cohort_month, a.month_offset;
