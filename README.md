# Programmier-Projekt
Dieses Repository dient für das Prgrammier-Projekt von Paul Potsch und Maximilian Viehauser im SoSe2024.

Der Webscraper basiert auf der Website des [cfsre](https://www.cfsre.org/nps-discovery/monographs). Alle Informationen zu den "Designer Drugs" befinden sich in den .pdf-Dateien auf der Seite.


## Struktur
Unter dem Ordner 'src' befindet sich der Sourcecode:
- **webscraper_backend**: Beschaffung der Informationen mittels Python, die in einer .json-Datei sowie in einer .js-Datei abgespeichert werden.
- **webscraper_frontend**: Visualisierung der Daten sowie Suchmaschine.
- **JSON-files**: Speicherung der Daten, welche das Backend erzeugt hat


## Anforderungen
Um dieses Projekt zu verwenden, benötigen Sie Folgendes:
- **Visual Studio Code**: Eine Entwicklungsumgebung, mit der sowohl das backend, als auch das frontend bedient werden kann.
- **Live Server Extension**: Nach dem Öffnen der IDE VS Code muss der Reiter "Extensions" (Links am Rand) geöffnet werden und nach der Extension "Live Server" gesucht werden. Diese Extension muss anschließend installiert werden.
- **Python**: Eine aktuelle Python-Version. Das Projekt wurde mit Python 3.12.2 getestet.
- **Bibliotheken**: Es werden einige Bibliotheken verwendet, die nicht Teil der Python-Standardbibliothek sind. Diese können mit pip wie folgt installiert werden:

    ```bash
    pip install pdfplumber rdkit requests beautifulsoup4
    ```

## Benutzung
- **webscraper_backend**: Innerhalb des ProgrammierProjekt-Ordners "main.py" ausführen und abwarten bis das Programm fertig ist.
- **webscraper_frontend**: "index.html" mit einem Browser öffnen. TIPP: Bedienen Sie die Website auf Englisch.