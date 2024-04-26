from json import dump
import pdfplumber
from constants import DATA
from rdkit.Chem.inchi import InchiToInchiKey
from rdkit.Chem import  MolFromInchi
from rdkit.Chem.rdmolfiles import MolToSmiles
from re import compile, search, DOTALL

"""
Args:
- pdf-Path
- (int) page_to_extract
"""
def extract_table_text_pdfPage(pdf_path, page_to_extract):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_to_extract]
        text = page.extract_text()
        if x := page.extract_table():
            return x, text
        else:
            return [], text

"""
There are at least 3 different types of pdfs, with different internal structure:
    Type 1 "NPS Discovery (new)" : https://www.cfsre.org/images/monographs/Medetomidine-New-Drug-Monograph-NPS-Discovery-112723.pdf
    Type 2 "NPS Discovery (old)" : https://www.cfsre.org/images/monographs/BZO-POXIZID_101921_CFSRE_Chemistry_Report.pdf 
    Type 3 "NMS LABS" : https://www.cfsre.org/images/monographs/25E-NBOH_022718_NMSLabs_Report.pdf

Type 1 has all the important information on the first page in a table and definies which infos have to be in DATA
Type 2+ does not have every information in a table, therefore regular expressions and text extraction is needed.
"""
def extract_data_from_pdf(pdf_path):
    data = DATA.copy()
    table, text = extract_table_text_pdfPage(pdf_path, 0)
    
    if len(table) == 9:
        # This is Type 1
        if table[0][0] == "Preferred Name":
            data["names"] = [table[0][1]]
            data["names"] += table[1][1].split(", ")
            data["iupac_name"] = table[2][1]
            data["inchi_key"] = table[3][1]
            data["cas_num"] = table[4][1]
            data["formula"] = table[5][1]
            data["molecular_mass"] = table[6][1]
            data["molecular_ion_[m+]"] = table[7][1]
            data["exact_mass_[m+h]+"] = table[8][1]
            # Classes:
            re_class = compile(r'(?<=NPS SUBCLASS\n).*?(?=\n)')
            data["classes"] = [re_class.search(text).group(0)]
        else:
            print("Error: Expected 'Preferred Name' in table[0][0]")
            data = None
        return data
    
    # This is Type 2+
    # Information(text and table) of page 2 is also needed
    next_page_table, next_page_text = extract_table_text_pdfPage(pdf_path, 1)
    table += next_page_table
    text += next_page_text

    # Preferred Name in text
    t = text.split('\n')
    if "NMS Labs" in t[0]:
        if '&' in t[3] or 'and' in t[3]:
            print("Error: Two chemicals in one pdf")
            return None
        data["names"] = [t[3]]
    elif "The Center for Forensic Science Research and Education" in t[0]:
        data["names"] = [t[4]]
    else:
        data["names"] = [t[0]]
    
    # These Data-keys are only to be found in the text by RegExps
    # DOTALL used, when the RegEx can be spread over multiple lines
    re_synonyms = compile(r'(?<=Synonyms:.).*?(?=Source|Important)', DOTALL)
    data["names"] += re_synonyms.search(text).group(0).replace("\n", "").split(", ")

    re_IUPAC_Name = compile(r'(?<=IUPAC.Name:.).*?(?=InChI)', DOTALL)
    data["iupac_name"] = re_IUPAC_Name.search(text).group(0).replace("\n", "")

    re_inchiString = compile(r'(?<=InChI.String:.).*?(?=CFR| )', DOTALL)
    data["inchi"] = re_inchiString.search(text).group(0).replace("\n", "")
    data["inchi_key"] = InchiToInchiKey(data["inchi"])

    re_casNumber = compile(r'(?<=CAS#.).*?(?=\n)')
    data["cas_num"] = re_casNumber.search(text).group(0)

    re_class = compile(r'(?<=classified as a )(?:novel |synthetic (?:\(or novel\) )?|substituted |suspected |)?.*?(?: analogue| precursor)?(?= |\.|\,|\;)')
    if x:=re_class.search(text):
        data["classes"] = [x.group(0).title()]
    elif "is classified as an analogue of the fentanyl precursor" in text:
        data["classes"] = ["Fentanyl Precursor"]
    elif "is a synthetic hallucinogen and analogue of LSD" in text:
        data["classes"] = ["Hallucinogen", "LSD Analoge"]

    # Other informations CAN be in table
    if len(table) in [2, 3]:
        data["formula"] = table[-1][1]
        data["molecular_mass"] = table[-1][2]
        # The table below "2.1 CHEMICAL DATA" can either have 4 or 5 columns, and "Molecular Ion [M+]" can be missing
        if len(table[-1]) == 5:
            data["molecular_ion_[m+]"] = table[-1][3]
        elif len(table[-1]) == 4:
            # In this case, "Molecular Ion [M+]" is not given and we make a good guess based on the "Molecular Weight"
            data["molecular_ion_[m+]"] = int(float(data["molecular_mass"]))
        else:
            print("Error: Unexpected size of table[-1]")
            return None
        data["exact_mass_[m+h]+"] = table[-1][-1]
    
    elif len(table) == 10 or len(table) == 6:
        # "2.1 CHEMICAL DATA" is not stored as a table, but the informations can be found in the text
        # there are more informations stored in a table, eventhough they are not visible
        # unfortunatly, these informations are not usable
        # example: https://www.cfsre.org/images/monographs/ADB-5Br-BINACA-055622-CFSRE-Chemistry-Report.pdf
        # table extraction delivers: [['', 'ADB-5’Br-BINACA', ''], ['ADB-BINACA', 'ADB-5’Br-BINACA', '5F-ADB-PINACA'], ['', '', ''], [None, '', None], [None, '', None], ['N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-\nyl)-1-Butyl-INdAzole-3-CarboxAmide', 'N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-', 'N-(1-Amino-3,3-Dimethyl-1-oxoButan-2-\nyl)-1-5-FluoroPentyl-INdAzole-3-\nCarboxAmide'], [None, 'yl)-1-Butyl-5-Bromo-INdAzole-3-', None], [None, 'CarboxAmide', None], ['Name: ADB-BINACA', 'Name: ADB-5’Br-BINACA', 'Name: 5F-ADB-PINACA'], ['Synonyms: ADB-BUTINACA', 'Synonyms: ADB-5’Br-BUTINACA', 'Synonyms: N/A']]

        re_chemical_data = compile(r'(?<=Base ).*?(?=3\. )', DOTALL)
        chemical_data_infos = re_chemical_data.search(text).group(0).split('\n')

        # Building formula from chemical_data_infos
        formula_numbers = chemical_data_infos[1]

        re_formula_letters = compile(r'^[A-Za-z\s]+(?=\d)')
        formula_letters = re_formula_letters.search(chemical_data_infos[0]).group(0).strip()
            
        formula = formula_letters + '\n' + formula_numbers
        data["formula"] = formula

        # Extracting "molecular weight", "molecular ion[m+]" and "exact mass[m+h]+"
        re_chemical_data_numbers = compile(r'\b\d[^\n]*')
        chemical_data_numbers = re_chemical_data_numbers.search(chemical_data_infos[0]).group(0).split(" ")
            
        data["molecular_mass"] = chemical_data_numbers[0]
        data["molecular_ion_[m+]"] = chemical_data_numbers[1]
        data["exact_mass_[m+h]+"] = chemical_data_numbers[-1]
    else:
        print("Error: Cannnot extract pdf because of unknown length of 'table'")
        return None

    return data

def format_names(data):
    for x in ['Not Available', 'None Available', 'Not Applicable']:
        if x in data["names"][1:]:
            data["names"].remove(x)

"""
Edits data["formula"] by removing '\n' and combining the two lines
# example: from 'C H N O\n20 19 3 2' to 'C20H19N3O2'
"""
def format_formula(data):
    tmp = data["formula"].split("\n")
    letters = tmp[0].split(" ")
    numbers = tmp[1].split(" ")
    
    formula = ""
    for i in range(len(numbers)):
        formula += letters[i] + numbers[i]
    
    if len(letters) == len(numbers)+1:
        formula += letters[-1]
    
    data["formula"] = formula

def add_smiles(data):
    if i:=data["inchi"]:
        mol = MolFromInchi(i)
        if mol is None:
            return "Invalid InChIKey"
        smiles = MolToSmiles(mol, canonical = True)
        data["smiles"] = smiles
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
    pdf_path = "src\\Webscraper\\pdf samples\\FluoroFuranylfentanyl_012319_ToxicologyAnalyticalReport.pdf"

    # Name of the created JSON-file
    #json_filename = 'sample_table_data.json'

    # Relative Path to JSON-files folder
    #directory = os.path.join(os.path.dirname(__file__), '..', 'JSON-files')
    #json_file_path = os.path.join(directory, json_filename)

    data = extract_data_from_pdf(pdf_path)
    add_smiles(data)
    format_formula(data)
    format_names(data)
    print(data)