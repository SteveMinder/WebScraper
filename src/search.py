def filter_news_by_query(news, search_query):
    """
    Filtert eine Liste von Nachrichtenartikeln basierend auf einem Suchbegriff.

    Args:
        news (list): Eine Liste von Dictionaries, die Nachrichtenartikel enthalten.
                     Jedes Dictionary sollte mindestens die Schlüssel "title" und "kicker" haben.
        search_query (str): Der Suchbegriff, nach dem gefiltert wird.
                            Falls None oder leer, werden alle Artikel zurückgegeben.

    Returns:
        list: Eine gefilterte Liste von Nachrichtenartikeln, die den Suchbegriff enthalten.
              Falls keine Artikel gefunden werden, wird eine leere Liste zurückgegeben.
    """
    if not search_query:
        return news  # Keine Sucheingabe -> Alle Artikel zurückgeben

    filtered_news = []  # Liste für die gefilterten Artikel
    search_query = search_query.lower()  # Umwandlung in Kleinbuchstaben für case-insensitive Suche

    for article in news:
        # Titel und Kicker in Kleinbuchstaben umwandeln, um eine Gross-/Kleinschreibung-unabhängige Suche zu ermöglichen
        title = article.get("title", "").lower()
        kicker = article.get("kicker", "").lower()

        # Falls der Suchbegriff im Titel oder Kicker vorkommt, Artikel zur Ergebnisliste hinzufügen
        if search_query in title or search_query in kicker:
            filtered_news.append(article)

    # Debug-Ausgabe für die Anzahl der gefundenen Artikel
    print(f"[DEBUG] {len(filtered_news)} Artikel gefunden für die Suche: '{search_query}'")

    return filtered_news  # Gefilterte Liste zurückgeben
