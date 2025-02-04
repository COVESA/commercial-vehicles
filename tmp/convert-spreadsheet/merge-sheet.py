import pandas as pd
import yaml
import re

# Function to convert pattern with '*' and '{b,c}' to regex
def convert_pattern_to_regex(pattern: str) -> str:
    # Replace '*' with '.*' to match any characters
    regex_pattern = pattern.replace('*', '.*')
    
    # Replace '{b,c}' with '(b|c)' for matching choices
    #regex_pattern = re.sub(r'\{([a-zA-Z0-9,]+)\}', r'(\1)', regex_pattern)
    regex_pattern = re.sub(r'\{([a-zA-Z0-9,]+)\}', lambda match: f"({match.group(1).replace(',', '|')})", regex_pattern)
    
    # Ensure we match the whole string (start to end)
    return f"^{regex_pattern}$"

# Function to clean key pattern (remove whitespace and =AAAA)
def clean_key_pattern(key: str) -> str:
    # Remove any whitespace
    key = key.replace(' ', '')
    # Remove '=AAAA' where AAAA is uppercase letters
    key = re.sub(r'=[A-Z_]+', '', key)
    return key

# Load the YAML file
yaml_file_path = 'vss.yaml'
with open(yaml_file_path, 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Load the spreadsheet
spreadsheet_path = 'sheet.csv'
df = pd.read_csv(spreadsheet_path)

# Create a dictionary to store the YAML entries with additional fields
yaml_entries_with_extra_fields = {}

# Iterate through the spreadsheet rows
for index, row in df.iterrows():
    vss_value = row['VSS']
    
    # Check for invalid VSS values (e.g., NaN, 'Not in VSS')
    if pd.isna(vss_value) or vss_value == "Not in VSS":
        print(f"Skipping row {index} due to missing or invalid VSS value: {vss_value}")
        continue
    
    # Clean the VSS value by removing unwanted parts
    vss_value_cleaned = clean_key_pattern(vss_value)
    
    # Convert the VSS pattern to regex
    vss_regex = convert_pattern_to_regex(vss_value_cleaned)
    
    # Find matching keys in the YAML data using regex
    matching_keys = [key for key in yaml_data if re.match(vss_regex, clean_key_pattern(key))]
    
    if matching_keys:
        for key in matching_keys:
            yaml_entry = yaml_data[key]
            
            # Add the additional fields from the spreadsheet
            yaml_entry['category'] = row['Pillar']
            yaml_entry['importance'] = row['Importance for use case']
            yaml_entry['usecase'] = row['Use case #']
            yaml_entry['sampling'] = row['Recommended Sampling']
            
            # Store the updated YAML entry
            yaml_entries_with_extra_fields[key] = yaml_entry
    else:
        print(f"Warning: No match found for VSS value: {vss_value_cleaned} (row {index}) with {vss_regex}")

# Save the resulting YAML data
with open('output.yaml', 'w') as output_yaml_file:
    yaml.dump(yaml_entries_with_extra_fields, output_yaml_file, default_flow_style=False)

print("Processing complete. The result is saved in 'output.yaml'.")
