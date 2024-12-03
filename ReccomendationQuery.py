import sqlite3

# Function to query POIs based on input criteria
def query_pois(poi_type, keywords, filters, k=5):
    # Connect to the SQLite database (same folder as the script)
    conn = sqlite3.connect('yelp_data_test.db')
    cursor = conn.cursor()

    # Base query to search for POIs, first checking for the poi_type
    query = '''
    SELECT business_id, name, stars, review_count, categories, city, address, latitude, longitude
    FROM business
    WHERE categories LIKE ?
    '''
    
    # Parameters for the poi_type (check for the type in the categories)
    params = [f"%{poi_type}%"]

    # Keyword filter for categories
    keyword_filters = []
    for keyword in keywords:
        keyword_filters.append("categories LIKE ?")  # Partial match for each keyword
    
    # Combine keyword filters with 'OR'
    if keywords:
        query += " AND (" + " OR ".join(keyword_filters) + ")"
        params.extend([f"%{keyword}%" for keyword in keywords])

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
poi_type = 'Restaurant'  # E.g., restaurant, museum
keywords = []  # Categories or other keywords
filters = {'stars': ('>=', 3.5), 'review_count': ('>=', 50), 'city': 'Franklin'}  # Filters like rating, review count
top_k = 5  # Number of results to return

# Query and print the top-k results
top_pois = query_pois(poi_type, keywords, filters, top_k)
for poi in top_pois:
    print(poi)
