def filter_news_by_query(news, search_query):
    """Filtert die Nachrichten nach einem Suchbegriff in Titel oder Kicker."""
    if not search_query:
        return news  # Keine Suche, alle Artikel zurückgeben

    filtered_news = []
    search_query = search_query.lower()

    for article in news:
        title = article.get("title", "").lower()
        kicker = article.get("kicker", "").lower()

        if search_query in title or search_query in kicker:
            filtered_news.append(article)

    print(f"[DEBUG] {len(filtered_news)} Artikel gefunden für die Suche: '{search_query}'")
    return filtered_news