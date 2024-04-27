# Programmier-Projekt
This repository is for the programming project SoSe2024 from Paul Potsch and Maximilian Viehauser.

Die zu scrapendene Website ist [cfsre](https://www.cfsre.org/nps-discovery/monographs), wobei einige wichtige Informationen ausschließlich in PDFs auffindbar sind.


## Struktur
Unter dem Ordner 'src' befindet sich der Sourcecode:
- **webscraper_backend**: Beschaffung der Informationen mittels Python, die in einer .json-Datei abgespeichert werden.
- **webscraper_frontend**: Visualisierung der Daten sowie Suchmaschine.
## Anforderungen

Um dieses Projekt zu verwenden, benötigen Sie Folgendes:

- **Python**: Eine aktuelle Python-Version. Das Projekt wurde mit Python 3.12.2 getestet.
- **Bibliotheken**: Es werden einige Bibliotheken verwendet, die nicht Teil der Python-Standardbibliothek sind. Diese können mit pip wie folgt installiert werden:

    ```bash
    pip install pdfplumber rdkit requests beautifulsoup4
    ```