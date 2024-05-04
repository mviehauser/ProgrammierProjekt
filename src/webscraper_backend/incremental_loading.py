from json import dump
from constants import LINK_ARCHIVE

"""
There are only 3 modes, therefore the mode has to be a valid number
"""
def check_mode(mode):
    if mode not in [1, 2, 3]:
        raise ValueError("You can only choose between mode 1, 2 and 3")
    

"""
Archives list of links, so that we can check which link is new in every run
"""
def archive_links(links):
    with open(LINK_ARCHIVE, mode="w") as json_file:
         dump(links, json_file, indent=4)


# Unit Test for mode 2:
# Delete some links from src\JSON-files\link_archive.json. Then run main.py while making sure to set mode=2
# This simulates that new pdf-files are found on the website