from json import dump
import os
import pdfplumber
from constants import DATA
from rdkit.Chem.inchi import InchiToInchiKey
from re import compile, search, DOTALL

"""
There are 2 different types of pdfs:
    Type 1 : https://www.cfsre.org/images/monographs/Medetomidine-New-Drug-Monograph-NPS-Discovery-112723.pdf
    Type 2 : https://www.cfsre.org/images/monographs/BZO-POXIZID_101921_CFSRE_Chemistry_Report.pdf 

Type 1 has all the important information on the first page.
Type 2 has some information in the text and on page two, therefore regular expressions are needed.
"""
def extract_data_from_pdf(pdf_path):
    table = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()
    
    data = DATA.copy()
    
    if table[0][0] == "Preferred Name":
        # This is Type 1
        for column in table:
            data[column[0]] = column[1]
        return data
    else:
        # This is Type 2
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[1]
            table += page.extract_table()
        
        data["Preferred Name"] = table[0][1]

        data["Chemical Formula"] = table[2][1]
        data["Molecular Weight"] = table[2][2]
        data["Molecular Ion [M+]"] = table[2][3]
        data["Exact Mass [M+H]+"] = table[2][4]
        
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        re_synonyms = compile(r'Synonyms:.*')
        data["Synonyms"] = re_synonyms.search(text).group(0)[10:]

        re_IUPAC_Name = compile(r'IUPAC.Name:.*')
        data["Formal Name"] = re_IUPAC_Name.search(text).group(0)[12:]

        re_inchiString = compile(r'InChI.String:.*CFR', DOTALL)
        inchi_String = re_inchiString.search(text).group(0).replace("\n", "")[14:-3]
        data["InChI Key"] = InchiToInchiKey(inchi_String)

        re_casNumber = compile(r'CAS#.*')
        data["CAS Number"] = re_casNumber.search(text).group(0)[5:]
        
        return data
    
"""
Saves table data as a JSON file.

Args:
- table (list of lists): The table data to save.
- json_file (str): Path to the JSON file.
"""
def save_table_as_json(table, json_file):

    with open(json_file, 'w') as f:
        dump(table, f)


pdf_path = "sample2.pdf"

# Name of the created JSON-file
json_filename = 'sample_table_data.json'

# Relative Path to JSON-files folder
#directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
#json_file_path = os.path.join(directory, json_filename)


print(extract_data_from_pdf(pdf_path))