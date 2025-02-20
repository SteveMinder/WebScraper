#Style für main.py

# Allgemeine Styles für das Fenster
MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Arial';
    }
"""

# Style für den Überschrift-Label
HEADER_STYLE = """
    font-size: 22px;
    font-weight: bold;
    color: #00a8e8;
    padding: 5px;
"""

# Style für Buttons
BUTTON_STYLE = """
    QPushButton {
        background-color: #1e1e1e;
        color: white;
        font-size: 10px;
        font-weight: bold;
        border: none;
        border-radius: 2px;
        padding: 8px 16px;
        transition: background-color 0.3s;
    }
    QPushButton:hover {
        background-color: #004080;
    }
    QPushButton:pressed {
        background-color: #004080;
    }
"""

EXPORT_BUTTON_STYLE = """
    QPushButton {
        background-color: #1e1e1e;
        color: white;
        font-size: 10px;
        font-weight: bold;
        border: none;
        border-radius: 2px;
        padding: 8px 16px;
        margin-left: 11px;
        width: 179px;
        min-width: 150px;
        max-width: 200px;  /* Verhindert volle Breite */
    }
    QPushButton:hover {
        background-color: #004080;
    }
    QPushButton:pressed {
        background-color: #004080;
    }
"""


# Style für News-Karten
CARD_STYLE = """
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 6px;
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
"""

TAB_WIDGET_STYLE = """
    QTabBar::tab {
        background-color: #1e1e1e;
        min-width: 80px;
        min-height: 20px;
        margin-left: 11px;
        padding: 5px 10px;
        font-size: 10px;
        font-weight: bold;
        border-radius: 2px;
        color: white;
    }
    
    QTabBar::tab:hover {
        background: #004080;
    }
"""

# Style für Bilder in News-Karten
IMAGE_STYLE = """
    border-radius: 8px;
    background-color: #2c2c2c;
    padding: 5px;
"""
# Style für Titel in News-Karten
TITLE_STYLE = "font-size: 15px; font-weight: bold; color: #a0afbd;"

# Style für Kicker-Text in News-Karten
KICKER_STYLE = "font-size: 13px; color: #b0b0b0;"
