from json import dump
import pdfplumber
from constants import DATA
from rdkit.Chem.inchi import InchiToInchiKey
from re import compile, search, DOTALL

"""
Args:
- pdf-Path
- pdf_info: a dict which contains the key 'pdfPage' to decide which page to extract and increment the page number for possibly needed future extractions
"""
def extract_table_pdfPage(pdf_path, pdf_page = 0):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[pdf_page]
        x = page.extract_table()
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
def extract_data_from_pdf_test(pdf_path):
    table = extract_table_pdfPage(pdf_path)
    data = DATA.copy()
    
    if len(table) == 9:
        # This is Type 1
        if table[0][0] == "Preferred Name":
            for column in table:
                data[column[0]] = column[1]
        else:
            print("Error: Expected 'Preferred Name' in table[0][0]")
            data = None
        return data
    
    # this is Type 2+
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        page = pdf.pages[1]
        text += page.extract_text()
    
    t = text.split('\n')
    if "NMS Labs" in t[0]:
        if '&' in t[3] or 'and' in t[3]:
            print("Error: Two chemicals in one pdf")
            return None
        data["Preferred Name"] = t[3]
    else:
        data["Preferred Name"] = t[0]

    re_chemical_data = compile(r'(?<=Formula Weight).*?(?=3\. |Important)', DOTALL)
    chemical_data_infos = re_chemical_data.search(text).group(0).split('\n')[1:]

    if len(chemical_data_infos) == 3:
        _, chemical_data_infos[0] = chemical_data_infos[0].split(' ', 1)
    elif len(chemical_data_infos) == 4:
        chemical_data_infos = chemical_data_infos[1:]
        _, chemical_data_infos[1] = chemical_data_infos[1].split(' ', 1)
    else:
        print(f"Unknown size of chemical_data_infos: {chemical_data_infos}")
        print(len(chemical_data_infos))
        return None
    
    # Building formula from chemical_data_infos
    formula_numbers = chemical_data_infos[1].split(" ")

    re_formula_letters = compile(r'^[A-Za-z\s]+(?=\d)')
    formula_letters = re_formula_letters.search(chemical_data_infos[0]).group(0).strip().split(" ")

    formula = ""
    for i in range(len(formula_numbers)):
        formula += formula_letters[i]
        formula += formula_numbers[i]
    if(len(formula_letters) == len(formula_numbers)+1):
        formula += formula_letters[-1]

    data["Chemical Formula"] = formula
    
    # Extracting "molecular weight", "molecular ion[m+]" and "exact mass[m+h]+"
    re_chemical_data_numbers = compile(r'\b\d[^\n]*')
    chemical_data_numbers = re_chemical_data_numbers.search(chemical_data_infos[0]).group(0).split(" ")

    data["Molecular Weight"] = chemical_data_numbers[0]
    if len(chemical_data_numbers) == 3:
        data["Molecular Ion [M+]"] = chemical_data_numbers[1]
    elif len(chemical_data_numbers) == 2:
        # 'Molecular Ion [M+]' is not given. This is a good guess based on the "Molecular Weight"
        data["Molecular Ion [M+]"] = int(float(data["Molecular Ion [M+]"]))
    else:
        print("Error: unknown amount of elements in 'chemical_data_numbers'")
    
    data["Exact Mass [M+H]+"] = chemical_data_numbers[-1]

    # remaining regexes
    re_synonyms = compile(r'Synonyms:.*')
    data["Synonyms"] = re_synonyms.search(text).group(0)[10:]

    re_IUPAC_Name = compile(r'(?<=IUPAC.Name:.).*?(?=InChI)', DOTALL)
    data["Formal Name"] = re_IUPAC_Name.search(text).group(0).replace("\n", "")

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
    pdf_path = "src\\Webscraper\\pdf samples\\Trifluoromethyl-U-47700_121421_CFSRE_Toxicology_Report.pdf"

    # Name of the created JSON-file
    #json_filename = 'sample_table_data.json'

    # Relative Path to JSON-files folder
    #directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
    #json_file_path = os.path.join(directory, json_filename)


    print(extract_data_from_pdf_test(pdf_path))