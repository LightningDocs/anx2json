# import xmltodict
import sys
import xml.etree.ElementTree as ET
import pprint
from datetime import datetime
import json
from strip_id import remove_key

def parse_TextValue(text: str) -> str:
    return text

def parse_NumValue(num: str) -> int:
    f = float(num)
    if f.is_integer():
        return int(f)
    else:
        return float(num)

def parse_DateValue(date: str) -> str:
    date_object = datetime.strptime(date, '%d/%m/%Y')
    return date_object.strftime('%Y-%m-%d')

def parse_TFValue(boolean: str) -> bool:
    return bool(boolean)

def parse_RptValue() -> list:
    pass

def save_dict_to_json(d: dict, filename: str) -> None:
    with open(filename, 'w') as out_file:
        stream = json.dumps(d, indent=2)
        out_file.write(stream)

def anx_to_json(filename: str) -> None:
    x = {}
    x['address'] = {'street': None, 'city': None, 'zip': None, 'county': None, 'state': None}
    
    tree = ET.parse(filename)
    answer_set = tree.getroot()

    for idx, answer in enumerate(answer_set[1:], start=1):
        child = answer[0]
        if 'name' in answer.attrib:
            key = answer.attrib['name']
            
        # ---
        if key == 'goals': # Looking at Knackly, we know that goals is a list of text elements
            x[key] = []
            for sub_child in child:
                x[key].append(parse_TextValue(sub_child.text))
            continue
        
        address_keys = ['borrowerStreet', 'borrowerCity', 'borrowerZip', 'borrowerCounty', 'borrowerState'] # We know that these answers will make up the Knackly 'address' object
        if key in address_keys:
            if key == 'borrowerStreet':
                x['address']['street'] = parse_TextValue(child.text)
            elif key == 'borrowerCity':
                x['address']['city'] = parse_TextValue(child.text)
            elif key == 'borrowerZip':
                x['address']['zip'] = parse_TextValue(child.text)
            elif key == 'borrowerCounty':
                x['address']['county'] = parse_TextValue(child.text)
            elif key == 'borrowerState':
                x['address']['state'] = parse_TextValue(child[0].text) # This uses 'child[0]' because 'borrowerState' is actually a MCValue, with a nested 'SelValue' that holds the state text
            continue
        # ---
            
        if child.tag in ['RptValue', 'MCValue']:
            for sub_child in child:
                if sub_child.tag == 'SelValue':
                    x[key] = parse_TextValue(sub_child.text)
        else:
            if child.tag == 'NumValue':
                x[key] = parse_NumValue(child.text)
            elif child.tag == 'DateValue':
                x[key] = parse_DateValue(child.text)
            elif child.tag == 'TFValue':
                x[key] = parse_TFValue(child.text)
            elif child.tag == 'TextValue':
                x[key] = parse_TextValue(child.text)
            
    # save_dict_to_json(x, 'test.json')
    return x

def compare(anx_dict: dict, json_file: str) -> bool:
    # Load the json file into memory and convert it to a dictionary
    try:
        with open(json_file, 'r') as in_file:
            json_dict = json.load(in_file)
            json_dict = remove_key(json_dict, 'id$')
    except FileNotFoundError:
        print(f'The file \'{json_file}\' does not exist. Are you sure you are typing it correctly?')
        sys.exit()
    except Exception as e:
        print(f'Could not parse {json_file} into valid JSON. Make sure your file is formatted properly.')
        sys.exit()
        
    # Compare the two
    if anx_dict == json_dict:
        return True
    else:
        return False
    
if __name__ == "__main__":
    # anx_to_json('simple_hotdocs_example.anx')
    result = compare(anx_to_json('simple_hotdocs_example.anx'), 'knackly_example.json')
    print(result)