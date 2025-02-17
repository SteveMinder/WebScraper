import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFrame, QGridLayout, QTabWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import scrapper
import requests
from io import BytesIO
import urllib.parse

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Scraper Steve Minder")
        self.resize(800, 700)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.bern_tab = QWidget()
        self.nau_tab = QWidget()

        self.tabs.addTab(self.bern_tab, "Bern Ost")
        self.tabs.addTab(self.nau_tab, "Nau")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.create_news_tab(self.bern_tab, "Bern Ost", "https://www.bern-ost.ch/", "span", "content-box-kicker", "h2", "content-box-title", "img", "img-fluid", "a", "content-box")
        self.create_news_tab(self.nau_tab, "Nau", "https://www.nau.ch/news", "span", "block", "span", "py-1", "img", "object-cover", "a", "text-black")

    def create_news_tab(self, tab, name, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag, link_class):
        layout = QVBoxLayout(tab)
        update_button = QPushButton(f"{name} News aktualisieren")
        update_button.setStyleSheet("""
                   QPushButton {
                       background-color: #004a99;
                       color: white;
                       padding: 6px;
                       border-radius: 5px;
                       transition: background-color 0.2s;
                   }
                   QPushButton:pressed {
                       background-color: #003377;
                   }
               """)
        update_button.clicked.connect(lambda: self.load_news(tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag, link_class))
        layout.addWidget(update_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        news_container = QWidget()
        grid_layout = QGridLayout(news_container)
        grid_layout.setSpacing(8)
        scroll_area.setWidget(news_container)
        layout.addWidget(scroll_area)

        tab.grid_layout = grid_layout
        self.load_news(tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag, link_class)

    def load_news(self, tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag, link_class):
        for i in reversed(range(tab.grid_layout.count())):
            widget = tab.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        news = scrapper.scrape_kicker_title_image(url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag, link_class)

        if not news:
            label = QLabel("ℹ️ Keine News gefunden.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tab.grid_layout.addWidget(label, 0, 0)
        else:
            for index, item in enumerate(news):
                kicker = item.get("kicker", "N/A")
                title = item.get("title", "N/A")
                image_url = urllib.parse.urljoin(url, item.get("image", ""))
                article_url = item.get("link", None)
                news_card = self.create_news_card(title, kicker, image_url, article_url)
                tab.grid_layout.addWidget(news_card, index // 3, index % 3)

    def create_news_card(self, title, kicker, image_url, article_url=None):
        card = QFrame()
        card.setStyleSheet("""
            background-color: #d0d0d0;
            border-radius: 8px;
            padding: 6px;
            box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        """)
        card_layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setFixedSize(200, 130)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("""
            border: 1px solid #00008B;
            border-radius: 6px;
            background-color: #f0f0f0;
        """)

        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                image_label.setPixmap(pixmap.scaled(
                    210, 140,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                ))
            else:
                image_label.setText("Bild nicht verfügbar")
        except Exception:
            image_label.setText("Bild konnte nicht geladen werden")

        title_label = QLabel(f"<b>🗞️ {title}</b>")
        title_label.setWordWrap(True)  # Automatischer Zeilenumbruch
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("font-size: 14px; color: #2c3e50; line-height: 1.4;")
        kicker_label = QLabel(f"📌 {kicker}")
        kicker_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")

        if article_url:
            link_label = QLabel(f"<a href='{article_url}' style='color:#00008B; text-decoration:underline; text-decoration-style:wavy;'>➡️ Weiterlesen</a>")
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
