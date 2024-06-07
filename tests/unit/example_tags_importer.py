from resolver.tagparser.dbm import RegexPattern, Tagstyle
from typing import List
import json


# Read the JSON file and convert it to Tagstyle objects
def read_json_and_get_tags(json_file_path) -> List[Tagstyle]:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    sample_tags = []
    
    for tag_name, tag_data in data.items():
        entire_pattern = RegexPattern(name=tag_name, pattern=tag_data["ENTIRE_PATTERN"])
        contents = [
            RegexPattern(name=content_name, pattern=content_pattern)
            for content_name, content_pattern in tag_data["contents"].items()
        ]
        sample_tags.append(Tagstyle(entire_pattern=entire_pattern, contents=contents))

    return sample_tags