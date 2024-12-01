import sqlite3

# Function to query POIs based on input criteria
def query_pois(poi_type, keywords, filters, k=5):
    # Connect to the SQLite database (same folder as the script)
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()
    
    # Base query
    query = f'''
    SELECT business_id, name, stars, review_count, categories, city, address, latitude, longitude
    FROM business
    WHERE categories LIKE ?
    '''
    
    # Add keyword-based filter to the query
    keyword_filter = f"%{poi_type}%"  # Match the type in categories
    params = [keyword_filter]
    
    # Add other filters (e.g., rating, review count) if provided
    for attr, value in filters.items():
        if isinstance(value, str):
            query += f' AND {attr} LIKE ?'
            params.append(f"%{value}%")
        else:
            operator = value[0]  # The operator e.g., '=', '>=', '>'
            value = value[1]  # The actual value
            query += f' AND {attr} {operator} ?'
            params.append(value)
    
    # Order by rating and review count, descending
    query += '''
    ORDER BY stars DESC, review_count DESC
    LIMIT ?
    '''
    params.append(k)
    
    # Execute the query
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# Example usage:
poi_type = 'restaurant'  # E.g., restaurant, museum
keywords = {'French', 'Italian'}  # Categories or other keywords
filters = {'stars': ('>=', 4), 'review_count': ('>', 100)}  # Filters like rating, review count
top_k = 5  # Number of results to return

# Query and print the top-k results
top_pois = query_pois(poi_type, keywords, filters, top_k)
for poi in top_pois:
    print(poi)
