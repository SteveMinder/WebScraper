import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFrame, QGridLayout, \
    QTabWidget, QFileDialog, QMessageBox, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import scrapper
import requests
from io import BytesIO
import urllib.parse
import style
import ui_setup
import api_scraper
from search import filter_news_by_query  # 🔍 Importiere die Suchfunktion


class MyWindow(QWidget):
    # Initialisierung
    def __init__(self):
        super().__init__()
        self.news_cache = {}  # 🗂 Speichert die News für eine schnellere Suche
        ui_setup.setup_window(self)
        ui_setup.setup_layout(self)
        ui_setup.setup_tabs(self)

    def create_header(self):
        """Erstellt die Kopfzeile des Fensters."""
        header_label = QLabel("📰 Aktuelle News auf einen Blick")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(style.HEADER_STYLE)
        return header_label

    def create_news_tab(self, tab, name, url, selectors):
        """Erstellt eine Nachrichten-Tab mit einer Suchfunktion."""
        layout = QVBoxLayout(tab)

        # 🔄 Aktualisieren-Button
        update_button = QPushButton(f"{name} News aktualisieren")
        update_button.setStyleSheet(style.BUTTON_STYLE)
        update_button.clicked.connect(lambda: self.refresh_news(tab, name, url, selectors))
        layout.addWidget(update_button)

        # 🔍 Suchfeld
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("🔍 Suchbegriff eingeben...")
        search_button = QPushButton("Suchen")
        search_button.clicked.connect(lambda: self.search_news(tab, name, search_bar.text()))

        layout.addWidget(search_bar)
        layout.addWidget(search_button)

        # 📰 Scrollbare Nachrichtenliste
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        news_container = QWidget()
        grid_layout = QGridLayout(news_container)
        scroll_area.setWidget(news_container)
        layout.addWidget(scroll_area)

        tab.grid_layout = grid_layout
        self.refresh_news(tab, name, url, selectors)  # Erstes Laden der News

    def create_api_news_tab(self, tab):
        """Erstellt einen neuen Tab für die TechCrunch API News."""
        layout = QVBoxLayout(tab)

        # 🔄 Aktualisieren-Button
        update_button = QPushButton("TechCrunch News aktualisieren")
        update_button.setStyleSheet(style.BUTTON_STYLE)
        update_button.clicked.connect(lambda: self.refresh_api_news(tab))
        layout.addWidget(update_button)

        # 🔍 Suchfeld
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("🔍 Suchbegriff eingeben...")
        search_button = QPushButton("Suchen")
        search_button.clicked.connect(lambda: self.search_news(tab, "TechCrunch API", search_bar.text()))

        layout.addWidget(search_bar)
        layout.addWidget(search_button)

        # 📰 Scrollbare Nachrichtenliste
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        news_container = QWidget()
        grid_layout = QGridLayout(news_container)
        scroll_area.setWidget(news_container)
        layout.addWidget(scroll_area)

        tab.grid_layout = grid_layout
        self.refresh_api_news(tab)  # Erstes Laden der API-News

    def search_news(self, tab, name, query):
        """Filtert die bereits geladenen Nachrichten nach einem Suchbegriff."""
        if name == "TechCrunch API":
            news = self.fetch_api_news()
        else:
            url, selectors = self.news_sources[name]["url"], self.news_sources[name]["selectors"]
            news = self.fetch_news(url, selectors)

        filtered_news = filter_news_by_query(news, query)
        self.display_news(tab, filtered_news)

    def fetch_api_news(self):
        """Holt die TechCrunch-News von der API."""
        API_KEY = "39016f1e98d14db08f899e80cffa0197"
        return api_scraper.scrape_techcrunch_api(API_KEY) or []

    def fetch_news(self, url, selectors):
        """Holt Nachrichten von der angegebenen Quelle und gibt eine Liste zurück."""
        try:
            return scrapper.scrape_kicker_title_image(
                url,
                selectors["kicker_tag"], selectors["kicker_class"],
                selectors["title_tag"], selectors["title_class"],
                selectors["img_tag"], selectors["img_class"],
                selectors["link_tag"], selectors["link_class"]
            ) or []
        except Exception as e:
            print(f"Fehler beim Abrufen der Nachrichten von {url}: {e}")
            return []

    def display_news(self, tab, news):
        """Zeigt Nachrichten in der angegebenen Tab an."""
        self.clear_grid_layout(tab.grid_layout)

        if not news:
            label = QLabel("ℹ️ Keine News gefunden.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tab.grid_layout.addWidget(label, 0, 0)
        else:
            for index, item in enumerate(news):
                news_card = self.create_news_card(
                    item.get("title", "N/A"),
                    item.get("kicker", "N/A"),
                    item.get("image", ""),
                    item.get("link", None)
                )
                tab.grid_layout.addWidget(news_card, index // 3, index % 3)

    def refresh_api_news(self, tab):
        """Aktualisiert die TechCrunch API News."""
        news = self.fetch_api_news()
        self.display_news(tab, news)

    def refresh_news(self, tab, name, url, selectors):
        """Aktualisiert die Nachrichtenanzeige in der Tab."""
        news = self.fetch_news(url, selectors)
        self.display_news(tab, news)

    def clear_grid_layout(self, layout):
        """Löscht alle Widgets und Layouts aus einem QGridLayout."""
        while layout.count():
            item = layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                elif item.layout():
                    self.clear_grid_layout(item.layout())

    def load_image(self, url):
        """Lädt ein Bild von einer URL und gibt es als QPixmap zurück."""
        if not url or url == "Kein Bild":
            return None  # ⛔ Falls kein Bild vorhanden ist, gib einfach `None` zurück

        pixmap = QPixmap()
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                pixmap.loadFromData(BytesIO(response.content).read())
                return pixmap.scaled(210, 140, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)
        except requests.RequestException:
            pass
        return None  # Falls das Bild nicht geladen werden konnte
    def create_news_card(self, title, kicker, image_url, article_url=None):
        """Erstellt eine News-Karte mit Titel, Bild und Link."""
        card = QFrame()
        card.setStyleSheet(style.CARD_STYLE)
        card_layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setFixedSize(200, 130)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet(style.IMAGE_STYLE)

        pixmap = self.load_image(image_url)
        if pixmap:
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Bild nicht verfügbar")

        title_label = QLabel(f"<b>🗞️ {title}</b>")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet(style.TITLE_STYLE)

        kicker_label = QLabel(f"📌 {kicker}")
        kicker_label.setStyleSheet(style.KICKER_STYLE)

        if article_url:
            link_label = QLabel(f"<a href='{article_url}'>➡️ Weiterlesen</a>")
            link_label.setOpenExternalLinks(True)
            card_layout.addWidget(link_label)

        card_layout.addWidget(image_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(kicker_label)

        card.setLayout(card_layout)
        return card


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
