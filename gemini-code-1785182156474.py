import feedparser
import urllib.parse
from config import COMPETITORS, KEYWORDS

def fetch_google_news(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:5]:
        articles.append({"title": entry.title, "url": entry.link, "published": entry.published, "source": "Google News RSS"})
    return articles

def scrape_all_competitors():
    all_news = []
    for competitor in COMPETITORS:
        results = fetch_google_news(f'"{competitor}" AND (funding OR patent OR mining OR contract)')
        for r in results:
            r['competitor'] = competitor
        all_news.extend(results)
    return all_news