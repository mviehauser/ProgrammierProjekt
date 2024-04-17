import json
import os
import pdfplumber
from constants import DATA
from rdkit.Chem.inchi import InchiToInchiKey

"""
Extracts tables from a PDF file using pdfplumber library.

Args:
- pdf_path (str): Path to the PDF file.
- page_number (int): Page number to extract the table from. Default is 0 (first page)

Returns:
- list of lists: The extracted table.
"""
def extract_table_from_pdf(pdf_path, page_number=0):

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        table = page.extract_table()
    return table

def extract_data_from_pdf(pdf_path, page_numbers = [0, 1]):
    data = DATA.copy()
    table = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in page_numbers:
            page = pdf.pages[page_number]
            table += page.extract_table()

    for key in data.keys():
        for column in table:
            if key == column[0]:
                data[key] = column[1]

    if data["Preferred Name"] == "":
        # Überschrift nehmen!
        print("x")

    if data["InChI Key"] == "":
        data["InChI Key"] == InchiToInchiKey(table[1][1])


    return data

def extract_data_from_pdf2(pdf_path, page_numbers = [0, 1]):
    data = {}
    table = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in page_numbers:
            page = pdf.pages[page_number]
            table += page.extract_table()

    for key in data.keys():
        for column in table:
            if key == column[0]:
                data[key] = column[1]

    if data["Preferred Name"] == "":


    if data["InChI Key"] == "":
        data["InChI Key"] == InchiToInchiKey(table[1][1])


    return data
"""
Saves table data as a JSON file.

Args:
- table (list of lists): The table data to save.
- json_file (str): Path to the JSON file.
"""
def save_table_as_json(table, json_file):

    with open(json_file, 'w') as f:
        json.dump(table, f)


# Example usage: "sample.pdf" file (sample file from url: https://www.cfsre.org/nps-discovery/monographs)
pdf_path = 'C:\\Users\\Fokus\\Code Projekte VS\\ProgrammierProjekt\\src\\Webscraper\\sample.pdf'

# Name of the created JSON-file
json_filename = 'sample_table_data.json'

# Relative Path to JSON-files folder
directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
json_file_path = os.path.join(directory, json_filename)


print(extract_data_from_pdf(pdf_path))




