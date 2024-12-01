import sqlite3
import json

# Connect to SQLite database (it will create a new one if it doesn't exist)
conn = sqlite3.connect('yelp_data.db')
cursor = conn.cursor()

# Create a table for the business data
cursor.execute('''
CREATE TABLE IF NOT EXISTS business (
    business_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude REAL,
    longitude REAL,
    stars REAL,
    review_count INTEGER,
    is_open INTEGER,
    attributes TEXT,
    categories TEXT,
    hours TEXT
)
''')

# Function to load JSON data into SQLite
def load_json_to_sqlite(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO business (
                business_id, name, address, city, state, postal_code, latitude, longitude,
                stars, review_count, is_open, attributes, categories, hours
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['business_id'],
                data['name'],
                data['address'],
                data['city'],
                data['state'],
                data['postal_code'],
                data['latitude'],
                data['longitude'],
                data['stars'],
                data['review_count'],
                data['is_open'],
                json.dumps(data['attributes']) if isinstance(data['attributes'], dict) else str(data['attributes']),
                ','.join(data['categories']) if isinstance(data['categories'], list) else str(data['categories']),
                json.dumps(data['hours']) if isinstance(data['hours'], dict) else str(data['hours'])
            ))
        conn.commit()

# Load the business data into SQLite
load_json_to_sqlite('yelp_academic_dataset_business.json', conn)
print("Data loaded into SQLite.")
