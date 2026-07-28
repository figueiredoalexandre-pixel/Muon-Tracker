import streamlit as st
import pandas as pd
import subprocess
import sys  # We need this to find the correct Python environment
from database import SessionLocal, ArticleEvent, Base, engine

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

# --- Admin Sidebar ---
with st.sidebar:
    st.header("Admin Controls")
    if st.button("Fetch Latest Intelligence"):
        with st.spinner("Scraping latest news and running LLM analysis..."):
            try:
                # Use sys.executable instead of a generic "python" string
                subprocess.run([sys.executable, "scrapers.py"], check=True)
                st.success("Scraping complete!")
                st.rerun() 
            except Exception as e:
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
