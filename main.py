# import xmltodict
import xml.etree.ElementTree as ET

def main():
    # tree = ET.parse('country_data.xml')
    tree = ET.parse('hotdocs_example.anx')
    root = tree.getroot()
    # print(root)
    
if __name__ == "__main__":
    main()