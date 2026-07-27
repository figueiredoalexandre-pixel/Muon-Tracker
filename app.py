import streamlit as st
import pandas as pd
from database import SessionLocal, ArticleEvent

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()

if not events:
    st.info("No competitor data found. Close this and wait for the initialization to complete.")
else:
    st.sidebar.header("Filter Intelligence")
    competitors = list(set([e.competitor for e in events if e.competitor]))
    selected_comp = st.sidebar.multiselect("Competitor", competitors, default=competitors)
    filtered_events = [e for e in events if e.competitor in selected_comp]
    
    for event in filtered_events:
        with st.expander(f"[{event.category}] {event.competitor}: {event.title}"):
            st.markdown(f"**Insight:** {event.actionable_insight}")
            st.markdown(f"[Original Article]({event.url})")
