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
        background-color: #00a8e8;
        color: white;
        padding: 10px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    QPushButton:hover {
        background-color: #0088cc;
    }
    QPushButton:pressed {
        background-color: #0077aa;
    }
"""

# Style für News-Karten
CARD_STYLE = """
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 6px;
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
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
