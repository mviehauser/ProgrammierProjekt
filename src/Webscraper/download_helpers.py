import requests
from constants import CFSRE_URL, HEADERS

from bs4 import BeautifulSoup

from os import remove
from os.path import exists


"""
Downloads a PDF from the Web

'local_filename = url.split('/')[-1]' : file is named after the last part in the url

'headers = HEADERS' : provides a new User-Agent to bypass bot-detection (see constants)
"""
def download_pdf(pdf_url):
    local_filename = pdf_url.split('/')[-1]

    with requests.get(pdf_url, headers = HEADERS) as request:
        with open(local_filename, 'wb') as new_file:
            new_file.write(request.content)
    
    return local_filename


"""
Doesn't need a Argument, because the url of cfsre is seen as a constant

Returns a list of strings, containing all Links to NPS pdfs

"""
def create_list_urls():
    page_to_scrape = requests.get(CFSRE_URL, headers = HEADERS)

    soup = BeautifulSoup(page_to_scrape.text, features = "html.parser")

    links = []

    # .find_all('a', href = True) finds all anchor-elements and puts everything from <a> to </a> in a list
    # by using ['href'], we only refer to the string past 'href ='
    # all relevant pdf-links have "/images/monographs" and ".pdf" as substrings
    # since these are relative links, it's important to put "https://www.cfsre.org" in front

    for a in soup.find_all('a', href = True):
        if ("/images/monographs" in a['href']) and (".pdf" in a['href']):
            links+= ["https://www.cfsre.org" + a['href'].strip()]
    
    return links


"""
Deletes the locally stored file
Args:
- String name of the file
"""
def delete_file(filename):
    if exists(filename):
        remove(filename)

"""
# Test:
links = create_list_urls()
print(links)
print(len(links))
download_pdf(links[100])
print(links[100])
delete_file(links[100].split('/')[-1])
# liefert 154 pdf Elemente, also genau 10Seiten * 15 PDFs + 1Seite * 4 PDFs
# Test bestanden ;)
"""