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
import sys
yaml_file_path = sys.argv[1] if len(sys.argv) > 1 else 'vss.yaml'
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
    
    # A cell may hold several patterns separated by newlines, spaces or commas
    # (commas inside {a,b} braces are kept). Keep only tokens that look like VSS paths.
    protected = re.sub(r'\{[^}]*\}', lambda m: m.group(0).replace(',', '\x00'), vss_value)
    tokens = [t.replace('\x00', ',') for t in re.split(r'[\s,]+', protected) if t.startswith('Vehicle.')]
    if not tokens:
        print(f"Skipping row {index} due to missing or invalid VSS value: {vss_value}")
        continue
    vss_value_cleaned = ' '.join(tokens)

    matching_keys = []
    for token in tokens:
        vss_regex = convert_pattern_to_regex(clean_key_pattern(token))
        matching_keys += [key for key in yaml_data if re.match(vss_regex, clean_key_pattern(key))]
    
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
        print(f"Warning: No match found for VSS value: {vss_value_cleaned} (row {index})")

# Save the resulting YAML data
with open('output.yaml', 'w') as output_yaml_file:
    yaml.dump(yaml_entries_with_extra_fields, output_yaml_file, default_flow_style=False)

print("Processing complete. The result is saved in 'output.yaml'.")
