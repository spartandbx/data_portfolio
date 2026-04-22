import pandas as pd
from sqlalchemy import create_engine
import os

# Connection
engine = create_engine('mysql+pymysql://root:portfolio123@127.0.0.1:3306/olist')

# Dataset Path
dataset_path = r'c:\dev\portfolio\project-1-olist\dataset'

# CSV to table mapping

tables ={
	'olist_customers_dataset.csv': 'customers',
    'olist_geolocation_dataset.csv': 'geolocation',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_order_payments_dataset.csv': 'order_payments',
    'olist_order_reviews_dataset.csv': 'order_reviews',
    'olist_orders_dataset.csv': 'orders',
    'olist_products_dataset.csv': 'products',
    'olist_sellers_dataset.csv': 'sellers',
    'product_category_name_translation.csv': 'product_category_translation',
}

for filename, table_name in tables.items():
	filepath = os.path.join(dataset_path, filename)
	print(f'Loading {filename} -> {table_name}...', end=' ')
	df = pd.read_csv(filepath)
	df.to_sql(table_name, engine, if_exists='replace', index=False)
	print(f'done ({len(df)} rows)')

print('\nAll tables loaded successfully.')