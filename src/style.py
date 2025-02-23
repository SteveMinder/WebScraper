# =========================
# 🖥️ STYLESHEET FÜR main.py
# =========================

# 🎨 Hauptstil für das gesamte Fenster
MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #121212;  /* Dunkler Hintergrund für Dark Mode */
        color: #e0e0e0;             /* Helle Schriftfarbe für Kontrast */
        font-family: 'Arial';       /* Standard-Schriftart */
    }
"""

# 📌 Stil für den Überschrift-Label (Header)
HEADER_STYLE = """
    font-size: 22px;          /* Größere Schrift für den Titel */
    font-weight: bold;        /* Fettgedruckt für mehr Sichtbarkeit */
    color: #00a8e8;          /* Blaue Farbe für visuelle Hervorhebung */
    padding: 5px;            /* Leichte Polsterung für bessere Lesbarkeit */
"""

# 🎛️ Stil für allgemeine Buttons (z. B. Aktualisieren)
BUTTON_STYLE = """
    QPushButton {
        background-color: #1e1e1e;  /* Dunkler Button-Hintergrund */
        color: white;               /* Weiße Schriftfarbe */
        font-size: 10px;            /* Kleinere Schriftgröße */
        font-weight: bold;          /* Fett für bessere Lesbarkeit */
        border: none;               /* Kein Rand für ein modernes Design */
        border-radius: 2px;         /* Leicht abgerundete Ecken */
        padding: 8px 16px;          /* Innenabstand für bessere Klickbarkeit */
        transition: background-color 0.3s;  /* Sanfter Hover-Effekt */
    }
    QPushButton:hover {
        background-color: #004080;  /* Dunkleres Blau beim Überfahren */
    }
    QPushButton:pressed {
        background-color: #004080;  /* Gleiches Blau beim Klicken */
    }
"""

# 🛠️ Stil für den Export-Button (leicht angepasst für Layout-Flexibilität)
EXPORT_BUTTON_STYLE = """
    QPushButton {
        background-color: #1e1e1e;  /* Dunkler Hintergrund */
        color: white;               /* Weiße Schrift */
        font-size: 10px;            /* Kleinere Schrift */
        font-weight: bold;
        border: none;
        border-radius: 2px;
        padding: 8px 16px;
        margin-left: 11px;          /* Leichter Abstand nach links */
        width: 179px;               /* Feste Breite */
        min-width: 150px;           /* Mindestbreite */
        max-width: 200px;           /* Maximale Breite, um zu große Buttons zu vermeiden */
    }
    QPushButton:hover {
        background-color: #004080;  /* Farbänderung beim Hover */
    }
    QPushButton:pressed {
        background-color: #004080;  /* Farbänderung beim Klicken */
    }
"""

# 📰 Stil für News-Karten (Container für Nachrichtenartikel)
CARD_STYLE = """
    background-color: #1e1e1e;  /* Dunkler Hintergrund */
    border-radius: 12px;        /* Abgerundete Ecken für modernes Design */
    padding: 6px;               /* Innenabstand für Inhalt */
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);  /* Leichter Schatten für mehr Tiefe */
"""

# 🔄 Stil für die Tabs (Kategoriebereiche)
TAB_WIDGET_STYLE = """
    QTabBar::tab {
        background-color: #1e1e1e;  /* Dunkler Tab-Hintergrund */
        min-width: 80px;            /* Mindestbreite für Tabs */
        min-height: 20px;           /* Mindesthöhe für Tabs */
        margin-left: 11px;          /* Abstand zwischen den Tabs */
        padding: 5px 10px;          /* Innenabstand für bessere Klickbarkeit */
        font-size: 10px;            /* Kleinere Schriftgröße */
        font-weight: bold;
        border-radius: 2px;
        color: white;               /* Weiße Schrift */
    }

    QTabBar::tab:hover {
        background: #004080;  /* Blaue Hervorhebung beim Überfahren */
    }
"""

# 🖼️ Stil für Bilder in den News-Karten
IMAGE_STYLE = """
    border-radius: 8px;        /* Abgerundete Ecken für weiche Kanten */
    background-color: #2c2c2c; /* Leicht dunkler Hintergrund */
    padding: 5px;              /* Abstand zwischen Bild und Rand */
"""

# 📰 Stil für Titel in den News-Karten
TITLE_STYLE = "font-size: 15px; font-weight: bold; color: #a0afbd;"

# 🔖 Stil für den Kicker-Text in den News-Karten
KICKER_STYLE = "font-size: 13px; color: #b0b0b0;"
