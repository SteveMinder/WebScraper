import csv
import datetime
import urllib.parse
from PyQt6.QtWidgets import QFileDialog, QMessageBox

"""
Der Export wurde in eine separate Datei ausgelagert.
Zu einem späteren Zeitpunkt wird er voraussichtlich an eine Datenbank angebunden
(vorgesehen für das 3. Semester im NDS an der TEKO Bern :)) ).

"""
def get_save_path(parent):
    """Öffnet einen Speicherdialog und schlägt einen Dateinamen mit Zeitstempel vor."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"news_export_{timestamp}.csv"

    file_path, _ = QFileDialog.getSaveFileName(parent, "News exportieren", default_filename,
                                               "CSV-Dateien (*.csv);;Alle Dateien (*)")

    return file_path if file_path else None  # Falls abgebrochen, None zurückgeben

def write_news_to_csv(file_path, news_sources, fetch_news, fetch_api_news, tabs):
    """Schreibt die News-Daten in eine CSV-Datei mit Zeitstempel."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Titel", "Kicker", "Bild-URL", "Artikel-URL", "Quelle", "Zeitstempel"])  # Kopfzeile

        # Alle Tabs durchlaufen und News exportieren
        for tab_index in range(tabs.count()):
            tab_name = tabs.tabText(tab_index)
            tab = tabs.widget(tab_index)

            if hasattr(tab, "grid_layout"):
                # **Unterscheiden, ob es sich um TechCrunch API oder Web-Scraping handelt**
                if tab_name == "TechCrunch API":
                    print("[DEBUG] API News werden exportiert...")
                    news = fetch_api_news()
                    source_url = "https://techcrunch.com"
                else:
                    print(f"[DEBUG] Web-Scraping News für {tab_name} werden exportiert...")
                    news = fetch_news(
                        news_sources[tab_name]["url"],
                        news_sources[tab_name]["selectors"]
                    )
                    source_url = news_sources[tab_name]["url"]

                # Nachrichten in die CSV-Datei schreiben
                for item in news:
                    writer.writerow([
                        item.get("title", "N/A"),
                        item.get("kicker", "N/A"),
                        urllib.parse.urljoin(source_url, item.get("image", "")),
                        item.get("link", "N/A"),
                        tab_name,  # Quelle hinzufügen
                        timestamp  # Zeitstempel für jede Zeile hinzufügen
                    ])
def export_news(parent, news_sources, fetch_news, fetch_api_news, tabs):
    """Exportiert die Nachrichten als CSV-Datei mit Fehlerbehandlung."""
    file_path = get_save_path(parent)
    if not file_path:
        return  # Falls der Benutzer den Speichern-Dialog abbricht

    try:
        write_news_to_csv(file_path, news_sources, fetch_news, fetch_api_news, tabs)
        print(f"✅ News erfolgreich exportiert: {file_path}")
    except PermissionError:
        QMessageBox.critical(parent, "Fehler beim Export", "Die Datei ist bereits geöffnet und kann nicht überschrieben werden.\nBitte schließen Sie die Datei und versuchen Sie es erneut.")
    except Exception as e:
        QMessageBox.critical(parent, "Fehler beim Export", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
