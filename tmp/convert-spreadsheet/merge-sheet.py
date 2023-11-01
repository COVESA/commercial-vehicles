import pandas as pd
import yaml


# Load the YAML file
yaml_file_path = 'vss_rel_4.0.yaml'
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
    
    # Check if the VSS value exists in the YAML data
    if vss_value in yaml_data:
        yaml_entry = yaml_data[vss_value]
        
        # Add the additional fields from the spreadsheet
        yaml_entry['category'] = row['category']
        yaml_entry['importance'] = row['importance']
        yaml_entry['usecase'] = row['usecase']
        yaml_entry['sampling'] = row['sampling']
        
        # Store the updated YAML entry
        yaml_entries_with_extra_fields[vss_value] = yaml_entry

# Save the resulting YAML data
with open('output.yaml', 'w') as output_yaml_file:
    yaml.dump(yaml_entries_with_extra_fields, output_yaml_file, default_flow_style=False)

print("Processing complete. The result is saved in 'output.yaml'.")
