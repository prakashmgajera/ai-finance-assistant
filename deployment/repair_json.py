import json
import re

input_path = 'crawled_finance_docs.json'
output_path = 'crawled_finance_docs_repaired.json'

# Read the raw file
with open(input_path, 'r') as f:
    raw = f.read()

# Attempt to repair common issues
# 1. Remove trailing commas before closing brackets
raw = re.sub(r',\s*([}\]])', r'\1', raw)
# 2. Remove any illegal control characters
raw = re.sub(r'[\x00-\x1F]+', '', raw)
# 3. Ensure the file starts and ends with [ ... ]
if not raw.strip().startswith('['):
    raw = '[' + raw
if not raw.strip().endswith(']'):
    raw = raw + ']'

# Try to load and dump as valid JSON
try:
    data = json.loads(raw)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Repaired JSON saved to {output_path} with {len(data)} records.")
except Exception as e:
    print(f"Failed to repair JSON: {e}")
