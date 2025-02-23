import requests
from search import filter_news_by_query  # ✅ Importiere die Suchfunktion

def scrape_techcrunch_api(api_key, search_query=None):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "sources": "techcrunch",
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()

        if "articles" not in news_data or not news_data["articles"]:
            print("\n[ERROR] Keine Artikel in der API-Antwort gefunden.")
            return [{"error": "Keine Artikel gefunden"}]

        print(f"\n[INFO] {len(news_data['articles'])} Artikel in der API-Antwort gefunden.")

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

            # 🔍 Debug-Ausgabe für jede gefundene API-News
            print("\n[DEBUG] Gefundene API-News:")
            print(f"📌 Kicker: {kicker_text}")
            print(f"📰 Titel: {title_text}")
            print(f"🖼️ Bild-URL: {img_url}")
            print(f"🔗 Artikel-Link: {article_url}")
            print("-" * 100)

        # 🔍 Filterung nach Suchbegriff (falls vorhanden)
        filtered_results = filter_news_by_query(results, search_query)
        print(f"\n[INFO] {len(filtered_results)} Ergebnisse nach Filterung mit Suchbegriff '{search_query}' gefunden." if search_query else "[INFO] Kein Suchfilter angewendet.")

        return filtered_results

    except requests.RequestException as e:
        print(f"\n[ERROR] Netzwerkfehler: {e}")
        return [{"error": "Netzwerkfehler"}]
    except Exception as e:
        print(f"\n[ERROR] Allgemeiner Fehler: {e}")
        return [{"error": "Allgemeiner Fehler"}]
