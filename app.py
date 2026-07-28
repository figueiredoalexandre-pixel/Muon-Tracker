import streamlit as st
import pandas as pd
import subprocess
from database import SessionLocal, ArticleEvent, Base, engine

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

# --- Admin Sidebar ---
with st.sidebar:
    st.header("Admin Controls")
    # This button triggers your scraper script
    if st.button("Fetch Latest Intelligence"):
        with st.spinner("Scraping latest news and running LLM analysis..."):
            try:
                # Executes your scrapers.py file exactly like running it in the terminal
                subprocess.run(["python", "scrapers.py"], check=True)
                st.success("Scraping complete!")
                st.rerun() # Automatically refreshes the dashboard to show the new data
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Main Dashboard ---
# Ensure tables exist
Base.metadata.create_all(bind=engine)

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()

# Display logic
if not events:
    st.info("The database is currently empty. No competitor intelligence has been gathered yet.")
else:
    df = pd.read_sql(session.query(ArticleEvent).statement, session.bind)
    st.dataframe(df, use_container_width=True)
