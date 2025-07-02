import sys

from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QPushButton
import style
import exporter # alter exporter (CSV)
from db_exporter import export_news_to_db # neuer exporter in db

# ============================
# 🏠 FENSTER-KONFIGURATION
# ============================

def setup_window(self):
    """
    Setzt die grundlegenden Eigenschaften des Hauptfensters.

    - Setzt den Fenstertitel.
    - Definiert die Fenstergrösse.
    - Wendet den Style aus `style.py` an.
    """
    self.setWindowTitle("News Scraper Steve Minder")  # 🏷️ Titel des Fensters
    self.resize(1000, 700)  # 📏 Fenstergrösse (Breite x Höhe)
    self.setStyleSheet(style.MAIN_WINDOW_STYLE)  # 🎨 Stil setzen


# ============================
# 📌 LAYOUT-EINRICHTUNG
# ============================

def setup_layout(self):
    """
    Erstellt das Hauptlayout des Fensters.

    - Fügt den Header hinzu.
    - Erstellt den Export-Button mit Styling und Funktion.
    """
    self.layout = QVBoxLayout(self)  # 📐 Hauptlayout (vertikal)
    self.layout.addWidget(self.create_header())  # 📰 Überschrift hinzufügen
    """
    # 📤 Export-Button für das Speichern von Nachrichten
    self.export_button = QPushButton("News exportieren")
    self.export_button.setStyleSheet(style.EXPORT_BUTTON_STYLE)  # Stil setzen
    self.export_button.clicked.connect(
        lambda: exporter.export_news(
            self, self.news_sources, self.fetch_news, self.fetch_api_news, self.tabs
        )
    )

    self.layout.addWidget(self.export_button)  # 🎯 Button ins Layout einfügen
    """

    self.export_button_db = QPushButton("In Datenbank exportieren")
    self.export_button_db.setStyleSheet(style.EXPORT_BUTTON_STYLE)
    self.export_button_db.clicked.connect(
        lambda: export_news_to_db(self.news_sources, self.fetch_news, self.fetch_api_news, self.tabs)
    )
    self.layout.addWidget(self.export_button_db)

# ============================
# 📰 TAB-VERWALTUNG (NEWS-QUELLEN)
# ============================

def setup_tabs(self):
    """
    Erstellt und verwaltet die Tabs für verschiedene Nachrichtenquellen.

    - Erstellt Tabs für definierte Nachrichtenquellen (Bern Ost, Nau).
    - Erstellt einen separaten Tab für die TechCrunch API.
    """
    self.tabs = QTabWidget()  # 📑 Tab-Widget initialisieren
    self.layout.addWidget(self.tabs)  # 🔗 Tabs ins Layout einfügen
    self.tabs.setStyleSheet(style.TAB_WIDGET_STYLE)  # 🎨 Styling anwenden

    # 📡 Definierte Nachrichtenquellen mit passenden Selektoren
    self.news_sources = {
        "Bern Ost": {
            "url": "https://www.bern-ost.ch/",
            "selectors": {
                "kicker_tag": "span",
                "kicker_class": "content-box-kicker",
                "title_tag": "h2",
                "title_class": "content-box-title",
                "img_tag": "img",
                "img_class": "img-fluid",
                "link_tag": "a",
                "link_class": "content-box"
            }
        },
        "Nau": {
            "url": "https://www.nau.ch/news",
            "selectors": {
                "kicker_tag": "span",
                "kicker_class": "block",
                "title_tag": "span",
                "title_class": "py-1",
                "img_tag": "img",
                "img_class": "object-cover",
                "link_tag": "a",
                "link_class": "text-black"
            }
        }
    }

    # 🔄 Erstelle für jede Nachrichtenquelle einen eigenen Tab
    for name, data in self.news_sources.items():
        tab = QWidget()
        self.tabs.addTab(tab, name)  # 📑 Tab hinzufügen
        self.create_news_tab(tab, name, data["url"], data["selectors"])

    # 🚀 Neuer Tab für TechCrunch API News
    techcrunch_tab = QWidget()
    self.tabs.addTab(techcrunch_tab, "TechCrunch [API]")  # 📡 API-Tab hinzufügen
    self.create_api_news_tab(techcrunch_tab)