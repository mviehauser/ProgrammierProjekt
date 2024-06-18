import os
import json

def merge_json_files():

    # Definieren des Pfads zum Ordner mit den JSON-files
    current_directory = os.path.dirname(__file__)
    json_files_directory = os.path.join(current_directory, '..', 'JSON-files', 'extern_JSON-files')
    
    # Initialisieren einer leeren Liste zum speichern aller Daten
    merged_data = []

    # Durchlaufe alle Dateien im Verzeichnis
    for filename in os.listdir(json_files_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(json_files_directory, filename)
            try:
                # Öffne die JSON-Datei und lade die Daten
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Füge die Daten zur Liste hinzu
                    merged_data.extend(data)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
            except Exception as e:
                print(f"An unexpected error has occurred with the file {filename}: {e}")

    return merged_data

