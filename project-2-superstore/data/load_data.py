import pandas as pd
from sqlalchemy import create_engine, text
import os

# Connect to MySQL
engine = create_engine('mysql+pymysql://root:portfolio123@127.0.0.1:3306/mysql')

# Create superstore database
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS superstore"))
    conn.commit()

# Reconnect to superstore database
engine = create_engine('mysql+pymysql://root:portfolio123@127.0.0.1:3306/superstore')

# Dataset path
dataset_path = r'c:\dev\portfolio\project-2-superstore\dataset'

# Find the CSV file
csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
print(f'Found: {csv_files}')

# Load it
filepath = os.path.join(dataset_path, csv_files[0])
df = pd.read_csv(filepath, encoding='latin1')
print(f'Loaded {len(df)} rows, {len(df.columns)} columns')
print(f'Columns: {list(df.columns)}')

df.to_sql('orders', engine, if_exists='replace', index=False)
print('Done.')