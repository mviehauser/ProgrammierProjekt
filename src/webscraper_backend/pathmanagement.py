import os

def create_file_paths():
    current_dir = os.getcwd()
    if "webscraper_backend" in current_dir:
        webscraper_backend_dir = current_dir
        src_dir = os.path.abspath(os.path.join(webscraper_backend_dir, ".."))

    elif "src" in current_dir:
        src_dir = current_dir
        webscraper_backend_dir = os.path.join(src_dir, "webscraper_backend")

    else:
        ProgrammierProjekt_dir = current_dir
        src_dir = os.path.join(ProgrammierProjekt_dir, "src")
        webscraper_backend_dir = os.path.join(src_dir, "webscraper_backend")
    

    JSON_dir = os.path.join(src_dir, "JSON-files")

    JSON_PATH = os.path.join(JSON_dir, "data.json")

    JSON_ALL_PATH = os.path.join(JSON_dir, "all_data.json")

    LINK_ARCHIVE_PATH = os.path.join(JSON_dir, "link_archive.json")

    JS_DATA_PATH = os.path.join(JSON_dir, "js_data.js")

    LOG_PATH = os.path.abspath(os.path.join(webscraper_backend_dir, "scraper.log"))

    return JSON_PATH, LINK_ARCHIVE_PATH, JS_DATA_PATH, LOG_PATH, JSON_ALL_PATH

if __name__ == "__main__":
    print(create_file_paths())