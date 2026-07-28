import streamlit as st
import pandas as pd
from database import SessionLocal, ArticleEvent, Base, engine

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

# Ensure tables exist
Base.metadata.create_all(bind=engine)

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()

# Check if we have data to display
if not events:
    st.info("The database is currently empty. No competitor intelligence has been gathered yet.")
else:
    # Convert the SQLAlchemy query directly into a Pandas DataFrame for easy viewing
    df = pd.read_sql(session.query(ArticleEvent).statement, session.bind)
    
    # Display the interactive table on the dashboard
    st.dataframe(df, use_container_width=True)
