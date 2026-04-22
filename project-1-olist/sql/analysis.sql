-- ============================================================
-- Olist E-Commerce Delivery Performance Analysis
-- Author: Nate Slater
-- Dataset: Brazilian E-Commerce Public Dataset by Olist
-- Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
-- ============================================================
-- Analytical Questions:
--   1. What is the overall delivery performance of the platform?
--   2. How severe are delays when they occur?
--   3. Which customer regions experience the worst delivery performance?
--   4. Is poor performance driven by sellers or logistics infrastructure?
-- ============================================================


-- ------------------------------------------------------------
-- SECTION 1: DATA ORIENTATION
-- Understand the distribution of order statuses before analysis
-- ------------------------------------------------------------

SELECT
    order_status,
    COUNT(*) as order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Result: 96,478 delivered orders (96.9% of total)
-- Analysis focused on delivered orders with confirmed delivery dates


-- ------------------------------------------------------------
-- SECTION 2: DELIVERY PERFORMANCE — ORDER LEVEL
-- Calculate days variance between estimated and actual delivery
-- Negative = early, Positive = late
-- ------------------------------------------------------------

SELECT
    order_id,
    order_purchase_timestamp,
    order_estimated_delivery_date,
    order_delivered_customer_date,
    DATEDIFF(
        order_delivered_customer_date,
        order_estimated_delivery_date
    ) as days_variance,
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 'On Time'
        ELSE 'Late'
    END as delivery_status
FROM orders
WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
LIMIT 100;


-- ------------------------------------------------------------
-- SECTION 3: HEADLINE KPI METRICS
-- Platform-wide delivery performance summary
-- ------------------------------------------------------------

SELECT
    COUNT(*) as total_orders,
    SUM(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 1 ELSE 0 END) as on_time,
    SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date
        THEN 1 ELSE 0 END) as late,
    ROUND(100.0 * SUM(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 1 ELSE 0 END) / COUNT(*), 2) as on_time_pct,
    ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date)), 1) as avg_days_variance,
    ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 1) as avg_fulfillment_days
FROM orders
WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL;

-- Key findings:
--   91.89% on-time rate across 96,470 delivered orders
--   Average 11.9 days early — estimates are systematically conservative
--   Average fulfillment time: 12.5 days from purchase to delivery
--   Note: Conservative estimating artificially inflates the on-time rate


-- ------------------------------------------------------------
-- SECTION 4: DELAY SEVERITY ANALYSIS
-- Characterise how late orders are when they miss
-- ------------------------------------------------------------

-- 4a. Maximum and average delay for late orders
SELECT
    MAX(DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date)) as max_days_late,
    AVG(DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date)) as avg_days_late
FROM orders
WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
    AND order_delivered_customer_date > order_estimated_delivery_date;

-- Max delay: 188 days (extreme outlier)
-- Average delay when late: 8.87 days


-- 4b. Delay band distribution
SELECT
    CASE
        WHEN DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) <= 3 THEN '1-3 days'
        WHEN DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) <= 7 THEN '4-7 days'
        WHEN DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) <= 14 THEN '8-14 days'
        WHEN DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) <= 30 THEN '15-30 days'
        ELSE '30+ days'
    END as delay_band,
    COUNT(*) as order_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_late_orders
FROM orders
WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
    AND order_delivered_customer_date > order_estimated_delivery_date
GROUP BY delay_band
ORDER BY MIN(DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date));

-- 40.4% of late orders are only 1-3 days late (marginal misses)
-- 63% of late orders are within one week
-- 4.4% (345 orders) are 30+ days late — significant customer impact


-- ------------------------------------------------------------
-- SECTION 5: REGIONAL ANALYSIS — CUSTOMER STATE
-- Identify which states have the worst delivery performance
-- ------------------------------------------------------------

SELECT
    c.customer_state,
    COUNT(*) as total_orders,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) as late_orders,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) / COUNT(*), 2) as late_pct,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) as avg_fulfillment_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY late_pct DESC;

-- Key findings:
--   AL (Alagoas): 23.93% late rate, 24.5 avg fulfillment days
--   SP (São Paulo): 5.89% late rate, 8.7 avg fulfillment days
--   Northeast states consistently underperform — ~4x worse than São Paulo
--   Remote states (RR, AP, AM) have low late rates but extreme fulfillment times
--   suggesting delivery estimates are adjusted for remoteness


-- ------------------------------------------------------------
-- SECTION 6: REGIONAL ANALYSIS — SELLER STATE
-- Determine whether delays originate with sellers or logistics
-- ------------------------------------------------------------

SELECT
    s.seller_state,
    COUNT(DISTINCT oi.seller_id) as seller_count,
    COUNT(*) as total_orders,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) as late_orders,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) / COUNT(*), 2) as late_pct,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) as avg_fulfillment_days
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_state
HAVING total_orders > 100
ORDER BY late_pct DESC;

-- Key findings:
--   Seller states are concentrated in the southeast (SP, RJ, PR, MG)
--   SP sellers: 8.52% late rate despite dominant volume (78,598 orders)
--   Seller late rates are significantly lower than customer state late rates
--   in the same regions — confirming delays accumulate in transit/last mile
--   not at the seller dispatch stage


-- ------------------------------------------------------------
-- SECTION 7: SELLER VS CUSTOMER STATE COMPARISON
-- Side-by-side view confirming logistics as root cause
-- ------------------------------------------------------------

SELECT
    s.seller_state as state,
    'Seller' as state_type,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) / COUNT(*), 2) as late_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_state
HAVING COUNT(*) > 100

UNION ALL

SELECT
    c.customer_state as state,
    'Customer' as state_type,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN 1 ELSE 0 END) / COUNT(*), 2) as late_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
HAVING COUNT(*) > 100
ORDER BY state_type, late_pct DESC;

-- Conclusion:
--   The divergence between seller state and customer state late rates
--   confirms that delivery delays are driven by logistics infrastructure
--   gaps — particularly last-mile delivery capacity in Brazil's northeast —
--   rather than seller dispatch performance.