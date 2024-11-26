import json
import pandas as pd
import pickle

# Function to load a JSON file into a DataFrame
def load_json_to_dataframe(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(json.loads(line))  # Parse each JSON object separately
    return pd.DataFrame(data)

# List of JSON file paths
file_paths = {
    "business": "yelp_academic_dataset_business.json",
    "review": "yelp_academic_dataset_review.json",
    "user": "yelp_academic_dataset_user.json",
    "checkin": "yelp_academic_dataset_checkin.json",
    "tip": "yelp_academic_dataset_tip.json",
}

# Dictionary to store DataFrames
dataframes = {}

# Load each file and display the first few rows
for name, path in file_paths.items():
    try:
        print(f"\nLoading {name} dataset from {path}...")
        df = load_json_to_dataframe(path)  # Load JSON file into a DataFrame
        dataframes[name] = df  # Store DataFrame in the dictionary
        print(f"First few rows of {name} dataset:")
        print(df.head())  # Display the first few rows
        print(f"Columns in {name} dataset: {df.columns.tolist()}\n")
    except Exception as e:
        print(f"Error loading {name} dataset: {e}")

# Save the DataFrames to disk using pickle for future use
with open('dataframes.pkl', 'wb') as f:
    pickle.dump(dataframes, f)

# To load the DataFrames back into memory in the future
# with open('dataframes.pkl', 'rb') as f:
#     dataframes = pickle.load(f)

# Now you have the datasets loaded into `dataframes` dictionary
# Access each dataset using its name, e.g., dataframes['business'], dataframes['review']
