from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def scrape_kicker_title_image(url, kicker_tag, kicker_class, title_tag, title_class, img_tag="img", img_class=None, link_tag="a", link_class=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        kickers = soup.find_all(kicker_tag, class_=kicker_class)
        titles = soup.find_all(title_tag, class_=title_class)
        images = soup.find_all(img_tag, class_=img_class) if img_class else soup.find_all(img_tag)
        links = soup.find_all(link_tag, class_=link_class) if link_class else soup.find_all(link_tag, href=True)

        results = []
        for kicker, title, img, link in zip(kickers, titles, images, links):
            kicker_text = kicker.text.strip()
            title_text = title.text.strip()
            img_url = img.get('src') if img and img.get('src') else "Kein Bild"

            # 🛠 Falls die Bild-URL relativ ist, ergänze sie mit der Haupt-Domain
            img_url = urljoin(url, img_url)

            article_url = urljoin(url, link.get('href', ''))

            results.append({
                "kicker": kicker_text,
                "title": title_text,
                "image": img_url,
                "link": article_url
            })

            # 🔍 Debug-Ausgabe beibehalten
            print("\n[DEBUG] Gefundene News:")
            print(f"📌 Kicker: {kicker_text}")
            print(f"📰 Titel: {title_text}")
            print(f"🖼️ Bild-URL: {img_url}")  # ✅ Zeigt die absolute Bild-URL an
            print(f"🔗 Artikel-Link: {article_url}")
            print("-" * 100)

        return results
    except requests.RequestException as e:
        print(f"\n[ERROR] Netzwerkfehler: {e}")
        return [{"error": "Netzwerkfehler"}]
    except Exception as e:
        print(f"\n[ERROR] Allgemeiner Fehler: {e}")
        return [{"error": "Allgemeiner Fehler"}]
