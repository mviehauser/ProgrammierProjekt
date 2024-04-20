from json import dump
import os
import pdfplumber
from constants import DATA
from rdkit.Chem.inchi import InchiToInchiKey
from re import compile, search, DOTALL

"""
Args:
- pdf-Path
- pdf_info: a dict which contains the key 'pdfPage' to decide which page to extract and increment the page number for possibly needed future extractions
"""
def extract_table_pdfPage(pdf_path, pdf_info):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[pdf_info['pdfPage']]
        x= page.extract_table()
        pdf_info['pdfPage'] += 1
        if x is not None:
            return x
        else:
            return []
"""
There are at least 3 different types of pdfs, with different internal structure:
    Type 1 "NPS Discovery (new)" : https://www.cfsre.org/images/monographs/Medetomidine-New-Drug-Monograph-NPS-Discovery-112723.pdf
    Type 2 "NPS Discovery (old)" : https://www.cfsre.org/images/monographs/BZO-POXIZID_101921_CFSRE_Chemistry_Report.pdf 
    Type 3 "NMS LABS" : https://www.cfsre.org/images/monographs/25E-NBOH_022718_NMSLabs_Report.pdf

Type 1 has all the important information on the first page in a table and definies which infos have to be in DATA
Type 2+ does not have every information in a table, therefore regular expressions and text extraction is needed.
"""
def extract_data_from_pdf(pdf_path):
    pdf_info = {
        'pdfPage' : 0,
    }
    table = extract_table_pdfPage(pdf_path, pdf_info)
    data = DATA.copy()
    
    if len(table) == 9:
        # This is Type 1
        if table[0][0] == "Preferred Name":
            for column in table:
                data[column[0]] = column[1]
        else:
            print("Error: Expected 'Preferred Name' in table[0][0]")
            data = None
    else:
        # This is Type 2+
        # while-loop ensures there are at least two table-rows in 'table', which means "2.1 CHEMICAL DATA" is extracted
        while len(table) < 2:
            table += extract_table_pdfPage(pdf_path, pdf_info)
        
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        if len(table) == 3:
            # if true, this means the heading(chemical prefered name) is stored in a table, NOT in the text
            data["Preferred Name"] = table[0][1]
            chemical_data_row = 2
        elif len(table) == 2:
            # in this case, the heading is stored in the 4th line of text
            if "NMS Labs" in text.split('\n')[0]:
                data["Preferred Name"] = text.split('\n')[3]
            else:
                data["Preferred Name"] = text.split('\n')[0]
            chemical_data_row = 1
        else:
            raise ValueError(f"Unexpected table size in {pdf_path}")

        data["Chemical Formula"] = table[chemical_data_row][1]
        data["Molecular Weight"] = table[chemical_data_row][2]
        data["Molecular Ion [M+]"] = table[chemical_data_row][3]
        data["Exact Mass [M+H]+"] = table[chemical_data_row][4]

        # These Data-keys are only to be found by RegExps
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

#test
if __name__ == "__main__":
    pdf_path = "ADB-5-Br-PINACA-New-Drug-Monograph-NPS-Discovery-230501.pdf"

    # Name of the created JSON-file
    #json_filename = 'sample_table_data.json'

    # Relative Path to JSON-files folder
    #directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
    #json_file_path = os.path.join(directory, json_filename)


    print(extract_data_from_pdf(pdf_path))