import requests
from constants import CFSRE_URL, HEADERS

from bs4 import BeautifulSoup

from os import remove
from os.path import exists



"""
Downloads a PDF from the Web

'local_filename = url.split('/')[-1]' : file is named after the last part in the url

'headers = headers' : provides a new User-Agent to bypass bot-detection (see constants)
"""
def download_pdf(pdf_url):
    local_filename = pdf_url.split('/')[-1]

    with requests.get(pdf_url, headers = HEADERS) as request:
        with open(local_filename, 'wb') as new_file:
            new_file.write(request.content)
    
    return local_filename


"""
All relevant pdf urls follow this RegEx: /images/monographs/ at the start, .pdf at the end


"""
def create_list_urls():
    page_to_scrape = requests.get(CFSRE_URL, headers = HEADERS)

    soup = BeautifulSoup(page_to_scrape.text, features = "html.parser")

    links = [a['href'] for a in soup.find_all('a',href=True)]
    
    return links
    #An die passenden Links muss von vorne auch noch "https://www.cfsre.org" angehänt werden


"""
Recieves a list of Strings, containing all links on the website.
Returns a list of Strings, with NPS pdf-links

Noch in Arbeit
"""
def filter_list(links):
    filtered_list = []
    # temporary for testing:
    for link in links:
        if ("/images/monographs" in link) and (".pdf" in link):
            filtered_list +=["https://www.cfsre.org" + link.strip()]
            print("https://www.cfsre.org" + link.strip())
    
    return filtered_list

def delete_file(filename):
    if exists(filename):
        remove(filename)

#Test
print(len(filter_list(create_list_urls())))
# liefert 154 pdf Elemente
# Maxi wieviel passende sind auf der website?