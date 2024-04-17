import json
import os
import pdfplumber


def extract_tables_from_pdf(pdf_path):
    tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(table)

    return tables

    def save_tables_as_json(tables, json_file):
        formatted_tables = []

    for table in tables:
        formatted_table = {
            "Preferred Name": table[0][0],
            "Synonyms": table[0][1],
            "Formal Name": table[0][2],
            "InChI Key": table[0][3],
            "CAS Number": table[0][4],
            "Chemical Formula": table[0][5],
            "Molecular Weight": table[0][6],
            "Molecular Ion [M+]": table[0][7],
            "Exact Mass [M+H]+": table[0][8],
        }
        formatted_tables.append(formatted_table)

    with open(json_file, 'w') as f:
        json.dump(formatted_tables, f, indent=4)


# Example usage
pdf_path = 'sample2.pdf'

tables =  extract_tables_from_pdf(pdf_path)
print(tables)