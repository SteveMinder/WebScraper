import requests
from search import filter_news_by_query  # ✅ Importiere die Suchfunktion zur Filterung von News

def scrape_techcrunch_api(api_key, search_query=None):
    """
    Ruft die Top-Headlines von TechCrunch über die NewsAPI ab und filtert sie optional nach einem Suchbegriff.

    Diese Funktion sendet eine HTTP-Anfrage an die NewsAPI, um aktuelle Nachrichten von TechCrunch abzurufen.
    Falls ein `search_query` angegeben wird, werden die Ergebnisse nach dem Titel oder Kicker gefiltert.

    Args:
        api_key (str): Der API-Schlüssel für die NewsAPI.
        search_query (str, optional): Optionaler Suchbegriff zur Filterung der News. Standard ist None.

    Returns:
        list: Eine Liste von Dictionaries mit den extrahierten Nachrichteninformationen.
              Falls ein Fehler auftritt, wird eine Liste mit einer Fehlernachricht zurückgegeben.
    """
    url = "https://newsapi.org/v2/everything"  # 📡 API-Endpunkt
    params = {
        "sources": "techcrunch",
        "apiKey": api_key
    }

    try:
        # 🌐 HTTP-Anfrage an die API senden
        response = requests.get(url, params=params)
        response.raise_for_status()  # Falls die Anfrage fehlschlägt (z. B. 401, 404, 500), wird eine Exception ausgelöst

        # 📊 JSON-Daten aus der API-Antwort extrahieren
        news_data = response.json()

        # ❌ Fehlerbehandlung: Falls keine Artikel vorhanden sind
        if "articles" not in news_data or not news_data["articles"]:
            print("\n[ERROR] Keine Artikel in der API-Antwort gefunden.")
            return [{"error": "Keine Artikel gefunden"}]

        print(f"\n[INFO] {len(news_data['articles'])} Artikel in der API-Antwort gefunden.")

        # 📥 Verarbeitung der Nachrichtenartikel
        results = []
        for article in news_data["articles"]:
            kicker_text = article.get("source", {}).get("name", "Unbekannte Quelle")  # 📰 Nachrichtenquelle (z. B. TechCrunch)
            title_text = article.get("title", "Kein Titel verfügbar")  # 🏷️ Titel der Nachricht
            img_url = article.get("urlToImage", "Kein Bild verfügbar")  # 🖼️ Bild-URL (falls vorhanden)
            article_url = article.get("url", "Kein Link verfügbar")  # 🔗 Artikel-URL

            # 📝 Nachricht in die Ergebnisliste aufnehmen
            results.append({
                "kicker": kicker_text,
                "title": title_text,
                "image": img_url,
                "link": article_url
            })

            # 🔍 Debugging-Ausgabe zur Kontrolle der API-Daten
            print("\n[DEBUG] Gefundene API-News:")
            print(f"📌 Kicker: {kicker_text}")
            print(f"📰 Titel: {title_text}")
            print(f"🖼️ Bild-URL: {img_url}")
            print(f"🔗 Artikel-Link: {article_url}")
            print("-" * 100)

        # 🔍 Filterung nach Suchbegriff (falls vorhanden)
        filtered_results = filter_news_by_query(results, search_query)

        # 📊 Debugging-Ausgabe für die gefilterten Ergebnisse
        if search_query:
            print(f"\n[INFO] {len(filtered_results)} Ergebnisse nach Filterung mit Suchbegriff '{search_query}' gefunden.")
        else:
            print("[INFO] Kein Suchfilter angewendet.")

        return filtered_results  # ✅ Rückgabe der gefilterten oder ungefilterten Ergebnisse

    except requests.RequestException as e:
        # 🚨 Fehlerbehandlung für Netzwerkprobleme (z. B. keine Internetverbindung, API nicht erreichbar)
        print(f"\n[ERROR] Netzwerkfehler: {e}")
        return [{"error": "Netzwerkfehler"}]

    except Exception as e:
        # 🚨 Allgemeine Fehlerbehandlung für unerwartete Fehler
        print(f"\n[ERROR] Allgemeiner Fehler: {e}")
        return [{"error": "Allgemeiner Fehler"}]
