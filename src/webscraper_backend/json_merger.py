import os
import json

def merge_json_files():
    current_directory = os.path.dirname(__file__)
    json_files_directory = os.path.join(current_directory, '..', 'JSON-files', 'extern_JSON-files')
    
    merged_data = []

    for filename in os.listdir(json_files_directory):
        file_path = os.path.join(json_files_directory, filename)

        if not filename.endswith('.json'):
           os.remove(file_path)
           continue

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data.extend(data)
        except json.JSONDecodeError as e:
            print(f"Error reading {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error has occurred with the file {filename}: {e}")

    return merged_data