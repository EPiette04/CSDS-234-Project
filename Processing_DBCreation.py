import sqlite3
import json

# Function to create the business table if it doesn't exist
def create_business_table(conn):
    cursor = conn.cursor()
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
    );
    ''')
    conn.commit()

# Function to clean attributes and hours fields before inserting into the database
def clean_json_field(data):
    """Clean specific fields of the data to remove extraneous characters."""
    if isinstance(data, str):
        # Remove any unwanted characters or quotes from strings
        return data.strip(" u'\"")  # Removes spaces, 'u' prefix, and quotes
    elif isinstance(data, dict):
        # Recursively clean dictionaries
        return {key: clean_json_field(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Clean each element in a list
        return [clean_json_field(item) for item in data]
    return data  # Return the data as-is if it's not a string, list, or dict

def prepare_for_insert(data):
    cleaned_attributes = clean_json_field(data.get('attributes', {}))
    cleaned_hours = clean_json_field(data.get('hours', {}))

    # Ensure categories is always a list before joining
    categories = data.get('categories', [])
    if not isinstance(categories, list):  # If categories is not a list, make it one
        categories = [categories] if categories else []

    # Ensure proper JSON format and no extra escaping
    return {
        "business_id": data.get('business_id'),
        "name": data.get('name'),
        "address": data.get('address'),
        "city": data.get('city'),
        "state": data.get('state'),
        "postal_code": data.get('postal_code'),
        "latitude": data.get('latitude'),
        "longitude": data.get('longitude'),
        "stars": data.get('stars'),
        "review_count": data.get('review_count'),
        "is_open": data.get('is_open'),
        "attributes": json.dumps(cleaned_attributes),  # Ensure JSON format
        "categories": ','.join(categories),  # Join the categories list
        "hours": json.dumps(cleaned_hours)  # Ensure JSON format
    }


# Database insertion function with cleaned data
def load_json_to_sqlite(file_path, conn):
    # Create the table if it doesn't exist
    create_business_table(conn)

    with open(file_path, 'r', encoding='utf-8') as file:
        cursor = conn.cursor()
        for line in file:
            data = json.loads(line)
            cleaned_data = prepare_for_insert(data)
            
            # Debugging: Check cleaned data before insertion
            #print(f"Cleaned Data: {cleaned_data}")

            cursor.execute(''' 
            INSERT OR IGNORE INTO business (
                business_id, name, address, city, state, postal_code, latitude, longitude,
                stars, review_count, is_open, attributes, categories, hours
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cleaned_data['business_id'],
                cleaned_data['name'],
                cleaned_data['address'],
                cleaned_data['city'],
                cleaned_data['state'],
                cleaned_data['postal_code'],
                cleaned_data['latitude'],
                cleaned_data['longitude'],
                cleaned_data['stars'],
                cleaned_data['review_count'],
                cleaned_data['is_open'],
                cleaned_data['attributes'],  # Insert cleaned attributes as JSON
                cleaned_data['categories'],
                cleaned_data['hours']  # Insert cleaned hours as JSON
            ))
        conn.commit()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('yelp_data_test5.db')

# Load the business data into SQLite
load_json_to_sqlite('yelp_academic_dataset_business.json', conn)
print("Data loaded into SQLite.")
