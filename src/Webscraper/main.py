from pdf_downloader import *
from json_converter_paul import *

# imports functions from own modules
# No other function besides run_webscraper() will be implemented here

def run_webscraper():
    links = create_list_urls()
    # For testing:
    for link in links:
        print(link)
    print("\n")

    num_links = len(links)

    for i, link in enumerate(links):
        download_pdf(link)
        print(f"Downloaded: {link} [{i+1} of {num_links}]")


        local_pdf_filename = link.split('/')[-1]
        # Missing : Exctract information into .json file
        print(extract_data_from_pdf(local_pdf_filename))

        delete_file(local_pdf_filename)
        print("Deleted: " + local_pdf_filename + "\n")
    


if __name__ == '__main__':
        run_webscraper()