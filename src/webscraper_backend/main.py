from pdf_downloader import *
from Webscraper.extract_data import *
from constants import *

# imports functions from own modules
# No other function besides run_webscraper() will be implemented here

def run_webscraper():
    links = create_list_urls()
    
    num_links = len(links)

    for i, link in enumerate(links):
        download_pdf(link)
        print(f"Downloaded {link} [{i+1} of {num_links}]")

        local_pdf_filename = link.split('/')[-1]
        # Missing : Extract information into .json file
        data = extract_data_from_pdf(local_pdf_filename)
        if data:
            add_smiles(data)
            format_formula(data)
            format_names(data)
            data["source_url"] = link
            print(data)

        delete_file(local_pdf_filename)
        print("Deleted pdf\n")
    

if __name__ == '__main__':
        run_webscraper()