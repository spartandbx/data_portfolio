import requests

url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tran_hv_frmod"

params = {
    'format': 'JSON',
    'lang': 'EN',
    'sinceTimePeriod': '2018'
}

response = requests.get(url, params=params, timeout=30)
print('Status code:', response.status_code)

if response.status_code == 200:
    data = response.json()
    print('Top level keys:', list(data.keys()))
    print('Dimensions:', list(data['dimension'].keys()))
    print('Size:', data['size'])
    print('\nUnit values:', list(data['dimension']['unit']['category']['label'].values()))
    print('\nMode values:', list(data['dimension']['vehicle']['category']['label'].values()) 
          if 'vehicle' in data['dimension'] 
          else list(data['dimension'][list(data['dimension'].keys())[2]]['category']['label'].values()))
else:
    print('Error:', response.text[:500])

geo_labels = data['dimension']['geo']['category']['label']
time_labels = data['dimension']['time']['category']['label']
mode_labels = data['dimension']['tra_mode']['category']['label']

print('Countries:')
for code, label in geo_labels.items():
    print(f'  {code}: {label}')

print('\nYears:', list(time_labels.values()))
print('\nModes:', list(mode_labels.keys()))