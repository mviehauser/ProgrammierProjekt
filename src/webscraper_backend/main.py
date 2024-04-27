import json

import pdf_utils as pdfU
import extract_data as ed

# imports functions from own modules
# No other function besides run_webscraper() will be implemented here

def run_webscraper():
    listData = []
    # for testing: (maybe later a name is being produced dynamically, depending on the date or version of the webscraper)
    json_path = "src\\JSON-files\\test.json"

    links = pdfU.create_list_urls()
    
    num_links = len(links)

    for i, link in enumerate(links):
        pdfU.download_pdf(link)
        print(f"Downloaded {link} [{i+1} of {num_links}]")

        local_pdf_filename = link.split('/')[-1]
        
        data = ed.extract_data_from_pdf(local_pdf_filename)
        if data:
            ed.add_smiles(data)
            ed.format_formula(data)
            ed.format_names(data)
            data["source_url"] = link
            listData.append(data)
            

        pdfU.delete_file(local_pdf_filename)
        print("Deleted pdf\n")
    
    with open(json_path, mode="w") as json_file:
         json.dump(listData, json_file, indent=4)
    

if __name__ == '__main__':
        run_webscraper()