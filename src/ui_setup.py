from PyQt6.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QPushButton
import style
import exporter


def setup_window(self):
    """Setzt grundlegende Eigenschaften des Fensters."""
    self.setWindowTitle("News Scraper Steve Minder")
    self.resize(1000, 700)
    self.setStyleSheet(style.MAIN_WINDOW_STYLE)

def setup_layout(self):
    """Initialisiert das Hauptlayout."""
    self.layout = QVBoxLayout(self)
    self.layout.addWidget(self.create_header())

    # Export-Button erstellen & Styling setzen
    self.export_button = QPushButton("News exportieren")
    self.export_button.setStyleSheet(style.EXPORT_BUTTON_STYLE)
    self.export_button.clicked.connect(lambda: exporter.export_news(self, self.news_sources, self.fetch_news, self.fetch_api_news, self.tabs))
    self.layout.addWidget(self.export_button)  # Fügt den Button ins Layout ein

def setup_tabs(self):
    """Erstellt die Tabs für Nachrichtenquellen."""
    self.tabs = QTabWidget()
    self.layout.addWidget(self.tabs)
    self.tabs.setStyleSheet(style.TAB_WIDGET_STYLE)  # Wende das Styling an

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

    for name, data in self.news_sources.items():
        tab = QWidget()
        self.tabs.addTab(tab, name)
        self.create_news_tab(tab, name, data["url"], data["selectors"])

    # 🚀 Neuer Tab für TechCrunch API News
    techcrunch_tab = QWidget()
    self.tabs.addTab(techcrunch_tab, "TechCrunch [API]")
    self.create_api_news_tab(techcrunch_tab)