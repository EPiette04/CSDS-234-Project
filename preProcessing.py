import sqlite3
import json

# Function to identify rows with malformed JSON in the 'attributes' column
def find_malformed_json_rows():
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()

    # Query to fetch all the rows and their 'attributes' column
    cursor.execute("SELECT business_id, attributes FROM business LIMIT 151000")  # You can change the LIMIT if needed
    rows = cursor.fetchall()

    malformed_rows = []

    # Try to load each 'attributes' column as JSON and find rows where it fails
    for row in rows:
        business_id, attributes_str = row
        try:
            # Attempt to load the 'attributes' field as JSON
            json.loads(attributes_str)
        except json.JSONDecodeError:
            # If it fails, add the business_id to the list of malformed rows
            malformed_rows.append(business_id)

    conn.close()

    return malformed_rows

# Find rows with malformed JSON
malformed_rows = find_malformed_json_rows()

# Output the IDs of the rows with malformed JSON
print(f"Rows with malformed JSON (business_id): {malformed_rows.__sizeof__()}")
def inspect_malformed_rows():
    malformed_rows = find_malformed_json_rows()
    conn = sqlite3.connect('yelp_data.db')
    cursor = conn.cursor()

    # Inspect each malformed row and print its attributes
    for business_id in malformed_rows:
        cursor.execute("SELECT business_id, attributes FROM business WHERE business_id = ?", (business_id,))
        row = cursor.fetchone()

        if row:
            business_id, attributes_str = row
            if attributes_str:  # Check if the attributes field is not None
                print(f"business_id: {business_id}")
                try:
                    # Try to load the JSON string
                    attributes_json = json.loads(attributes_str)
                    print(f"Attributes (parsed): {json.dumps(attributes_json, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON for business_id: {business_id}")
            else:
                print(f"business_id: {business_id} - Attributes are NULL or missing")

        print("-" * 50)

    conn.close()

# Inspect and print the malformed rows
#inspect_malformed_rows()

