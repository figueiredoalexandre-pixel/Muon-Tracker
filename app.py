import streamlit as st
import pandas as pd
import subprocess
import sys
from database import SessionLocal, ArticleEvent, Base, engine

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

# --- Admin Sidebar ---
with st.sidebar:
    st.header("Admin Controls")
    if st.button("Fetch Latest Intelligence"):
        with st.spinner("Scraping latest news and running LLM analysis. This may take a moment..."):
            # Capture output and errors instead of letting them hide in the background
            result = subprocess.run(
                [sys.executable, "scrapers.py"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                st.success("Scraping complete!")
                # Show exactly what the scraper was doing
                with st.expander("View Scraper Logs"):
                    st.code(result.stdout)
                st.rerun() 
            else:
                st.error("The scraper encountered an issue.")
                # Show the exact error trace so we can debug it
                with st.expander("View Error Details"):
                    st.code(result.stderr)

# --- Main Dashboard ---
Base.metadata.create_all(bind=engine)

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()

if not events:
    st.info("The database is currently empty. No competitor intelligence has been gathered yet.")
else:
    df = pd.read_sql(session.query(ArticleEvent).statement, session.bind)
    st.dataframe(df, use_container_width=True)
