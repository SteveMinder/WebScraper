from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def scrape_kicker_title_image(url, kicker_tag, kicker_class, title_tag, title_class, img_tag="img", img_class=None, link_tag="a", link_class=None):
    """
    Scraped Nachrichtenartikel von einer Webseite und extrahiert relevante Informationen.

    Diese Funktion durchsucht eine Webseite nach bestimmten HTML-Tags und extrahiert:
    - Kicker (Kategorie/Untertitel)
    - Titel
    - Bild-URL
    - Artikel-Link

    Falls ein Bild oder ein Link als relative URL angegeben ist, wird diese in eine absolute URL umgewandelt.

    Args:
        url (str): Die URL der Webseite, von der gescraped werden soll.
        kicker_tag (str): HTML-Tag für den Kicker.
        kicker_class (str): CSS-Klasse für den Kicker.
        title_tag (str): HTML-Tag für den Titel.
        title_class (str): CSS-Klasse für den Titel.
        img_tag (str, optional): HTML-Tag für das Bild. Standard ist "img".
        img_class (str, optional): CSS-Klasse für das Bild. Falls None, wird jeder `img`-Tag akzeptiert.
        link_tag (str, optional): HTML-Tag für den Artikel-Link. Standard ist "a".
        link_class (str, optional): CSS-Klasse für den Link. Falls None, wird jeder `a`-Tag mit `href` akzeptiert.

    Returns:
        list: Eine Liste von Dictionaries mit den extrahierten Informationen. Falls ein Fehler auftritt, wird eine Liste mit einer Fehlernachricht zurückgegeben.
    """
    try:
        # 🛠 HTTP-Request an die Webseite senden
        response = requests.get(url)
        response.raise_for_status()  # Falls die Anfrage fehlschlägt, wird eine Exception ausgelöst

        # 📄 HTML-Parsing mit BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # 🔍 Extrahiere Elemente basierend auf den angegebenen Tags & Klassen
        kickers = soup.find_all(kicker_tag, class_=kicker_class)
        titles = soup.find_all(title_tag, class_=title_class)
        images = soup.find_all(img_tag, class_=img_class) if img_class else soup.find_all(img_tag)
        links = soup.find_all(link_tag, class_=link_class) if link_class else soup.find_all(link_tag, href=True)

        # 📊 Ergebnisse speichern
        results = []
        for kicker, title, img, link in zip(kickers, titles, images, links):
            kicker_text = kicker.text.strip()  # 📌 Kicker extrahieren
            title_text = title.text.strip()  # 📰 Titel extrahieren

            # 🖼️ Bild-URL extrahieren, falls vorhanden
            img_url = img.get('src') if img and img.get('src') else "Kein Bild"
            img_url = urljoin(url, img_url)  # Falls die URL relativ ist, in absolute URL umwandeln

            # 🔗 Artikel-Link extrahieren und ebenfalls in absolute URL umwandeln
            article_url = urljoin(url, link.get('href', ''))

            # 📥 Speichere die Daten in einem Dictionary
            results.append({
                "kicker": kicker_text,
                "title": title_text,
                "image": img_url,
                "link": article_url
            })

            # 🔍 Debug-Ausgabe zur Kontrolle der extrahierten Daten
            print("\n[DEBUG] Gefundene News:")
            print(f"📌 Kicker: {kicker_text}")
            print(f"📰 Titel: {title_text}")
            print(f"🖼️ Bild-URL: {img_url}")  # ✅ Zeigt die absolute Bild-URL an
            print(f"🔗 Artikel-Link: {article_url}")
            print("-" * 100)

        return results  # ✅ Liste der gefundenen Artikel zurückgeben

    except requests.RequestException as e:
        # 🚨 Fehlerbehandlung für Netzwerkprobleme (z. B. keine Verbindung, HTTP-Fehler)
        print(f"\n[ERROR] Netzwerkfehler: {e}")
        return [{"error": "Netzwerkfehler"}]

    except Exception as e:
        # 🚨 Allgemeine Fehlerbehandlung für unerwartete Fehler
        print(f"\n[ERROR] Allgemeiner Fehler: {e}")
        return [{"error": "Allgemeiner Fehler"}]
