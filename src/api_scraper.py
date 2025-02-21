import requests

def scrape_techcrunch_api(api_key):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "sources": "techcrunch",
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Fehler abfangen (z.B. 401, 404, 500)
        news_data = response.json()

        # Überprüfen, ob Artikel vorhanden sind
        if "articles" not in news_data or not news_data["articles"]:
            print("[ERROR] Keine Artikel gefunden.")
            return [{"error": "Keine Artikel gefunden"}]

        print(f"[DEBUG] {len(news_data['articles'])} Artikel gefunden.")

        results = []
        for article in news_data["articles"]:
            kicker_text = article.get("source", {}).get("name", "Unbekannte Quelle")
            title_text = article.get("title", "Kein Titel verfügbar")
            img_url = article.get("urlToImage", "Kein Bild verfügbar")
            article_url = article.get("url", "Kein Link verfügbar")

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

# Beispielaufruf mit API-Schlüssel
API_KEY = "DEIN_NEWSAPI_KEY"
news = scrape_techcrunch_api(API_KEY)
