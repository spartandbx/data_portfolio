# Global Superstore Business Performance Analysis

## Overview

This project analyses four years of sales data across a global retail operation spanning 7 markets and 3 product categories. The central question is: **what is driving profitability variance across markets, products, and customer segments?**

The analysis identifies discount policy as the primary driver of margin erosion, a finding that connects market-level underperformance, category-level losses, and order-level profitability into a single coherent explanation.

---

## Dataset

**Global Superstore Dataset**  
Source: [Kaggle](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)

A retail orders dataset covering 51,290 transactions across 7 global markets between 2011 and 2014. A single denormalised table containing order, customer, product, and financial data.

| Field                     | Description                                         |
| ------------------------- | --------------------------------------------------- |
| Order Date, Ship Date     | Transaction and fulfillment timestamps              |
| Market, Region, Country   | Geographic hierarchy                                |
| Segment                   | Customer segment (Consumer, Corporate, Home Office) |
| Category, Sub-Category    | Product classification                              |
| Sales, Profit, Discount   | Financial metrics                                   |
| Shipping Cost             | Fulfillment cost                                    |
| Ship Mode, Order Priority | Operational fields                                  |

---

## Tools

- **MySQL 8.0** - data storage and analysis layer
- **Metabase** - dashboard and visualisation
- **Python (pandas, sqlalchemy)** - data loading and preparation
- **Docker** - containerised environment

---

## Methodology

Analysis was structured around four analytical questions:

1. Which markets generate the most revenue and profit, and why do margins differ?
2. What is the relationship between discount rate and profitability?
3. Which product categories and sub-categories are profitable, and which are loss-making?
4. How have sales and profit trended over the four-year period?

Financial metrics calculated per order and aggregated by market, category, sub-category, and discount band. Date fields were parsed from raw string format for time series analysis.

---

## Key Findings

### 1. Overall Performance Masks Significant Variance

- Total sales of &#36;12.6M across 51,290 orders at an overall margin of 11.6%
- APAC leads on both revenue (&#36;3.6M) and profit (&#36;436k)
- **Canada posts the highest margin at 26.6%** - driven entirely by a zero-discount policy
- **EMEA posts the worst margin at 5.45%** despite &#36;806k in revenue

### 2. Discount Policy Is the Primary Driver of Profitability

The relationship between discount rate and margin is linear and unambiguous:

| Discount Band | Profit Margin |
| ------------- | ------------- |
| No Discount   | +25.3%        |
| 1–10%         | +17.2%        |
| 11–20%        | +9.9%         |
| 21–30%        | -5.5%         |
| 31–50%        | -32.4%        |
| 50%+          | -111.0%       |

- Orders discounted above 20% are structurally loss-making
- 10,361 orders (20% of total) carry discounts above 30%
- Those orders generated **&#36;793,526 in combined losses**
- The no-discount segment (29,009 orders) generated **&#36;1.77M in profit**

### 3. Tables Is the Only Loss-Making Sub-Category

- Tables generates -8.46% margin on &#36;757k in sales - a &#36;64k loss
- Average discount on Tables orders is 29.07% - directly crossing the unprofitable threshold
- All Technology sub-categories are profitable; Copiers leads at 17.1% margin
- Paper (Office Supplies) posts the best margin in the dataset at 24.2%

### 4. EMEA Underperformance Is Explained by Discount Rate

- EMEA carries the highest average discount of any market at 19.61%
- This places EMEA orders consistently in the margin-erosion zone
- Canada's 0% average discount directly explains its 26.6% margin
- The discount-margin relationship explains market variance better than any other variable

### 5. Clear Growth Trend With Consistent Seasonality

- Monthly sales grow from ~&#36;100–300k in 2011 to ~&#36;250–550k in 2014
- Q4 (October–December) is consistently the strongest quarter across all years
- Margin volatility month-to-month reflects uneven application of discounting

---

## Dashboard

Five views presented in the Metabase dashboard:

1. **Headline KPIs** - total orders, total sales, total profit, overall margin
2. **Profit Margin by Discount Band** - bar chart showing margin collapse above 20% discount
3. **Sales and Profit by Market** - comparative market performance
4. **Profit Margin by Sub-Category** - identifying Tables as the loss-making outlier
5. **Monthly Sales Trend** - four-year time series with seasonality pattern

[View Full Dashboard (PDF)](screenshots/dashboard.pdf)

---

## Recommendations

Three actionable recommendations follow from the analysis:

1. **Implement a discount ceiling of 20%** - orders above this threshold are loss-making without exception. The current policy of allowing 50%+ discounts is destroying margin at scale
2. **Review the Tables pricing and discount strategy** - at 29% average discount and -8.46% margin, Tables requires either a price increase, a discount restriction, or a strategic decision to exit the sub-category
3. **Investigate EMEA discount authorisation** - EMEA's 19.61% average discount is the highest of any market and directly explains its margin underperformance. Tightening discount approval in this market would have the most immediate margin impact

---

## Repository Structure

```
project-2-superstore/
├── README.md
├── sql/
│   └── analysis.sql        ← All analytical queries with commentary
├── data/
│   └── load_data.py        ← CSV to MySQL loading script
└── screenshots/
    └── dashboard.pdf       ← Metabase dashboard export
```

---

## About This Project

This project was completed as part of a data analyst portfolio. The Superstore dataset is a well-known analytical benchmark, the value here is not in the dataset choice but in the analytical framing: identifying a single root cause (discount policy) that explains variance across markets, categories, and order-level profitability simultaneously. This kind of connecting analysis, moving from symptom to cause, reflects the operational thinking developed through a background in logistics and process coordination.
