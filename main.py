from database import init_db, SessionLocal, ArticleEvent
from scrapers import scrape_all_competitors
from llm_analyzer import analyze_article

def run_pipeline():
    init_db()
    session = SessionLocal()
    raw_articles = scrape_all_competitors()
    for item in raw_articles:
        exists = session.query(ArticleEvent).filter_by(url=item['url']).first()
        if exists: continue
        analysis = analyze_article(item['title'], item['title'], item['competitor'])
        new_event = ArticleEvent(title=item['title'], url=item['url'], source=item['source'], competitor=item['competitor'], category=analysis.get('category'), impact_level=analysis.get('impact_level'), executive_summary=analysis.get('executive_summary'), actionable_insight=analysis.get('actionable_insight'))
        session.add(new_event)
        session.commit()

if __name__ == "__main__":
    run_pipeline()
