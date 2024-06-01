import json
import logging

import pdf_utils as pdfU
import extract_data as ed
from validation import validate_data
from constants import CFSRE_URL
import pathmanagement
import logger_config
import incremental_loading as incL

def run_webscraper(mode):
    incL.check_mode(mode)
    JSON_PATH, LINK_ARCHIVE_PATH, JS_DATA_PATH, LOG_PATH = pathmanagement.create_file_paths()
    # If you want to change shown logging level, change the argument in setup_logger(level=)
    logger = logger_config.setup_logger(LOG_PATH, level=logging.DEBUG)
    logger.info(f"Programm is starting in mode {mode}")

    found_links = pdfU.create_list_urls()
    logger.info(f"Found {len(found_links)} links on {CFSRE_URL}")

    date_strings = incL.fetch_date_strings()

    if mode == 1:
        data_collection = []
        # In mode 1, all links in found_links will be extracted
        links_to_extract = found_links
    else:
        data_collection = incL.load_existing_data(JSON_PATH)
        logger.info(f"Loaded data.json with {len(data_collection)} substances")

        with open(LINK_ARCHIVE_PATH, 'r') as f:
            archived_links = json.load(f)
        logger.info(f"Loaded link_archive.json with {len(archived_links)} links that were found in the past")
        links_to_extract = [x for x in found_links if x not in archived_links]
        logger.info(f"{len(links_to_extract)} links are new on this site")
    
    if len(links_to_extract) == 0:
        logger.info("There are no new files to extract. Ending the programm.")
        exit()
    
    num_failed_extractions = 0

    for i, link in enumerate(links_to_extract):
        pdfU.download_pdf(link)

        local_pdf_filename = link.split('/')[-1]
        
        data = ed.extract_data_from_pdf(local_pdf_filename)
        if data:
            ed.add_smiles(data)
            ed.format_formula(data)
            ed.format_names(data)
            data["source_url"] = link
            validate_data(data)
            data["last_modified"] = date_strings[i]
            data_collection.append(data)
            logger.info(f"Successfully extracted {link} [{i+1}/{len(links_to_extract)}]")
        else:
            num_failed_extractions += 1
            logger.error(f"Failed to extract {link} [{i+1}/{len(links_to_extract)}]")
            
        pdfU.delete_file(local_pdf_filename)

    logger.info(f"Was able to extract {len(links_to_extract) - num_failed_extractions} / {len(links_to_extract)} PDFs")
    # Create a link archive that helps with incremential loading
    incL.archive_links(found_links, LINK_ARCHIVE_PATH)
    
    with open(JSON_PATH, mode="w") as json_file:
        json.dump(data_collection, json_file, indent=4)
    logger.info(f"Created json-file with {len(data_collection)} substances under {JSON_PATH}.")

    # Create a .js file for the frontend
    js_code = f"const Data = {json.dumps(data_collection)}"
    with open(JS_DATA_PATH, mode="w") as js_file:
        js_file.write(js_code)
    logger.info(f"Created javascript-file under {JS_DATA_PATH} and finished the scraping-process.")

if __name__ == '__main__':
        # Give run_webscraper one of the following arguments:
        # mode=1, load everything completely new
        # mode=2, load only new Substances
        # currently missing mode=3, load new Substances as well as changes to existing data
        run_webscraper(2)