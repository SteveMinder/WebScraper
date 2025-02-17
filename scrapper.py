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

        print(f"[DEBUG] {len(kickers)} Kicker, {len(titles)} Titel, {len(images)} Bilder, {len(links)} Links gefunden.")

        results = []
        for kicker, title, img, link in zip(kickers, titles, images, links):
            kicker_text = kicker.text.strip()
            title_text = title.text.strip()
            img_url = img.get('src', 'Kein Bild') if img else 'Kein Bild'
            article_url = urljoin(url, link.get('href', ''))

            results.append({
                "kicker": kicker_text,
                "title": title_text,
                "image": img_url,
                "link": article_url
            })

            print(f"[DEBUG] Kicker: {kicker_text}")
            print(f"[DEBUG] Title: {title_text}")
            print(f"[DEBUG] Bild-URL: {img_url}")
            print(f"[DEBUG] Artikel-Link: {article_url}")
            print("-" * 100)

        return results
    except requests.RequestException as e:
        print(f"[ERROR] Netzwerkfehler: {e}")
        return [{"error": "Netzwerkfehler"}]
    except Exception as e:
        print(f"[ERROR] Allgemeiner Fehler: {e}")
        return [{"error": "Allgemeiner Fehler"}]
