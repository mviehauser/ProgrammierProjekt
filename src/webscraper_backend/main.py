import pdf_utils as pdfU
import extract_data as ed

# imports functions from own modules
# No other function besides run_webscraper() will be implemented here

def run_webscraper():
    links = pdfU.create_list_urls()
    
    num_links = len(links)

    for i, link in enumerate(links):
        pdfU.download_pdf(link)
        print(f"Downloaded {link} [{i+1} of {num_links}]")

        local_pdf_filename = link.split('/')[-1]
        # Missing : Extract information into .json file
        data = ed.extract_data_from_pdf(local_pdf_filename)
        if data:
            ed.add_smiles(data)
            ed.format_formula(data)
            ed.format_names(data)
            data["source_url"] = link
            print(data)

        pdfU.delete_file(local_pdf_filename)
        print("Deleted pdf\n")
    

if __name__ == '__main__':
        run_webscraper()