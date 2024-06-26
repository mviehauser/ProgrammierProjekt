import os

def create_file_paths():
    webscraper_backend_dir = os.path.dirname(__file__)
    src_dir = os.path.dirname(webscraper_backend_dir)  

    JSON_dir = os.path.join(src_dir, "JSON-files")

    JSON_PATH = os.path.join(JSON_dir, "data.json")

    JSON_ALL_PATH = os.path.join(JSON_dir, "all_data.json")

    LINK_ARCHIVE_PATH = os.path.join(JSON_dir, "link_archive.json")

    JS_DATA_PATH = os.path.join(JSON_dir, "js_data.js")

    LOG_PATH = os.path.abspath(os.path.join(webscraper_backend_dir, "scraper.log"))

    return JSON_PATH, LINK_ARCHIVE_PATH, JS_DATA_PATH, LOG_PATH, JSON_ALL_PATH

if __name__ == "__main__":
    print(create_file_paths())