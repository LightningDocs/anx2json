import argparse
import sys
import json

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [filename]",
        description="Removes any keys with the name \'id$\' from a provided json file."
    )
    parser.add_argument("filename", type=str)
    parser.add_argument("-r", "--replace", action='store_true', help='replace the provided file instead of creating a new file')
    return parser

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

# Parse command line arguments
parser = init_argparse()
args = parser.parse_args()

filename = args.filename
period_index = filename.rfind('.')
if period_index == -1:
    print(f'Please include the file extension \'.json\'')
    sys.exit()

extension = filename[period_index:]
if extension != '.json':
    print(f'You must provide a .json file, not a \'{extension}\' file')
    sys.exit()
    
# Load the json object into memory
try:
    with open(filename, 'r') as in_file:
        data = json.load(in_file)
except FileNotFoundError:
    print(f'The file \'{filename}\' does not exist. Are you sure you are typing it correctly?')
    sys.exit()
except Exception as e:
    print(f'Could not parse {filename} into valid JSON. Make sure your file is formatted properly.')
    sys.exit()

# Remove all 'id$' keys since we cannot predict those
data = remove_key(data, 'id$')

# Save the altered json to a file
if not args.replace:
    filename = '_' + filename
    
with open(filename, 'w') as out_file:
    stream = json.dumps(data, indent=2)
    out_file.write(stream)
    
print(f'Success! New file created: {filename}')