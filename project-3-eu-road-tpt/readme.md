# EU Road Freight Transport Analysis

## Post-COVID Recovery and Country-Level Performance (2019–2024)

## Overview

This project uses Python to explore EU road freight transport performance across
31 countries from 2015 to 2024, with an extended analysis back to 2010 for
country-level comparisons. The central question is: **how has EU road freight
recovered from COVID-19 disruption, and which countries are driving growth or
decline?**

The analysis identifies a clear east-west structural divide, investigates the
drivers of Poland's dominant position, and works through a methodological case
study on the importance of baseline selection in growth rate analysis.

---

## Dataset

**Eurostat Road Freight Transport Statistics — `road_go_ta_tott`**  
Source: [Eurostat Data Browser](https://ec.europa.eu/eurostat/databrowser/view/road_go_ta_tott)

Annual road freight transport data collected from national surveys across EU
member states and selected non-EU countries. Data is reported in multiple units
and transport operation types.

| Field       | Description                                               |
| ----------- | --------------------------------------------------------- |
| geo         | Country or EU aggregate                                   |
| TIME_PERIOD | Reference year                                            |
| tra_type    | Transport operator type (hire/reward, own account, total) |
| tra_oper    | Transport operation (national, international, total)      |
| unit        | Measurement unit (TKM, VKM, thousand tonnes)              |
| OBS_VALUE   | Observed value                                            |

**Filters applied:**

- Transport type: Total
- Transport operation: Total — all movements
- Unit: Million tonne-kilometres (TKM)
- Primary analysis: 2019–2024 (31 countries)
- Extended analysis: 2010–2024 (country-level peer comparison)

Raw dataset: 73,212 rows | Filtered dataset: 176 rows (31 countries, 6 years)

---

## Tools

- **Python 3.13** — analysis environment
- **pandas** — data loading, filtering, transformation
- **matplotlib / seaborn** — visualisation
- **JupyterLab** — notebook authoring

---

## Methodology

Analysis was structured around four analytical questions, each addressed in a
dedicated notebook section with supporting code, visualisation, and narrative
commentary.

The approach follows a standard EDA pattern:

1. Load and inspect raw structure
2. Filter and clean to analytical scope
3. Explore dimensions and distributions
4. Build visualisations around specific questions
5. Investigate anomalies before drawing conclusions

A key methodological decision — extending the peer comparison baseline from
2019 to 2010 — materially changed one finding and is documented explicitly
as an analytical case study.

---

## Key Findings

### 1. The 2021-2022 Surge Was the Anomaly, Not the 2023 Contraction

EU-27 road freight grew steadily from 1,614,870M TKM in 2015 to 1,813,524M TKM
in 2019 — a 12% expansion over four years. COVID-19 caused a surprisingly
modest 0.8% decline in 2020, followed by an exceptional demand surge in
2021-2022 that pushed volumes 6% above the pre-COVID trend.

The 2023 contraction (-3.2%) and 2024 stabilisation (+0.6%) represent
normalisation toward the long-run trend rather than structural decline.
The pandemic itself caused less lasting damage to freight volumes than
the post-2022 macroeconomic environment.

### 2. Poland Leads EU Road Freight by a Structural, Long-Run Margin

In 2024, Poland (368,314M TKM) exceeded Germany (280,840M TKM) by 31% —
a gap that has widened consistently since at least 2010. Indexed to 2010,
Poland reached 182.1 by 2024 while Germany declined to 88.3.

The Ukraine conflict (February 2022) is a plausible contributing factor
to Poland's relative resilience in 2023, but is not the primary explanation.
Poland's dominance predates the invasion by over a decade and reflects
structural competitive advantages: geographic position as the primary
east-west transit corridor, lower operating costs, and fleet scale.

### 3. A Clear East-West Performance Divide Has Emerged (2019–2024)

15 of 28 countries recorded net freight declines from 2019 to 2024,
predominantly in western Europe:

**Declining:** Portugal (-25.5%), Luxembourg (-13.8%), Germany (-10.0%),
Slovakia (-10.0%), Slovenia (-9.0%)

**Growing:** Lithuania (+24.7%), Bulgaria (+31.2%), Croatia (+14.8%),
Italy (+10.6%), Romania (+10.3%)

The divide broadly follows a west-east axis, consistent with lower operating
costs in eastern member states, supply chain nearshoring post-COVID, and
growing intra-EU trade flows through central European corridors.

### 4. Baseline Selection Matters: The Czechia Case Study

Initial analysis flagged Czechia's +80.1% growth (2019-2024) as a potential
reporting anomaly — a near-doubling during COVID while peers contracted seemed
implausible.

Extending the peer comparison to 2010 revealed the correct interpretation:

| Year | Austria | Czechia  | Hungary | Poland | Slovakia |
| ---- | ------- | -------- | ------- | ------ | -------- |
| 2010 | 100.0   | 100.0    | 100.0   | 100.0  | 100.0    |
| 2015 | 88.8    | 113.3    | 113.7   | 128.9  | 121.6    |
| 2019 | 92.3    | **75.4** | 109.6   | 172.5  | 123.1    |
| 2024 | 88.3    | 135.7    | 101.5   | 182.1  | 110.8    |

Czechia's 2019 baseline was a trough — the country had lost significant
freight share between 2015 and 2019, likely due to competitive displacement
by lower-cost Polish and Slovak operators. Post-2020 growth reflects genuine
recovery of lost share, not a statistical anomaly.

**The lesson:** baseline selection materially affects conclusions. The initial
anomaly flag, the investigation, and the revised finding are documented in
full as an example of analytical process.

---

## Charts

| Chart                        | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| `chart1_eu_trend.png`        | EU-27 freight performance 2019–2024 with annotated values    |
| `chart2_top10_2024.png`      | Top 10 countries by freight volume in 2024                   |
| `chart3_growth_rates.png`    | Growth rates by country 2019–2024, colour coded by direction |
| `chart4_poland_vs_peers.png` | Poland vs Germany, France, Spain time series 2019–2024       |
| `chart5_eu_longrun.png`      | EU-27 long-run trend 2015–2024 with event markers            |
| `chart6_czechia_peers.png`   | Czechia vs regional peers indexed to 2010 = 100              |

---

## Repository Structure

```
project-3-eu-road-tpt/
├── README.md
├── eu_road_freight_analysis.ipynb  ← Full annotated analysis notebook
├── dataset/
│   └── road_go_ta_tott_linear.csv  ← Raw Eurostat download
└── charts/
    ├── chart1_eu_trend.png
    ├── chart2_top10_2024.png
    ├── chart3_growth_rates.png
    ├── chart4_poland_vs_peers.png
    ├── chart5_eu_longrun.png
    └── chart6_czechia_peers.png
```

---

## Limitations and Further Work

- **Unit choice:** Analysis uses tonne-kilometres (TKM) rather than tonnes —
  TKM captures both volume and distance, but may overstate the role of
  long-haul transit countries (Poland, Lithuania) relative to domestic-focused
  economies
- **Czechia 2015-2019 decline:** The drivers of Czechia's freight share loss
  are not explained by this dataset alone — further investigation using
  operator-level or commodity-level data would be needed
- **Non-EU countries:** Norway, Switzerland, Montenegro, and North Macedonia
  are included in the dataset but excluded from the east-west divide analysis
  as non-EU members
- **2024 data:** Provisional in some countries — figures may be revised in
  subsequent Eurostat releases

---

## About This Project

This notebook was completed as part of a data analyst portfolio. The dataset
was chosen to apply Python EDA techniques to a recent, real-world logistics
context — directly relevant to a background in operations and supply chain
coordination. The Czechia case study was not planned; it emerged from the
data and is documented in full as an example of analytical process over
clean results.
