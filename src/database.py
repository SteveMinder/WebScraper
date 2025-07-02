# database.py
import sqlite3  # 📦 Import des SQLite-Moduls für lokale Datenbankzugriffe

# ===============================
# 📁 INITIALISIERT DIE DATENBANK
# ===============================
def init_db(db_name="news.db"):
    """
    Erstellt (falls nicht vorhanden) die SQLite-Datenbank und die Tabelle 'news'.

    Args:
        db_name (str): Der Name der SQLite-Datenbankdatei. Standard: "news.db"
    """
    conn = sqlite3.connect(db_name)  # 🔌 Verbindung zur SQLite-Datenbank herstellen
    c = conn.cursor()                # 🧠 Cursor-Objekt für SQL-Befehle erzeugen

    # 📦 Tabelle 'news' anlegen, falls sie noch nicht existiert
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 🔑 Eindeutige ID (wird automatisch hochgezählt)
            title TEXT,                             -- 📰 Titel des Artikels
            kicker TEXT,                            -- 📌 Untertitel oder Kategorie
            image TEXT,                             -- 🖼️ Bild-URL
            link TEXT,                              -- 🔗 Artikel-Link
            source TEXT,                            -- 🌐 Nachrichtenquelle (z. B. "Nau", "TechCrunch")
            timestamp TEXT,                         -- 🕒 Zeitstempel des Eintrags
            UNIQUE(title, link)                     -- 🔁 Kombination aus Titel & Link muss eindeutig sein
        )
    ''')

    conn.commit()   # 💾 Änderungen dauerhaft speichern
    conn.close()    # 🔒 Verbindung zur Datenbank schliessen


# =============================================
# 📝 FÜGT ARTIKEL IN DIE DATENBANK EIN (OHNE DUPLIKATE)
# =============================================
def insert_news(news_items, source, timestamp, db_name="news.db"):
    """
    Fügt eine Liste von Nachrichtenartikeln in die Datenbank ein und zählt, wie viele neue Datensätze wirklich gespeichert wurden.

    Args:
        news_items (list): Liste von Dictionaries mit den Artikeldaten.
        source (str): Name der Nachrichtenquelle.
        timestamp (str): Zeitstempel des Exports.
        db_name (str): Datenbankdatei. Standard: "news.db"

    Returns:
        int: Anzahl der neu eingefügten Artikel (Duplikate werden ignoriert).
    """
    conn = sqlite3.connect(db_name)  # 🔌 Verbindung zur Datenbank
    c = conn.cursor()                # 🧠 Cursor erstellen
    inserted_count = 0              # 📊 Zähler für neu eingefügte Artikel

    for item in news_items:
        try:
            # ⬇️ Versuche, einen Artikel einzufügen (wird ignoriert, wenn Titel+Link schon vorhanden)
            c.execute('''
                INSERT OR IGNORE INTO news (title, kicker, image, link, source, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item.get("title", "N/A"),      # 📰 Titel des Artikels (oder "N/A" als Fallback)
                item.get("kicker", "N/A"),     # 📌 Untertitel (Kategorie)
                item.get("image", "N/A"),      # 🖼️ Bild-URL
                item.get("link", "N/A"),       # 🔗 Artikel-Link
                source,                        # 🌐 Quelle (wird übergeben)
                timestamp                      # 🕒 Zeitstempel
            ))

            # ✅ Prüfe, ob der Eintrag wirklich neu ist (rowcount = 1)
            if c.rowcount > 0:
                inserted_count += 1

        except Exception as e:
            # ❌ Fehler beim Einfügen eines Artikels (z.B. ungültige Daten)
            print(f"[Fehler beim Einfügen] {item.get('title')} → {e}")

    conn.commit()   # 💾 Änderungen speichern
    conn.close()    # 🔒 Verbindung beenden

    # 📣 Ausgabe: wie viele Artikel neu waren
    print(f"🆕 {inserted_count} neue Artikel aus '{source}' hinzugefügt.")
    return inserted_count  # 🔁 Rückgabe der Anzahl neuer Einträge
