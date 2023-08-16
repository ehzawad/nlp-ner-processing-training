import json
import ast

# Paths to the uploaded JSONL files (adjust to your local paths)
no_time_file_path = '/home/ehz/Downloads/no-time-output.jsonl'
time_file_path = '/home/ehz/Downloads/time.jsonl'

# Read the content from the no-time-output.jsonl file
no_time_data = []
with open(no_time_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        no_time_data.append(json.loads(line.strip()))

# Read the content from the time.jsonl file, using literal_eval for parsing
time_data = []
with open(time_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        time_data.append(ast.literal_eval(line.strip()))

# Convert time_data into a dictionary with ID as the key
time_data_dict = {entry['id']: entry['label'] for entry in time_data}

# Merge the properties based on matching IDs
merged_data = []
for entry in no_time_data:
    entry_id = entry['id']
    if entry_id in time_data_dict:
        entry['label'] += time_data_dict[entry_id]
    merged_data.append(entry)

# Path to the output JSONL file for saving the merged data (adjust to your local path)
merged_file_path = '/home/ehz/Downloads/merged_output.jsonl'

# Writing the merged data to the JSONL file
with open(merged_file_path, 'w', encoding='utf-8') as file:
    for entry in merged_data:
        file.write(json.dumps(entry, ensure_ascii=False) + '\n')

