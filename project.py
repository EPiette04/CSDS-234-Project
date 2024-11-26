import json
import pandas as pd

# Open the JSON file with the correct encoding
business_data = []
with open("yelp_academic_dataset_business.json", "r", encoding="utf-8") as file:
    for line in file:
        business_data.append(json.loads(line))  # Parse each JSON object separately

# Convert the list of dictionaries into a DataFrame
business_df = pd.DataFrame(business_data)

# Inspect the first few rows and columns
print(business_df.head())
print(business_df.columns)
