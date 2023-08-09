import sys
import xml.etree.ElementTree as ET
from pprint import pprint
from datetime import datetime
import json
# from mapping import knacklyToHotDocs2, hotdocsToKnackly
from mapping import knacklyToHotDocs2

def save_dict_to_json(d: dict, filename: str) -> None:
    with open(filename, 'w') as out_file:
        stream = json.dumps(d, indent=2)
        out_file.write(stream)

def anx_to_knackly_json(filename: str) -> dict:
    x = {}
    # x['address'] = {}
    
    # tree = ET.parse(filename)
    # answer_set = tree.getroot()

    # for idx, answer in enumerate(answer_set[1:], start=1):
    #     child = answer[0]
    #     if 'name' in answer.attrib:
    #         key = answer.attrib['name']
            
    #     # ---
    #     if key == 'hd_goals': # Looking at Knackly, we know that goals is a list of text elements
    #         x[hotdocsToKnackly[key]] = []
    #         for sub_child in child:
    #             x[hotdocsToKnackly[key]].append(parse_TextValue(sub_child.text))
    #         continue
        
    #     address_keys = ['hd_borrowerStreet', 'hd_borrowerCity', 'hd_borrowerZip', 'hd_borrowerCounty', 'hd_borrowerState'] # We know that these answers will make up the Knackly 'address' object
    #     if key in address_keys:
    #         if key == 'hd_borrowerStreet':
    #             x['address']['street'] = parse_TextValue(child.text)
    #         elif key == 'hd_borrowerCity':
    #             x['address']['city'] = parse_TextValue(child.text)
    #         elif key == 'hd_borrowerZip':
    #             x['address']['zip'] = parse_TextValue(child.text)
    #         elif key == 'hd_borrowerCounty':
    #             x['address']['county'] = parse_TextValue(child.text)
    #         elif key == 'hd_borrowerState':
    #             x['address']['state'] = parse_TextValue(child[0].text) # This uses 'child[0]' because 'borrowerState' is actually a MCValue, with a nested 'SelValue' that holds the state text
    #         continue
    #     # ---
            
    #     if child.tag in ['RptValue', 'MCValue']:
    #         print('here')
    #         for sub_child in child:
    #             if sub_child.tag == 'SelValue':
    #                 x[key] = parse_TextValue(sub_child.text)
    #     else:
    #         if child.tag == 'NumValue':
    #             x[hotdocsToKnackly[key]] = parse_NumValue(child.text)
    #         elif child.tag == 'DateValue':
    #             x[hotdocsToKnackly[key]] = parse_DateValue(child.text)
    #         elif child.tag == 'TFValue':
    #             x[hotdocsToKnackly[key]] = parse_TFValue(child.text)
    #         elif child.tag == 'TextValue':
    #             x[hotdocsToKnackly[key]] = parse_TextValue(child.text)
            
    # save_dict_to_json(x, 'test.json')
    return x

def anx_to_knackly_json2(filename: str) -> dict:
    x = {}
    tree = ET.parse(filename)
    answer_set = tree.getroot()
    
    for answer in answer_set[1:]:
        child = answer[0]
        if 'name' in answer.attrib:
            key = answer.attrib['name']
            
        # map_value = hotdocsToKnackly[key]
        map_value = 2
        
        object_map = map_value.split('.')
        if len(object_map) == 1:
            pass
        else:
            for i, key in enumerate(object_map[:-1]):
                print(key)
            # x[object_map[0]] = {}
        # x[thing[0]] = {}
            
        if child.tag in ['RptValue', 'MCValue']:
            for sub_child in child:
                print(key, sub_child.text)
        else:
            if child.tag == 'NumValue':
                pass
            #     x[hotdocsToKnackly[key]] = parse_NumValue(child.text)
            # elif child.tag == 'DateValue':
            #     x[hotdocsToKnackly[key]] = parse_DateValue(child.text)
            
    
    return x

def anx_to_knackly_json3(filename: str) -> dict:
    x = {}
    tree = ET.parse(filename)
    answer_set = tree.getroot()
    
    for answer in answer_set[1:]:
        child = answer[0]
    

# filename2 = './examples/hotdocs/multipleLendersExample.anx'
filename2 = './examples/hotdocs/subordinations_example.anx'

if __name__ == "__main__":
    # pprint(anx_to_knackly_json('simple_hotdocs_example.anx'))
    # result = anx_to_knackly_json(filename2)
    d = knacklyToHotDocs2
    save_dict_to_json(2, 'test2.json')
    # pprint(result, indent=2)