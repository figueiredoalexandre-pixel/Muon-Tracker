from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_PATH
import os

os.makedirs("data", exist_ok=True)
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ArticleEvent(Base):
    __tablename__ = "article_events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    published_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    competitor = Column(String)
    category = Column(String)
    impact_level = Column(String)
    executive_summary = Column(Text)
    actionable_insight = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)