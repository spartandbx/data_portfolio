# Olist Delivery Performance Analysis

## Overview

This project analyses delivery performance across 96,000+ orders on the Olist Brazilian e-commerce platform. The central question is: **where does the platform fail its customers, and why?**

The analysis identifies a clear geographic pattern in delivery failures and traces the root cause to logistics infrastructure gaps rather than seller behaviour: a distinction with significant operational implications.

---

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**  
Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

A real commercial dataset covering orders placed on the Olist marketplace between 2016 and 2018. Contains 9 relational tables spanning orders, customers, sellers, products, payments, and reviews across all Brazilian states.

| Table                        | Rows      | Description                          |
| ---------------------------- | --------- | ------------------------------------ |
| orders                       | 99,441    | Order lifecycle and timestamps       |
| customers                    | 99,441    | Customer location data               |
| order_items                  | 112,650   | Line items linking orders to sellers |
| sellers                      | 3,095     | Seller location data                 |
| order_payments               | 103,886   | Payment method and value             |
| order_reviews                | 99,224    | Customer satisfaction scores         |
| products                     | 32,951    | Product catalogue                    |
| geolocation                  | 1,000,163 | Zip code coordinate mapping          |
| product_category_translation | 71        | Category name translations           |

---

## Tools

- **MySQL 8.0** - data storage and analysis layer
- **Metabase** - dashboard and visualisation
- **Python (pandas, sqlalchemy)** - data loading and preparation
- **Docker** - containerised environment

---

## Methodology

Analysis was scoped to the 96,478 delivered orders with confirmed delivery timestamps (96.9% of total orders). Key metrics calculated for each order:

- **Days variance** - difference between actual and estimated delivery date (negative = early, positive = late)
- **Delivery status** - on time if delivered on or before estimated date
- **Fulfillment time** - days from purchase timestamp to delivery

Regional analysis was conducted at the Brazilian state level for both customer and seller locations, enabling a comparison that isolates whether delays originate at dispatch or in transit.

---

## Key Findings

### 1. Overall Performance Is Strong, But Estimates Are Conservative

- **91.9% on-time rate** across 96,470 delivered orders
- Orders arrive an average of **11.9 days earlier** than the estimated delivery date
- This suggests Olist sets deliberately conservative estimates, which inflates the headline on-time rate
- True fulfillment speed averages **12.5 days** from purchase to delivery

### 2. When Orders Are Late, Delays Are Meaningful

- Average delay when late: **8.9 days**
- 40% of late orders miss by 1-3 days - marginal misses
- 4.4% of late orders (345 orders) are **30+ days late**, representing significant customer experience failures
- Maximum recorded delay: 188 days

### 3. Geographic Inequality Is the Dominant Pattern

- **AL (Alagoas): 23.9% late rate, 24.5 day average fulfillment**
- **SP (São Paulo): 5.9% late rate, 8.7 day average fulfillment**
- Customers in northeastern states face nearly **4x the late rate** of São Paulo customers
- Northeast states (AL, MA, PI, CE, SE, BA) consistently appear at the top of the late rate ranking

### 4. Delays Are a Logistics Problem, Not a Seller Problem

- Seller operations are concentrated in southeastern states (SP, RJ, PR, MG)
- SP sellers post only an **8.5% late rate** despite handling 78,598 orders
- Seller-side late rates are significantly lower than customer-side late rates in equivalent regions
- The divergence confirms delays accumulate **in transit and last-mile delivery**, not at the seller dispatch stage
- Northeast customers are primarily served by southeast sellers — the distance and infrastructure gap is the root cause

---

## Dashboard

The Metabase dashboard presents four views:

1. **Headline KPIs** - total orders, on-time rate, average fulfillment days, total late orders
2. **Delay Band Distribution** - bar chart showing volume of late orders by severity band
3. **Late Rate by Customer State** - ranked bar chart of all 27 Brazilian states
4. **Seller vs Customer State Comparison** - side-by-side late rates confirming logistics as root cause

[Dashboard Screenshot (PDF)](screenshots/dashboard.pdf)

---

## Recommendations

Based on the analysis, three operational recommendations follow:

1. **Recalibrate delivery estimates for northeastern states** - current estimates do not reflect actual delivery times in high-latency regions, creating avoidable late classifications
2. **Prioritise last-mile logistics partnerships in AL, MA, PI, CE** - these states show the highest late rates and longest fulfillment times relative to order volume
3. **Investigate the 345 orders with 30+ day delays** - extreme outliers warrant root cause analysis; they may reflect specific carrier failures, remote delivery challenges, or data quality issues

---

## Repository Structure

```
project-1-olist/
├── README.md
├── sql/
│   └── analysis.sql        ← All analytical queries with commentary
├── data/
│   └── load_data.py        ← CSV to MySQL loading script
└── screenshots/
    └── dashboard.png       ← Metabase dashboard export
```

---

## About This Project

This project was completed as part of a data analyst portfolio, applying SQL and BI tooling to a real-world logistics dataset. The analytical focus on delivery performance and regional inequality, reflects a background in operations and logistics, where understanding the difference between a process failure and an infrastructure constraint has practical significance.
