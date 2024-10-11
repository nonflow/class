import json
import xml.etree.ElementTree as ET

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    return json.dumps(xml_to_dict(root))

def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result
