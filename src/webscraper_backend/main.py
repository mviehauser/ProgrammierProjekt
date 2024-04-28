import json
import logging

# import from own modules
import pdf_utils as pdfU
import extract_data as ed
from constants import CFSRE_URL
import logger_config

# No other function besides run_webscraper() will be implemented here

def run_webscraper():
    listData = []

    links = pdfU.create_list_urls()
    num_links = len(links)
    num_failed_extractions = 0

    # If you want to change shown logging level, change the argument in setup_logger(level=)
    logger = logger_config.setup_logger(level=logging.DEBUG)
    logger.info(f"Found {num_links} links on {CFSRE_URL}")

    for i, link in enumerate(links):
        pdfU.download_pdf(link)

        local_pdf_filename = link.split('/')[-1]
        
        data = ed.extract_data_from_pdf(local_pdf_filename)
        if data:
            ed.add_smiles(data)
            ed.format_formula(data)
            ed.format_names(data)
            data["source_url"] = link
            listData.append(data)
            logger.info(f"Successfully extracted {link} [{i+1}/{num_links}]")
        else:
             num_failed_extractions += 1
             logger.error(f"Failed to extract link #{i+1} {link}")
            
        pdfU.delete_file(local_pdf_filename)

    logger.info(f"Extracted {num_links - num_failed_extractions} / {num_links} PDFs")
    # for testing: (maybe later a name is being produced dynamically, depending on the date or version of the webscraper)
    json_path = "src\\JSON-files\\test.json"
    with open(json_path, mode="w") as json_file:
         json.dump(listData, json_file, indent=4)
    
    logger.info("Created .json-file ({json_path}) and finished the scraping-process.")
    

if __name__ == '__main__':
        run_webscraper()