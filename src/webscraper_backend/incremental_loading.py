import json
from constants import LINK_ARCHIVE, JSON_PATH
from os.path import exists

"""
There are only 3 modes, therefore the mode has to be a valid number
"""
def check_mode(mode):
    if mode not in [1, 2, 3]:
        raise ValueError("You can only choose between mode 1, 2 and 3")
    
"""
Returns the existing data as list of dicts
In case there is no file, an empty list will be returned
"""
def load_existing_data():
    if exists(JSON_PATH) == False:
        return []
    with open(JSON_PATH, 'r') as existing_data_file:
        return json.load(existing_data_file)

"""
Archives list of links, so that we can check which link is new in every run

It is possible to take all 'source_url' from data.json, but then you're missing the links which could not be extracted in the past, 
since ed.extract_data_from_pdf() returns None if the pdf could not be extracted.
"""
def archive_links(links):
    with open(LINK_ARCHIVE, mode="w") as json_file:
        json.dump(links, json_file, indent=4)


# Unit Test for mode 2:
# Delete some links from src\JSON-files\link_archive.json. Then run main.py while making sure to set mode=2
# This simulates that new pdf-files are found on the website