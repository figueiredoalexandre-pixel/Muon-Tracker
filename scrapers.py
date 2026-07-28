import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from google import genai
from datetime import datetime
from database import SessionLocal, ArticleEvent

# Initialize the new Gemini client securely
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
client = genai.Client(api_key=api_key)

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
    Passes the scraped text to Gemini for analysis and summarization.
    """
    prompt = (
        f"You are an intelligence analyst for Muon Solutions. "
        f"Analyze the following recent text regarding our competitor, {competitor_name}. "
        f"Extract any key technological advancements, funding rounds, or strategic partnerships. "
        f"Provide a concise summary of the threat level or opportunity.\n\n"
        f"Source Text:\n{text_content}"
    )

    try:
        # Call the model using the current production model ID
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        # Capture the exact error string if anything else goes wrong
        return f"API ERROR DETAILS: {str(e)}"

def main():
    """
    The main execution function imported by app.py.
    """
    print("Initializing scraping sequence...")
    
    competitors = {
        "Ideon Technologies": "https://ideon.ai/category/news/", 
        "Exodigo": "https://www.exodigo.com/news" 
        "GScan": "https://gscan.eu/"
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
            
            # 3. Save or update the results in the database
            existing_event = db.query(ArticleEvent).filter(ArticleEvent.url == url).first()
            
            if existing_event:
                print(f"Updating existing record for {competitor}...")
                existing_event.executive_summary = analysis_result
            else:
                print(f"Creating new record for {competitor}...")
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
