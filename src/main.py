import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QFrame, QGridLayout, \
    QTabWidget
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
        self.resize(1000, 700)

        # Überschrift hinzufügen
        header_label = QLabel("📰 Aktuelle News auf einen Blick")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #00a8e8;
            padding: 5px;
        """)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Arial';
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(header_label)
        self.tabs = QTabWidget()
        self.bern_tab = QWidget()
        self.nau_tab = QWidget()

        self.tabs.addTab(self.bern_tab, "Bern Ost")
        self.tabs.addTab(self.nau_tab, "Nau")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.create_news_tab(self.bern_tab, "Bern Ost", "https://www.bern-ost.ch/", "span", "content-box-kicker", "h2",
                             "content-box-title", "img", "img-fluid", "a", "content-box")
        self.create_news_tab(self.nau_tab, "Nau", "https://www.nau.ch/news", "span", "block", "span", "py-1", "img",
                             "object-cover", "a", "text-black")

    def create_news_tab(self, tab, name, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class,
                        link_tag, link_class):
        layout = QVBoxLayout(tab)
        update_button = QPushButton(f"{name} News aktualisieren")
        update_button.setStyleSheet("""
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
        """)
        update_button.clicked.connect(
            lambda: self.load_news(tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class,
                                   link_tag, link_class))
        layout.addWidget(update_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        news_container = QWidget()
        grid_layout = QGridLayout(news_container)
        grid_layout.setSpacing(8)
        scroll_area.setWidget(news_container)
        layout.addWidget(scroll_area)

        tab.grid_layout = grid_layout
        self.load_news(tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag,
                       link_class)

    def load_news(self, tab, url, kicker_tag, kicker_class, title_tag, title_class, img_tag, img_class, link_tag,
                  link_class):
        for i in reversed(range(tab.grid_layout.count())):
            widget = tab.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        news = scrapper.scrape_kicker_title_image(url, kicker_tag, kicker_class, title_tag, title_class, img_tag,
                                                  img_class, link_tag, link_class)

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
            background-color: #1e1e1e;
            border-radius: 12px;
            padding: 6px;
            box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
        """)
        card_layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setFixedSize(200, 130)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("""
            border-radius: 8px;
            background-color: #2c2c2c;
            padding: 5px;
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
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #a0afbd;")
        kicker_label = QLabel(f"📌 {kicker}")
        kicker_label.setStyleSheet("font-size: 13px; color: #b0b0b0;")

        if article_url:
            link_label = QLabel(
                f"<a href='{article_url}' style='color:#00a8e8; text-decoration:underline;'>➡️ Weiterlesen</a>")
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
