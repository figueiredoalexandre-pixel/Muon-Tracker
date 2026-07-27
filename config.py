import os
from dotenv import load_dotenv
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
COMPETITORS = ["Ideon Technologies", "Outer Rim Exploration", "Muon Vision", "Lynkeos Technology", "Geomuon", "Exodigo", "GeologicAI"]
KEYWORDS = ["Muon tomography", "Muography", "Cosmic-ray muon imaging", "Density mapping mining"]
DB_PATH = "sqlite:///data/muon_tracker.db"
