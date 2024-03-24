from download_helpers import *

# In diesem Programm sollen die Funktionen aus den Modulen importiert werden, um (Test-) Durchläufe zu starten
# Dabei sollen keine weiteren Funktionen neben run_webscraper() implementiert werden

# Hinweis: VSCode gibt mir Fehlermeldungen bezüglich den importierten Funktionen, es funktioniert aber wenn man den Ordner "Webscraper" herunterläd 

def run_webscraper():
    links = create_list_urls()

    # For testing:
    for link in links:
        print(link)
    print("\n")

    for link in links:
        download_pdf(link)
        print("Downloaded: " + link)

        local_pdf_filename = link.split('/')[-1]
        # Missing : Exctract information into .json file

        delete_file(local_pdf_filename)
        print("Deleted: " + local_pdf_filename)
    


if __name__ == '__main__':
        run_webscraper()