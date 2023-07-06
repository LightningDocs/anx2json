import sys
import json

def remove_key(d: dict, k: str) -> dict:
    '''Recursively remove all keys with the name 'k' from the nested dictionary 'd'
    '''
    if not isinstance(d, dict):
        return d
    new_dict = {}
    for key, value in d.items():
        if key == k:
            continue
        elif isinstance(value, dict):
            new_dict[key] = remove_key(value, k)
        else:
            new_dict[key] = value
    return new_dict

# Load the specified file into memory, as a python dictionary
if len(sys.argv) != 2:
    print('Sorry, usage must be in the format: \'python strip_id.py <filename>\'')
    sys.exit()
    
filename = sys.argv[1]
with open(filename, 'r') as in_file:
    data = json.load(in_file)

# Remove all 'id$' keys since we cannot predict those
data = remove_key(data, 'id$')

# Save the altered json as a new file
with open(f'_{filename}', 'w') as out_file:
    stream = json.dumps(data, indent=2)
    out_file.write(stream)
    
print(f'Success! New file created: _{filename}')