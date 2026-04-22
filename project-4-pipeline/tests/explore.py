import requests
import json

# World Bank Logistics Performance Index
# Indicator: LP.LPI.OVRL.XQ = Overall LPI index

# Check which LPI years have actual data
url = "https://api.worldbank.org/v2/country/all/indicator/LP.LPI.OVRL.XQ"

params = {
    'format': 'json',
    'date': '2010:2024',
    'per_page': 1000
}

response = requests.get(url, params=params)
data_wb = response.json()

# Collect all records across pages
all_records = data_wb[1]

# Find years with non-null values
import pandas as pd

df_wb = pd.DataFrame([{
    'country': r['country']['value'],
    'iso3': r['countryiso3code'],
    'year': r['date'],
    'lpi_score': r['value']
} for r in all_records])

# Filter to non-null values only
df_wb_valid = df_wb[df_wb['lpi_score'].notna()]

print('Years with LPI data:')
print(df_wb_valid['year'].value_counts().sort_index())

print(f'\nCountries with data in most recent year:')
most_recent = df_wb_valid['year'].max()
print(f'Most recent year: {most_recent}')
print(f'Country count: {len(df_wb_valid[df_wb_valid["year"] == most_recent])}')