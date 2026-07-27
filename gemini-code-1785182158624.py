import json
import anthropic
from config import ANTHROPIC_API_KEY

def analyze_article(title, text_preview, competitor):
    # Simplified fallback for local testing without API key
    return {
        "category": "General News",
        "impact_level": "Medium",
        "executive_summary": "Summary pending API configuration.",
        "actionable_insight": "Review for strategic implications."
    }