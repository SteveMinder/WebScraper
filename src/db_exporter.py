# db_exporter.py
import datetime  # 📆 Für Zeitstempel beim Speichern der News
from database import init_db, insert_news  # 🔌 Import der Datenbankfunktionen

# ===============================================
# 💾 EXPORTIERT ALLE NEWS-TABS IN DIE DATENBANK
# ===============================================
def export_news_to_db(news_sources, fetch_news, fetch_api_news, tabs):
    """
    Exportiert Nachrichten aus allen Tabs (Web-Scraping & API) in die SQLite-Datenbank
    und zeigt für jede Quelle an, wie viele neue Artikel gespeichert wurden.

    Args:
        news_sources (dict): Enthält URLs und Selektoren für die Scraping-Quellen.
        fetch_news (function): Funktion zum Abrufen von Web-Scraping-News.
        fetch_api_news (function): Funktion zum Abrufen von API-News.
        tabs (QTabWidget): Das Tab-Widget mit allen Nachrichtenquellen.
    """
    init_db()  # 🛠️ Initialisiere die Datenbank (erstellt Tabelle bei Bedarf)

    # 🕒 Aktueller Zeitstempel für alle Einträge
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔁 Alle Tabs (Quellen) durchlaufen
    for tab_index in range(tabs.count()):
        tab_name = tabs.tabText(tab_index)  # 📛 Name des Tabs (z.B. "Nau", "TechCrunch [API]")
        tab = tabs.widget(tab_index)        # 🧱 Zugriff auf das Tab-Objekt

        if hasattr(tab, "grid_layout"):
            # 📡 API-Tab
            if tab_name == "TechCrunch [API]":
                news = fetch_api_news()
            else:
                # 🌍 Web-Scraping-Tab
                news = fetch_news(
                    news_sources[tab_name]["url"],
                    news_sources[tab_name]["selectors"]
                )

            # 💾 News in die Datenbank einfügen und Anzahl neuer Einträge erfassen
            new_count = insert_news(news, tab_name, timestamp)

            # 📣 Konsolenausgabe für diese Quelle
            print(f"🆕 {new_count} neue Artikel aus '{tab_name}' gespeichert.")

    # ✅ Abschliessende Erfolgsmeldung
    print("✅ Alle Quellen erfolgreich in die Datenbank exportiert.")
