import streamlit as st
import pandas as pd
from database import SessionLocal, ArticleEvent, Base, engine

# 1. Import your scraping function directly from the file
# Note: This assumes your scraping logic is inside a function named 'main'
from scrapers import main as run_scraper 

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

# --- Admin Sidebar ---
with st.sidebar:
    st.header("Admin Controls")
    if st.button("Fetch Latest Intelligence"):
        with st.spinner("Scraping latest news and running LLM analysis..."):
            try:
                # 2. Run the function natively instead of using subprocess
                run_scraper()
                st.success("Scraping complete!")
                st.rerun() 
            except Exception as e:
                # This will catch and display ANY python error natively
                st.error(f"An error occurred: {e}")

# --- Main Dashboard ---
Base.metadata.create_all(bind=engine)

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()

if not events:
    st.info("The database is currently empty. No competitor intelligence has been gathered yet.")
else:
    df = pd.read_sql(session.query(ArticleEvent).statement, session.bind)
    st.dataframe(df, use_container_width=True)
