import requests
import pandas as pd
import logging
import argparse
import os
from pathlib import Path
from datetime import datetime

# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output'
LOG_DIR = BASE_DIR / 'logs'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ============================================================
# Logging setup
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# World Bank LPI extractor
# ============================================================

def fetch_world_bank_lpi(years: list) -> pd.DataFrame:
    """
    Fetch Logistics Performance Index scores from World Bank API.
    Returns country-level LPI scores for specified years.
    LPI is published every 2-3 years — available years: 2010, 2012, 2014, 2016, 2018, 2022.
    """
    logger.info('Fetching World Bank LPI data...')

    date_range = f"{min(years)}:{max(years)}"
    url = "https://api.worldbank.org/v2/country/all/indicator/LP.LPI.OVRL.XQ"
    all_records = []
    page = 1

    while True:
        params = {
            'format': 'json',
            'date': date_range,
            'per_page': 500,
            'page': page
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        metadata = data[0]
        records = data[1]
        all_records.extend(records)

        logger.info(f'  Page {page}/{metadata["pages"]} fetched ({len(records)} records)')

        if page >= metadata['pages']:
            break
        page += 1

    # Parse into dataframe
    df = pd.DataFrame([{
        'country_name': r['country']['value'],
        'iso3': r['countryiso3code'],
        'year': int(r['date']),
        'lpi_score': r['value']
    } for r in all_records])

    # Filter to valid country-level data only
    df = df[df['lpi_score'].notna()]
    df = df[df['year'].isin(years)]

    # Exclude regional aggregates (iso3 codes that are not 3 uppercase letters)
    df = df[df['iso3'].str.match(r'^[A-Z]{3}$')]

    logger.info(f'World Bank LPI: {len(df)} valid records across {df["iso3"].nunique()} countries')
    return df


# ============================================================
# Eurostat road freight extractor
# ============================================================

def fetch_eurostat_freight(years: list) -> pd.DataFrame:
    """
    Fetch road freight transport volumes from Eurostat API.
    Returns country-level TKM values for specified years.
    Dataset: road_go_ta_tott
    """
    logger.info('Fetching Eurostat road freight data...')

    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_go_ta_tott"
    params = {
        'format': 'JSON',
        'lang': 'EN',
        'freq': 'A',
        'unit': 'MIO_TKM',
        'tra_type': 'TOTAL',
        'tra_oper': 'TOTAL',
        'sinceTimePeriod': str(min(years))
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Decode JSON-stat format
    geo_labels = data['dimension']['geo']['category']['label']
    geo_index = data['dimension']['geo']['category']['index']
    time_labels = data['dimension']['time']['category']['label']
    time_index = data['dimension']['time']['category']['index']

    n_geo = len(geo_index)
    n_time = len(time_index)

    geo_by_pos = {v: k for k, v in geo_index.items()}
    time_by_pos = {v: k for k, v in time_index.items()}

    records = []
    for str_idx, value in data['value'].items():
        idx = int(str_idx)
        geo_pos = idx // n_time
        time_pos = idx % n_time

        geo_code = geo_by_pos[geo_pos]
        year = int(time_by_pos[time_pos])

        if year in years:
            records.append({
                'geo_code': geo_code,
                'country_name_eurostat': geo_labels[geo_code],
                'year': year,
                'tkm_millions': value
            })

    df = pd.DataFrame(records)

    # Exclude EU aggregates
    eu_aggregates = ['EU27_2020', 'EU28', 'EU27_2007', 'EU25', 'EU15']
    df = df[~df['geo_code'].isin(eu_aggregates)]

    logger.info(f'Eurostat freight: {len(df)} valid records across {df["geo_code"].nunique()} countries')
    return df


# ============================================================
# Eurostat modal split extractor
# ============================================================

def fetch_eurostat_modal_split(years: list) -> pd.DataFrame:
    """
    Fetch inland freight modal split from Eurostat API.
    Returns road, rail, and inland waterway percentage shares per country.
    Dataset: tran_hv_frmod
    Note: Maritime and air are excluded — this dataset covers inland modes only.
    """
    logger.info('Fetching Eurostat modal split data...')

    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tran_hv_frmod"
    params = {
        'format': 'JSON',
        'lang': 'EN',
        'freq': 'A',
        'unit': 'PC',
        'sinceTimePeriod': str(min(years))
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Decode JSON-stat format
    geo_labels = data['dimension']['geo']['category']['label']
    geo_index = data['dimension']['geo']['category']['index']
    time_labels = data['dimension']['time']['category']['label']
    time_index = data['dimension']['time']['category']['index']
    mode_labels = data['dimension']['tra_mode']['category']['label']
    mode_index = data['dimension']['tra_mode']['category']['index']

    n_geo = len(geo_index)
    n_time = len(time_index)
    n_mode = len(mode_index)

    geo_by_pos = {v: k for k, v in geo_index.items()}
    time_by_pos = {v: k for k, v in time_index.items()}
    mode_by_pos = {v: k for k, v in mode_index.items()}

    records = []
    for str_idx, value in data['value'].items():
        idx = int(str_idx)
        mode_pos = idx // (n_geo * n_time)
        remainder = idx % (n_geo * n_time)
        geo_pos = remainder // n_time
        time_pos = remainder % n_time

        geo_code = geo_by_pos.get(geo_pos)
        year = int(time_by_pos.get(time_pos, 0))
        mode_code = mode_by_pos.get(mode_pos)

        if geo_code and year in years and mode_code in ['ROAD', 'RAIL', 'IWW']:
            records.append({
                'geo_code': geo_code,
                'year': year,
                'mode': mode_code,
                'share_pct': value
            })

    df = pd.DataFrame(records)

    # Exclude EU aggregate
    df = df[df['geo_code'] != 'EU27_2020']

    # Pivot to wide format — one row per country/year
    df_wide = df.pivot_table(
        index=['geo_code', 'year'],
        columns='mode',
        values='share_pct'
    ).reset_index()

    df_wide.columns.name = None
    df_wide = df_wide.rename(columns={
        'ROAD': 'road_share_pct',
        'RAIL': 'rail_share_pct',
        'IWW': 'iww_share_pct'
    })

    # Fill missing IWW with 0 for countries with no inland waterways
    if 'iww_share_pct' in df_wide.columns:
        df_wide['iww_share_pct'] = df_wide['iww_share_pct'].fillna(0)
    else:
        df_wide['iww_share_pct'] = 0

    logger.info(f'Modal split: {len(df_wide)} country-year records across {df_wide["geo_code"].nunique()} countries')
    return df_wide


# ============================================================
# Country code mapper
# ============================================================

def build_country_mapping() -> dict:
    """
    Map Eurostat 2-letter codes to ISO3 codes for joining to World Bank data.
    """
    return {
        'AT': 'AUT', 'BE': 'BEL', 'BG': 'BGR', 'HR': 'HRV',
        'CY': 'CYP', 'CZ': 'CZE', 'DK': 'DNK', 'EE': 'EST',
        'FI': 'FIN', 'FR': 'FRA', 'DE': 'DEU', 'EL': 'GRC',
        'HU': 'HUN', 'IE': 'IRL', 'IT': 'ITA', 'LV': 'LVA',
        'LT': 'LTU', 'LU': 'LUX', 'MT': 'MLT', 'NL': 'NLD',
        'PL': 'POL', 'PT': 'PRT', 'RO': 'ROU', 'SK': 'SVK',
        'SI': 'SVN', 'ES': 'ESP', 'SE': 'SWE', 'NO': 'NOR',
        'CH': 'CHE', 'UK': 'GBR', 'ME': 'MNE', 'MK': 'MKD',
        'LI': 'LIE', 'IS': 'ISL', 'TR': 'TUR'
    }


# ============================================================
# Transform and join
# ============================================================

def transform_and_join(df_lpi: pd.DataFrame,
                        df_freight: pd.DataFrame,
                        df_modal: pd.DataFrame,
                        join_year: int) -> pd.DataFrame:
    """
    Join LPI, freight volume, and modal split datasets on country and year.
    Calculates freight volume change from 2018 to join_year.
    """
    logger.info(f'Joining datasets on year {join_year}...')

    code_map = build_country_mapping()

    # Map iso2 to iso3 for freight and modal
    df_freight['iso3'] = df_freight['geo_code'].map(code_map)
    df_modal['iso3'] = df_modal['geo_code'].map(code_map)

    df_freight = df_freight.dropna(subset=['iso3'])
    df_modal = df_modal.dropna(subset=['iso3'])

    # Filter to join year
    lpi_join = df_lpi[df_lpi['year'] == join_year][['iso3', 'country_name', 'lpi_score']]
    freight_join = df_freight[df_freight['year'] == join_year][['iso3', 'tkm_millions']]
    modal_join = df_modal[df_modal['year'] == join_year][['iso3', 'road_share_pct', 'rail_share_pct', 'iww_share_pct']]

    # Freight change from 2018
    freight_2018 = df_freight[df_freight['year'] == 2018][['iso3', 'tkm_millions']].rename(
        columns={'tkm_millions': 'tkm_2018'})
    freight_join = freight_join.merge(freight_2018, on='iso3', how='left')
    freight_join['tkm_change_pct'] = (
        (freight_join['tkm_millions'] - freight_join['tkm_2018']) /
        freight_join['tkm_2018'] * 100
    ).round(2)

    # Join all three datasets
    df_combined = lpi_join.merge(freight_join, on='iso3', how='inner')
    df_combined = df_combined.merge(modal_join, on='iso3', how='left')
    df_combined = df_combined.rename(columns={'tkm_millions': f'tkm_{join_year}'})
    df_combined = df_combined.sort_values('lpi_score', ascending=False)

    # Drop countries with incomplete modal split data
    df_combined = df_combined.dropna(subset=['road_share_pct', 'rail_share_pct'])

    all_countries = set(lpi_join['iso3']) & set(freight_join['iso3'])
    modal_countries = set(modal_join['iso3'])
    missing_modal = all_countries - modal_countries
    logger.info(f'Countries missing modal data: {missing_modal}')

    logger.info(f'After dropping incomplete modal data: {len(df_combined)} countries')

    # Standardise country names
    df_combined['country_name'] = df_combined['country_name'].replace({
        'Slovak Republic': 'Slovakia'
    })

    logger.info(f'Combined dataset: {len(df_combined)} countries matched')
    return df_combined


# ============================================================
# Load — output to CSV
# ============================================================

def load_output(df: pd.DataFrame, label: str) -> Path:
    """
    Save combined dataset to CSV output directory.
    """
    filename = OUTPUT_DIR / f'lpi_freight_{label}_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(filename, index=False)
    logger.info(f'Output saved to: {filename}')
    return filename


# ============================================================
# Summary report
# ============================================================

def generate_summary(df: pd.DataFrame, join_year: int):
    """
    Print a summary report of key findings to console.
    """
    print('\n' + '='*60)
    print('PIPELINE SUMMARY REPORT')
    print(f'LPI vs Road Freight and Modal Split — {join_year}')
    print('='*60)

    print(f'\nCountries in combined dataset: {len(df)}')
    print(f'Average LPI score: {df["lpi_score"].mean():.2f}')
    print(f'Average freight volume: {df[f"tkm_{join_year}"].mean():,.0f}M TKM')

    print('\nTop 5 countries by LPI score:')
    cols = ['country_name', 'lpi_score', f'tkm_{join_year}', 'road_share_pct', 'rail_share_pct']
    print(df[cols].head(5).to_string(index=False))

    print('\nTop 5 countries by freight volume:')
    top_freight = df.nlargest(5, f'tkm_{join_year}')
    print(top_freight[cols].to_string(index=False))

    print('\nHighest rail share (% of inland freight):')
    top_rail = df.nlargest(5, 'rail_share_pct')[['country_name', 'lpi_score', 'rail_share_pct', 'road_share_pct']]
    print(top_rail.to_string(index=False))

    print('\nHighest road dependency (% of inland freight):')
    top_road = df.nlargest(5, 'road_share_pct')[['country_name', 'lpi_score', 'road_share_pct', 'rail_share_pct']]
    print(top_road.to_string(index=False))

    print('\nFreight change 2018 to 2022 (top 5 growers):')
    top_growth = df.nlargest(5, 'tkm_change_pct')[['country_name', 'tkm_change_pct']]
    print(top_growth.to_string(index=False))

    print('\nFreight change 2018 to 2022 (top 5 decliners):')
    top_decline = df.nsmallest(5, 'tkm_change_pct')[['country_name', 'tkm_change_pct']]
    print(top_decline.to_string(index=False))
    print('='*60)


# ============================================================
# Main pipeline
# ============================================================

def run_pipeline(join_year: int = 2022):
    logger.info('='*50)
    logger.info('Starting EU Logistics Pipeline')
    logger.info(f'Join year: {join_year}')
    logger.info('='*50)

    # Extract
    df_lpi = fetch_world_bank_lpi(years=[2018, join_year])
    df_freight = fetch_eurostat_freight(years=[2018, join_year])
    df_modal = fetch_eurostat_modal_split(years=[join_year])

    # Transform and join
    df_combined = transform_and_join(df_lpi, df_freight, df_modal, join_year)

    # Load
    output_path = load_output(df_combined, str(join_year))

    # Report
    generate_summary(df_combined, join_year)

    logger.info('Pipeline completed successfully')
    return df_combined


# ============================================================
# CLI interface
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='EU Logistics Performance and Freight Volume Pipeline'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=2022,
        help='LPI join year (default: 2022, options: 2018, 2022)'
    )
    args = parser.parse_args()
    run_pipeline(join_year=args.year)