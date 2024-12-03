import sqlite3
import pandas as pd
from FinalAlgorithm import query_pois

# Example usage
poi_type = 'Restaurant'  # Example POI type
keywords = ['Chinese']  # Example keywords (can be modified)
filters = {
    'stars': ('>=', 3), 
    'review_count': ('>', 20),
    'state': ('=', 'CA')  # Modify this filter as needed
}
top_k = 10  # Number of results to return

# Run the query using the imported query_pois function
results = query_pois(poi_type, keywords, filters, top_k)

# Convert the results into a pandas DataFrame for better display
df = pd.DataFrame(results, columns=["name", "stars", "review_count", "categories", "city", "address"])

# Save the DataFrame as an HTML file
df.to_html('query_results.html', index=False)

print("The results have been saved to 'query_results.html'. Open it in a web browser to view the table.")
