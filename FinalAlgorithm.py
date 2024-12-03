import sqlite3
import json

# Function to query POIs based on input criteria
def query_pois(poi_type, keywords, filters, k=5):
    # Connect to the SQLite database (same folder as the script)
    conn = sqlite3.connect('FinalDatabase.db')
    cursor = conn.cursor()
    
    # Base query to search for POIs, first checking for the poi_type
    query = '''
    SELECT name, stars, review_count, categories, city, address 
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

    # Add other filters (e.g., rating, review count, attributes) if provided
    for attr, value in filters.items():
        if attr == "attributes":
            # Special case for attributes: search inside JSON
            for key, val in value.items():
                # Ensure that the query looks for nested keys correctly
                query += f' AND json_extract(attributes, "$.{key}") = ?'
                params.append(val)
        else:
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
poi_type = 'Restaurant'  # E.g., type of business (restaurant, museum, etc.)
keywords = ['Chinese']  # Categories or other keywords
filters = {
    'stars': ('>=', 2), 
    'review_count': ('>', 20),
    'attributes': {'RestaurantsDelivery': 'True'}, 
    'state': ('=', 'ID')
    #'attributes': {'BusinessParking.lot': 'False'}  # Filter for businesses with 'BikeParking' set to True
}
top_k = 5  # Number of results to return

# Query and print the top-k results
top_pois = query_pois(poi_type, keywords, filters, top_k)
for poi in top_pois:
    print(poi)