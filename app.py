import streamlit as st
import pandas as pd
from database import SessionLocal, ArticleEvent, Base, engine

st.set_page_config(page_title="Muon Solutions | Competitor Intel", layout="wide")
st.title("Muon Solutions: Competitor Tracking Dashboard")

Base.metadata.create_all(bind=engine)

session = SessionLocal()
events = session.query(ArticleEvent).order_by(ArticleEvent.created_at.desc()).all()
