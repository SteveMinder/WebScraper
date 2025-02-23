import csv
import datetime
import urllib.parse
from PyQt6.QtWidgets import QFileDialog, QMessageBox

"""
📌 Modul für den Export von News-Daten als CSV-Datei.

✅ Der Export wurde in eine separate Datei ausgelagert, um den Code sauberer zu strukturieren.
✅ In zukünftigen Versionen wird er voraussichtlich mit einer Datenbank verknüpft.
   (Geplant für das 3. Semester im NDS an der TEKO Bern 🚀).
"""

# ============================
# 📂 DATEIPFAD FÜR EXPORT WÄHLEN
# ============================

def get_save_path(parent):
    """
    Öffnet einen Dialog zur Auswahl des Speicherorts und schlägt einen Dateinamen mit Zeitstempel vor.

    Args:
        parent (QWidget): Das übergeordnete Widget (z. B. das Hauptfenster).

    Returns:
        str | None: Der gewählte Dateipfad oder `None`, wenn der Dialog abgebrochen wird.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 🕒 Zeitstempel für Dateinamen
    default_filename = f"news_export_{timestamp}.csv"

    file_path, _ = QFileDialog.getSaveFileName(
        parent,
        "News exportieren",
        default_filename,
        "CSV-Dateien (*.csv);;Alle Dateien (*)"
    )

    return file_path if file_path else None  # Falls abgebrochen, None zurückgeben


# ============================
# 📝 CSV-SCHREIBFUNKTION
# ============================

def write_news_to_csv(file_path, news_sources, fetch_news, fetch_api_news, tabs):
    """
    Schreibt Nachrichten in eine CSV-Datei mit Zeitstempel.

    Args:
        file_path (str): Der Speicherort der CSV-Datei.
        news_sources (dict): Dictionary mit Web-Scraping-Quellen (URLs & Selektoren).
        fetch_news (function): Funktion zum Abrufen der Nachrichten von Webseiten.
        fetch_api_news (function): Funktion zum Abrufen der Nachrichten von der TechCrunch API.
        tabs (QTabWidget): Tab-Widget, das die verschiedenen News-Tabs enthält.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 🕒 Aktueller Zeitstempel

    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Titel", "Kicker", "Bild-URL", "Artikel-URL", "Quelle", "Zeitstempel"])  # 🏷️ CSV-Kopfzeile

        # 🔄 Alle Tabs durchlaufen und die jeweiligen Nachrichten exportieren
        for tab_index in range(tabs.count()):
            tab_name = tabs.tabText(tab_index)
            tab = tabs.widget(tab_index)

            if hasattr(tab, "grid_layout"):
                # 🌍 Unterscheidung zwischen Web-Scraping und API-Tab
                if tab_name == "TechCrunch [API]":
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

                # ✍️ Nachrichten in die CSV-Datei schreiben
                for item in news:
                    writer.writerow([
                        item.get("title", "N/A"),  # 📰 Nachrichtentitel
                        item.get("kicker", "N/A"),  # 📌 Kicker (Untertitel)
                        urllib.parse.urljoin(source_url, item.get("image", "")),  # 🖼️ Bild-URL
                        item.get("link", "N/A"),  # 🔗 Artikel-Link
                        tab_name,  # 🌍 Quelle (Webseite oder API)
                        timestamp  # ⏳ Zeitpunkt des Exports
                    ])


# ============================
# 📤 EXPORT-LOGIK MIT FEHLERHANDLING
# ============================

def export_news(parent, news_sources, fetch_news, fetch_api_news, tabs):
    """
    Startet den Exportprozess der Nachrichten als CSV-Datei mit Fehlerbehandlung.

    Args:
        parent (QWidget): Das übergeordnete Widget (z. B. Hauptfenster).
        news_sources (dict): Dictionary mit den Nachrichtenquellen.
        fetch_news (function): Funktion zum Abrufen von Nachrichten über Scraping.
        fetch_api_news (function): Funktion zum Abrufen von API-Nachrichten.
        tabs (QTabWidget): Tab-Widget mit den Nachrichten-Tabs.
    """
    file_path = get_save_path(parent)  # 📂 Speicherort abrufen
    if not file_path:
        return  # Falls der Benutzer den Speichern-Dialog abbricht

    try:
        write_news_to_csv(file_path, news_sources, fetch_news, fetch_api_news, tabs)
        print(f"✅ News erfolgreich exportiert: {file_path}")  # 🟢 Erfolgreiche Meldung
    except PermissionError:
        QMessageBox.critical(
            parent,
            "Fehler beim Export",
            "Die Datei ist bereits geöffnet und kann nicht überschrieben werden.\n"
            "Bitte schließen Sie die Datei und versuchen Sie es erneut."
        )
    except Exception as e:
        QMessageBox.critical(
            parent,
            "Fehler beim Export",
            f"Ein unerwarteter Fehler ist aufgetreten:\n{e}"
        )
