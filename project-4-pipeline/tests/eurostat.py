import requests
import json

# Eurostat API - Road freight total by country
# Dataset: road_go_ta_tott

url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_go_ta_tott"

params = {
	'format': 'JSON',
	'lang': 'EN',
	'freq': 'A',
	'unit': 'MIO_TKM',
	'tra_type': 'TOTAL',
	'tra_oper': 'TOTAL', 
	'sinceTimePeriod': '2018'
}

response = requests.get(url, params=params)
print('Status code:', response.status_code)

if response.status_code == 200:
	data = response.json()
	print('Top level keys:', list(data.keys()))
	print('\nDimension keys:', list(data['dimension'].keys()))
	print('\nSize:', data['size'])
else:
	print('Error:', response.text[:500])


geo_dim = data['dimension']['geo']['category']
time_dim = data['dimension']['time']['category']

print('Countries available:')
for code, label in geo_dim['label'].items():
	print(f'	{code}: {label}')

print(f'\nYears available:')
for code, label in time_dim['label'].items():
	print(f'	{code}: {label}')

print(f'\nTotal value entries: {len(data["value"])}')
print(f'Sample values (first 5):')

items = list(data['value'].items())[:5]
for k, v in items:
	print(f' index {k}: {v}')