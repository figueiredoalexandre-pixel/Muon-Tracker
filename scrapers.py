import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from anthropic import Anthropic
from datetime import datetime
from database import SessionLocal, ArticleEvent

# Initialize the Anthropic client securely using Streamlit Secrets
anthropic_client = Anthropic(
    api_key=st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY"))
)

def fetch_competitor_news(url):
    """
    Scrapes the target URL for text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        
        return text_content[:4000] 
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def analyze_intelligence(text_content, competitor_name):
    """
    Passes the scraped text to Claude for analysis and summarization.
    """
    prompt = (
        f"You are an intelligence analyst for Muon Solutions. "
        f"Analyze the following recent text regarding our competitor, {competitor_name}. "
        f"Extract any key technological advancements, funding rounds, or strategic partnerships. "
        f"Provide a concise summary of the threat level or opportunity.\n\n"
        f"Source Text:\n{text_content}"
    )

    try:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307", 
            max_tokens=500,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Anthropic API Error: {e}")
        return "Analysis failed due to API error."

def main():
    """
    The main execution function imported by app.py.
    """
    print("Initializing scraping sequence...")
    
    competitors = {
        "Ideon Technologies": "https://ideon.ai/category/news/", 
        "Exodigo": "https://www.exodigo.com/news" 
    }

    db = SessionLocal()

    try:
        for competitor, url in competitors.items():
            print(f"Scraping data for {competitor}...")
            
            raw_text = fetch_competitor_news(url)
            
            if not raw_text or len(raw_text) < 50:
                print(f"Not enough new content found for {competitor}. Skipping.")
                continue
                
            print("Running LLM analysis...")
            
            analysis_result = analyze_intelligence(raw_text, competitor)
            
          # 3. Save the results to the database
            new_event = ArticleEvent(
                competitor=competitor,
                url=url,
                executive_summary=analysis_result,
            )
            
            db.add(new_event)
        
        db.commit()
        print("Database successfully updated with latest intelligence.")
        
    except Exception as e:
        print(f"An unexpected error occurred during the scraping process: {e}")
        db.rollback() 
        raise e       
    
    finally:
        db.close()    

if __name__ == "__main__":
    main()
