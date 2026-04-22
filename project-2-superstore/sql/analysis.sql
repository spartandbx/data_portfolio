-- ============================================================
-- Global Superstore Business Performance Analysis
-- Author: [Your Name]
-- Dataset: Global Superstore Dataset
-- Source: https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset
-- ============================================================
-- Analytical Questions:
--   1. Which markets generate the most revenue and profit?
--   2. What is the relationship between discount rate and profitability?
--   3. Which product categories and sub-categories are profitable?
--   4. How have sales and profit trended over the four-year period?
-- ============================================================
-- Note: Dataset loaded as a single denormalised table (superstore.orders)
-- Date fields stored as strings — STR_TO_DATE() used for time series analysis
-- ============================================================


-- ------------------------------------------------------------
-- SECTION 1: DATA ORIENTATION
-- Confirm row count, column structure, and date format
-- ------------------------------------------------------------

-- Row count and basic shape
SELECT COUNT(*) as total_rows
FROM superstore.orders;

-- Sample rows to confirm structure and date format
SELECT `Order Date`, `Ship Date`, Market, Category, Sales, Profit, Discount
FROM superstore.orders
LIMIT 5;

-- Date format confirmed as '%d-%m-%Y' (e.g. 31-07-2012)


-- ------------------------------------------------------------
-- SECTION 2: HEADLINE KPI METRICS
-- Platform-wide business performance summary
-- ------------------------------------------------------------

SELECT
    COUNT(DISTINCT `Order ID`) as total_orders,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(100.0 * SUM(Profit) / SUM(Sales), 2) as overall_margin_pct
FROM superstore.orders;

-- Total orders: 51,290
-- Total sales: ~12.6M
-- Total profit: ~1.47M
-- Overall margin: 11.6%


-- ------------------------------------------------------------
-- SECTION 3: MARKET PERFORMANCE
-- Sales, profit, margin, and average discount by market
-- ------------------------------------------------------------

SELECT
    Market,
    COUNT(DISTINCT `Order ID`) as total_orders,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(100.0 * SUM(Profit) / SUM(Sales), 2) as profit_margin_pct,
    ROUND(AVG(Discount) * 100, 2) as avg_discount_pct
FROM superstore.orders
GROUP BY Market
ORDER BY total_sales DESC;

-- Key findings:
--   APAC leads on sales (3.6M) and profit (436k)
--   Canada: highest margin at 26.6% — zero average discount
--   EMEA: worst margin at 5.45% — highest average discount at 19.61%
--   Discount rate and margin are inversely correlated across markets


-- ------------------------------------------------------------
-- SECTION 4: DISCOUNT IMPACT ANALYSIS
-- Quantify the relationship between discount bands and profitability
-- This is the primary analytical finding of the project
-- ------------------------------------------------------------

SELECT
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.1 THEN '1-10%'
        WHEN Discount <= 0.2 THEN '11-20%'
        WHEN Discount <= 0.3 THEN '21-30%'
        WHEN Discount <= 0.5 THEN '31-50%'
        ELSE '50%+'
    END as discount_band,
    COUNT(*) as order_count,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(100.0 * SUM(Profit) / SUM(Sales), 2) as profit_margin_pct,
    ROUND(AVG(Discount) * 100, 2) as avg_discount_pct
FROM superstore.orders
GROUP BY discount_band
ORDER BY MIN(Discount);

-- Key findings:
--   No discount:  25.32% margin (29,009 orders, 1.77M profit)
--   1-10%:        17.23% margin
--   11-20%:        9.86% margin
--   21-30%:       -5.53% margin — crosses into loss-making
--   31-50%:      -32.39% margin
--   50%+:       -111.02% margin — losing more than order revenue
--   10,361 orders carry discounts above 30%, generating 793k in combined losses
--   Discount ceiling of 20% would eliminate structural loss-making


-- ------------------------------------------------------------
-- SECTION 5: CATEGORY AND SUB-CATEGORY PERFORMANCE
-- Identify profitable and loss-making product segments
-- ------------------------------------------------------------

SELECT
    Category,
    `Sub-Category`,
    COUNT(DISTINCT `Order ID`) as total_orders,
    ROUND(SUM(Sales), 2) as total_sales,
    ROUND(SUM(Profit), 2) as total_profit,
    ROUND(100.0 * SUM(Profit) / SUM(Sales), 2) as profit_margin_pct,
    ROUND(AVG(Discount) * 100, 2) as avg_discount_pct
FROM superstore.orders
GROUP BY Category, `Sub-Category`
ORDER BY profit_margin_pct DESC;

-- Key findings:
--   Paper (Office Supplies): highest margin at 24.2%
--   Copiers (Technology): 17.1% margin, highest absolute profit (258k)
--   All Technology sub-categories are profitable
--   Tables (Furniture): only loss-making sub-category at -8.46% margin
--   Tables average discount of 29.07% directly explains the loss
--   Connects to Section 4 finding — 20%+ discount threshold


-- ------------------------------------------------------------
-- SECTION 6: MONTHLY SALES TREND
-- Four-year time series showing growth and seasonality
-- ------------------------------------------------------------

SELECT
    DATE_FORMAT(STR_TO_DATE(`Order Date`, '%d-%m-%Y'), '%Y-%m') as order_month,
    ROUND(SUM(Sales), 2) as monthly_sales,
    ROUND(SUM(Profit), 2) as monthly_profit,
    ROUND(100.0 * SUM(Profit) / SUM(Sales), 2) as profit_margin_pct
FROM superstore.orders
GROUP BY order_month
ORDER BY order_month;

-- Key findings:
--   Clear upward growth trend 2011-2014
--   Monthly sales grow from ~100-300k (2011) to ~250-550k (2014)
--   Q4 (Oct-Dec) consistently strongest quarter across all years
--   Margin volatility month-to-month reflects uneven discount application
--   No structural margin improvement over the period despite revenue growth


-- ============================================================
-- SUMMARY OF FINDINGS
-- ============================================================
-- 1. Overall margin of 11.6% masks significant variance by market
-- 2. Discount policy is the single strongest predictor of margin:
--    orders above 20% discount are structurally loss-making
-- 3. Tables is the only loss-making sub-category, driven by
--    a 29% average discount rate
-- 4. EMEA underperformance is explained by its 19.61% average
--    discount — the highest of any market
-- 5. Canada's 26.6% margin is explained by zero discounting
-- 6. Revenue is growing consistently but margin is not improving,
--    suggesting discounting is scaling with the business
-- ============================================================