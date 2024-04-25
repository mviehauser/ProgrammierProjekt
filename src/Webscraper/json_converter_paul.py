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
    pdf_info = {'pdfPage' : 0}
    table = extract_table_pdfPage(pdf_path, pdf_info)
    data = DATA.copy()
    
    if len(table) == 9:
        # This is Type 1
        if table[0][0] == "Preferred Name":
            data["Preferred Name"] = table[0][1]
            data["Synonyms"] = table[1][1]
            data["Formal Name"] = table[2][1]
            data["InChI Key"] = table[3][1]
            data["CAS Number"] = table[4][1]
            data["Chemical Formula"] = table[5][1]
            data["Molecular Weight"] = table[6][1]
            data["Molecular Ion [M+]"] = table[7][1]
            data["Exact Mass [M+H]+"] = table[8][1]
        else:
            print("Error: Expected 'Preferred Name' in table[0][0]")
            data = None
        return data
    
    # This is Type 2+
    # while-loop ensures there are at least two table-rows in 'table', which means "2.1 CHEMICAL DATA" is extracted
    while len(table) < 2:
        table += extract_table_pdfPage(pdf_path, pdf_info)
        
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    
    # Preferred Name in text
    t = text.split('\n')
    if "NMS Labs" in t[0]:
        if '&' in t[3] or 'and' in t[3]:
            print("Error: Two chemicals in one pdf")
            return None
        data["Preferred Name"] = t[3]
    elif "The Center for Forensic Science Research and Education" in t[0]:
        data["Preferred Name"] = t[4]
    else:
        data["Preferred Name"] = t[0]
    
    # These Data-keys are only to be found in the text by RegExps
    # DOTALL used when information can be spread over multiple lines
    re_synonyms = compile(r'(?<=Synonyms:.).*?(?=Source|Important)', DOTALL)
    data["Synonyms"] = re_synonyms.search(text).group(0).replace("\n", "")

    re_IUPAC_Name = compile(r'(?<=IUPAC.Name:.).*?(?=InChI)', DOTALL)
    data["Formal Name"] = re_IUPAC_Name.search(text).group(0).replace("\n", "")

    re_inchiString = compile(r'(?<=InChI.String:.).*?(?=CFR)', DOTALL)
    inchi_String = re_inchiString.search(text).group(0).replace("\n", "")
    data["InChI Key"] = InchiToInchiKey(inchi_String)

    re_casNumber = compile(r'(?<=CAS#.).*?(?=\n)')
    data["CAS Number"] = re_casNumber.search(text).group(0)

    # Other informations CAN be in table
    if len(table) in [2, 3]:
        data["Chemical Formula"] = table[-1][1]
        data["Molecular Weight"] = table[-1][2]
        # The table below "2.1 CHEMICAL DATA" can either have 4 or 5 columns, and "Molecular Ion [M+]" can be missing
        if len(table[-1]) == 5:
            data["Molecular Ion [M+]"] = table[-1][3]
        elif len(table[-1]) == 4:
            # In this case, "Molecular Ion [M+]" is not given and me make a good guess based on the "Molecular Weight"
            data["Molecular Ion [M+]"] = int(float(data["Molecular Weight"]))
        else:
            print("Error: Unexpected size of table[-1]")
            return None
        data["Exact Mass [M+H]+"] = table[-1][-1]
    
    elif len(table) == 10 or len(table) == 6:
        # "2.1 CHEMICAL DATA" is not stored as a table, but the informations can be found in the text
        # there are more informations stored in a table, eventhough they are not visible
        # unfortunatly, these informations are not usable
        # example: https://www.cfsre.org/images/monographs/ADB-5Br-BINACA-055622-CFSRE-Chemistry-Report.pdf
        # table extraction delivers: [['', 'ADB-5’Br-BINACA', ''], ['ADB-BINACA', 'ADB-5’Br-BINACA', '5F-ADB-PINACA'], ['', '', ''], [None, '', None], [None, '', None], ['N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-\nyl)-1-Butyl-INdAzole-3-CarboxAmide', 'N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-', 'N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-\nyl)-1-5-FluoroPentyl-INdAzole-3-\nCarboxAmide'], [None, 'yl)-1-Butyl-5-Bromo-INdAzole-3-', None], [None, 'CarboxAmide', None], ['Name: ADB-BINACA', 'Name: ADB-5’Br-BINACA', 'Name: 5F-ADB-PINACA'], ['Synonyms: ADB-BUTINACA', 'Synonyms: ADB-5’Br-BUTINACA', 'Synonyms: N/A']]
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[1]
            text += page.extract_text()

        re_chemical_data = compile(r'(?<=Base ).*?(?=3\. )', DOTALL)
        chemical_data_infos = re_chemical_data.search(text).group(0).split('\n')

        # Building formula from chemical_data_infos
        formula_numbers = chemical_data_infos[1]

        re_formula_letters = compile(r'^[A-Za-z\s]+(?=\d)')
        formula_letters = re_formula_letters.search(chemical_data_infos[0]).group(0).strip()
            
        formula = formula_letters + '\n' + formula_numbers
        data["Chemical Formula"] = formula

        # Extracting "molecular weight", "molecular ion[m+]" and "exact mass[m+h]+"
        re_chemical_data_numbers = compile(r'\b\d[^\n]*')
        chemical_data_numbers = re_chemical_data_numbers.search(chemical_data_infos[0]).group(0).split(" ")
            
        data["Molecular Weight"] = chemical_data_numbers[0]
        data["Molecular Ion [M+]"] = chemical_data_numbers[1]
        data["Exact Mass [M+H]+"] = chemical_data_numbers[-1]
    else:
        print("Error: Cannnot extract pdf because of unknown length of 'table'")
        return None

    return data

"""
Turns String of Synonyms into list of synonyms
"""
def format_synonyms(data):
    synonyms = data["Synonyms"].split(", ")
    synonyms = [s for s in synonyms if s not in ['Not Available', 'Not Applicable', 'None Available']]
    data["Synonyms"] = synonyms
"""
# example: from 'C H N O\n20 19 3 2' to 'C20H19N3O2'
"""
def format_formula(data):
    tmp = data["Chemical Formula"].split("\n")
    letters = tmp[0].split(" ")
    numbers = tmp[1].split(" ")
    
    formula = ""
    for i in range(len(numbers)):
        formula += letters[i] + numbers[i]
    
    if len(letters) == len(numbers)+1:
        formula += letters[-1]
    
    data["Chemical Formula"] = formula

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
    pdf_path = "src\\Webscraper\\pdf samples\\sample1.pdf"

    # Name of the created JSON-file
    #json_filename = 'sample_table_data.json'

    # Relative Path to JSON-files folder
    #directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
    #json_file_path = os.path.join(directory, json_filename)

    print(extract_data_from_pdf(pdf_path))