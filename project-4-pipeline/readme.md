# EU Logistics Performance and Freight Modal Analysis

## A Multi-Source Data Pipeline: World Bank API + Eurostat API

## Overview

This project builds a data pipeline that extracts, joins, and analyses data
from two public APIs to compare European country-level logistics quality against
inland freight modal mix and road freight volume.

The central question is: do countries with higher logistics performance scores
use a more balanced modal mix, and do they move more freight? The answer to
both questions is largely no — and the reasons why are analytically interesting.

---

## Pipeline Architecture

```
World Bank API          Eurostat API            Eurostat API
(LPI scores)       +   (Road freight TKM)  +   (Modal split %)
      |                       |                       |
      v                       v                       v
fetch_world_bank_lpi()   fetch_eurostat_freight()   fetch_eurostat_modal_split()
      |                       |                       |
      +----------+------------+-----------+-----------+
                 |
                 v
         transform_and_join()
                 |
                 v
         load_output() --> CSV
                 |
                 v
         generate_summary() --> Console report
```

Three data sources joined on country, producing a single clean dataset of
27 European countries with complete data across all metrics.

---

## Data Sources

| Source         | Dataset         | Description                                                             |
| -------------- | --------------- | ----------------------------------------------------------------------- |
| World Bank API | LP.LPI.OVRL.XQ  | Logistics Performance Index — overall score per country (1=low, 5=high) |
| Eurostat API   | road_go_ta_tott | Annual road freight transport in million tonne-kilometres               |
| Eurostat API   | tran_hv_frmod   | Inland freight modal split — road, rail, and inland waterway shares     |

**Coverage:** 27 European countries, reference year 2022, with 2018 freight
data for change calculation.

**Note on LPI:** The World Bank publishes LPI every 2-3 years. The most recent
available year is 2022. Modal split covers inland modes only — maritime is
excluded as it accounts for 67% of EU freight by tonne-kilometres and
dominates cross-country comparisons.

---

## Tools and Stack

- **Python 3.13** — pipeline and analysis
- **requests** — API extraction
- **pandas** — transformation and joining
- **matplotlib, seaborn** — visualisation
- **JupyterLab** — notebook analysis
- **logging** — pipeline run logging
- **argparse** — CLI interface

---

## Usage

**Run the pipeline:**

```bash
python pipeline.py
```

**Run with a specific join year:**

```bash
python pipeline.py --year 2022
```

**Available join years:** 2018, 2022 (constrained by World Bank LPI publication schedule)

**Output:** CSV file saved to `output/` directory with timestamp. Log file saved to `logs/`.

---

## Repository Structure

```
project-4-pipeline/
├── README.md
├── pipeline.py                 -- ETL pipeline with CLI interface
├── analysis.ipynb              -- Jupyter notebook with charts and findings
├── output/                     -- Generated CSV files (gitignored)
└── logs/                       -- Pipeline run logs (gitignored)
```

---

## Key Findings

### Finding 1: Modal Mix Is Driven by Geography and History, Not Logistics Quality

Inland freight modal split varies dramatically across Europe, from Latvia
(53.2% rail) to Ireland (99.3% road). This variation reflects Soviet-era
rail infrastructure, Alpine geography, and river corridor access rather
than logistics system quality as measured by LPI.

Notable patterns:

- Latvia and Lithuania lead on rail share due to legacy Soviet infrastructure
- Switzerland and Austria use more rail due to Alpine geography
- The Netherlands achieves modal balance through inland waterway (41.1% IWW)
  via the Rhine corridor rather than rail
- Ireland, Greece, and Spain are almost entirely road dependent

### Finding 2: Higher LPI Does Not Predict Greater Rail Usage

The correlation between LPI score and rail share is -0.298 — weak and negative.
High-scoring western European countries have invested in road and port logistics
excellence rather than rail freight capacity. The LPI measures customs efficiency,
infrastructure reliability, tracking technology, and timeliness — qualities that
correlate with economic development, not modal mix.

### Finding 3: Freight Volume and Logistics Quality Are Largely Independent

The correlation between LPI score and freight volume is 0.198 — effectively
no relationship. Two countries illustrate this most clearly:

- **Poland (LPI 3.6, 385,089M TKM)** — highest freight volume at a mid-table
  LPI score, driven by geographic position and cost competitiveness
- **Switzerland (LPI 4.1, 12,988M TKM)** — top LPI tier with one of the lowest
  volumes, reflecting a small, landlocked economy with a highly efficient but
  not large logistics system

Country size, geographic position, and transit role explain freight volume
better than logistics quality scores.

---

## Charts

| Chart                      | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `chart1_lpi_scores.png`    | LPI scores by country with average reference line                 |
| `chart2_modal_split.png`   | Stacked bar chart of road, rail, and IWW shares by country        |
| `chart3_lpi_vs_rail.png`   | Scatter plot of LPI vs rail share, bubble sized by freight volume |
| `chart4_lpi_vs_volume.png` | Scatter plot of LPI vs road freight volume                        |
| `chart5_heatmap.png`       | Normalised heatmap of all metrics across all countries            |

---

## Limitations

- **LPI is published every 2-3 years** — 2022 is the most recent year,
  limiting time-series analysis
- **Cross-sectional only** — with two LPI data points, causal claims
  cannot be supported. Findings describe patterns, not mechanisms
- **Modal split covers inland modes only** — maritime excluded. Countries
  with large port sectors (Netherlands, Belgium) may appear more road-dependent
  than their total freight picture suggests
- **27 countries** — Montenegro excluded due to missing modal split data.
  Cyprus excluded due to missing rail data

---

## About This Project

This project was completed as part of a data analyst portfolio. The pipeline
demonstrates end-to-end data engineering thinking — API extraction,
pagination handling, JSON-stat decoding, multi-source joining, logging,
and CLI interface design — applied to a genuine analytical question in a
logistics and transport context directly relevant to a background in
operations and supply chain coordination.

The finding that logistics quality and freight volume are largely independent
was not the expected result, and is more analytically interesting for it.
