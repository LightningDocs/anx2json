import xml.etree.ElementTree as ET
import json

# from mapping import knacklyToHotDocs2, hotdocsToKnackly
from mapping import knacklyToHotDocs
from anx_utilities import remove_none_values


def save_dict_to_json(d: dict, filename: str) -> None:
    with open(filename, "w") as out_file:
        stream = json.dumps(d, indent=2)
        out_file.write(stream)


def anx_to_knackly_json2(filename: str) -> dict:
    x = {}
    tree = ET.parse(filename)
    answer_set = tree.getroot()

    for answer in answer_set[1:]:
        child = answer[0]
        if "name" in answer.attrib:
            key = answer.attrib["name"]

        # map_value = hotdocsToKnackly[key]
        map_value = 2

        object_map = map_value.split(".")
        if len(object_map) == 1:
            pass
        else:
            for i, key in enumerate(object_map[:-1]):
                print(key)
            # x[object_map[0]] = {}
        # x[thing[0]] = {}

        if child.tag in ["RptValue", "MCValue"]:
            for sub_child in child:
                print(key, sub_child.text)
        else:
            if child.tag == "NumValue":
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


filename2 = "./examples/hotdocs/subordinations_example.anx"

if __name__ == "__main__":
    d = knacklyToHotDocs
    d = remove_none_values(d)
    save_dict_to_json(d, "test2.json")
