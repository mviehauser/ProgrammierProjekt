import json

import requests
from bs4 import BeautifulSoup
from constants import CFSRE_URL, HEADERS
from datetime import datetime

"""
There are only 3 modes, therefore the mode has to be a valid number
"""
def check_mode(mode):
    if mode not in [1, 2, 3]:
        raise ValueError("You can only choose between mode 1, 2 and 3")
    
"""
Returns the existing data
In case there is no file, an empty list will be returned
"""
def load_json(path):
    try:
        with open(path, 'r') as existing_data_file:
            return json.load(existing_data_file)
    except Exception as e:
        return []

"""
Archives list of links, so that we can check which link is new in every run

It is possible to take all 'source_url' from data.json, but then you're missing the links which could not be extracted in the past, 
since ed.extract_data_from_pdf() returns None if the pdf could not be extracted.
"""
def archive_links(links, link_archive_path):
    with open(link_archive_path, mode="w") as json_file:
        json.dump(links, json_file, indent=4)

"""
    date_string-Format: yyyy-mm-dd
    .JSON-files can store Strings, but not datetime objects
"""
def fetch_date_strings():
    page_to_scrape = requests.get(CFSRE_URL, headers = HEADERS)
    soup = BeautifulSoup(page_to_scrape.text, features = "html.parser")
    dates = []

    for td in soup.find_all('td'):
        if 'data-sort' in td.attrs:
            date_str = td['data-sort'].strip().replace("/", "-")
            dates.append(date_str)
    
    return dates

def date_string_to_date(date_string):
    date_string = date_string.replace("T00:00:00Z", '')
    [year, month, day] = date_string.split("-")
    return datetime(int(year), int(month), int(day))

# Unit Test for mode 2:
# Delete some links from src/JSON-files/link_archive.json. Then run main.py while making sure to set mode=2
# This simulates that new pdf-files are found on the website

# Unit Test for mode 3:
# Set 'last-modified' of some chemicals to an older date
# this simulates that a pdf has been modified and updated the date

if __name__ == "__main__":
    dates = fetch_date_strings()
    print(dates)
    print(len(dates))
    print(date_string_to_date(dates[0]) > date_string_to_date(dates[1]))
    print(date_string_to_date("2023-11-30T00:00:00Z"))