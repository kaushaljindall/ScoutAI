import re
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

class WebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self.phone_pattern = re.compile(r"(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}")

    async def scrape_website(self, url: str) -> Dict[str, Any]:
        result = {
            "website": url,
            "email": None,
            "phone": None,
            "linkedin": None,
            "instagram": None,
            "facebook_url": None,
            "raw_text": ""
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                html = response.text
                
                soup = BeautifulSoup(html, "html.parser")
                
                # Extract text for AI
                for script in soup(["script", "style", "nav", "footer"]):
                    script.extract()
                text = soup.get_text(separator=' ', strip=True)
                result["raw_text"] = text[:2000]  # Limit context for AI

                # Find Emails
                emails = set(self.email_pattern.findall(html))
                # Filter out image extensions or common false positives
                valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))]
                if valid_emails:
                    result["email"] = valid_emails[0]

                # Find Phones
                phones = set(self.phone_pattern.findall(soup.get_text()))
                if phones:
                    result["phone"] = list(phones)[0]

                # Find Socials
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if 'linkedin.com/company' in href:
                        result["linkedin"] = href
                    elif 'instagram.com' in href:
                        result["instagram"] = href
                    elif 'facebook.com' in href:
                        result["facebook_url"] = href
                        
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            
        return result
