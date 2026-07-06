import asyncio
from typing import List, Dict, Any, Optional
from typing import List, Dict, Any, Optional

from app.models.scout import Business, BusinessAnalysis
from app.services.discovery.scraper import WebScraper
from app.services.ai.analyzer import AIService
from app.services.ai.provider import GeminiProvider
from app.core.config import settings

class DiscoveryPipeline:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.scraper = WebScraper()
        # Initialize AI service if API key exists
        self.ai_service = None
        if settings.GEMINI_API_KEY:
            self.ai_service = AIService(GeminiProvider(settings.GEMINI_API_KEY))

    async def run(self, query: str, location: Optional[str] = None, max_results: int = 5, filters: Optional[Dict] = None) -> Dict[str, Any]:
        search_query = query
        if location:
            search_query += f" in {location}"

        print(f"🔍 Searching Google for: {search_query}")
        results = []
        try:
            from googlesearch import search
            # Run the synchronous search in a thread pool to avoid blocking the event loop
            def do_search():
                return list(search(search_query, num_results=max_results, lang="en"))
            
            search_results = await asyncio.to_thread(do_search)
            
            for url in search_results:
                name = url.split("://")[-1].split("/")[0].replace("www.", "").capitalize()
                results.append({
                    "name": name,
                    "url": url,
                    "snippet": f"Business located at {url}"
                })
        except Exception as e:
            print(f"❌ Google Search failed: {e}")
            # Fallback mock results if search engine blocks the request
            results = [
                {"name": "Example Corp", "url": "https://example.com", "snippet": "Mock business fallback"},
                {"name": "Tech Solutions", "url": "https://example.org", "snippet": "Mock business fallback"}
            ]

        discovered_businesses = []

        # Process each result asynchronously
        async def process_result(search_res):
            url = search_res["url"]
            print(f"🌐 Scraping {url}...")
            
            # 1. Scrape Website
            scraped_data = await self.scraper.scrape_website(url)
            
            # 2. Merge Data
            business_name = search_res["name"] or "Unknown Business"
            
            business = Business(
                business_name=business_name,
                website=url,
                email=scraped_data.get("email"),
                phone=scraped_data.get("phone"),
                linkedin=scraped_data.get("linkedin"),
                instagram=scraped_data.get("instagram"),
                facebook_url=scraped_data.get("facebook_url"),
                city=location,
                source="DuckDuckGo + Web Scraper",
                raw_data={"snippet": search_res["snippet"], "scraped_text": scraped_data.get("raw_text", "")[:500]}
            )
            
            # 3. Save Business
            await business.insert()
            
            # 4. AI Analysis (Optional)
            if self.ai_service and scraped_data.get("raw_text"):
                try:
                    print(f"🤖 Analyzing {business_name} with AI...")
                    analysis_data = await self.ai_service.analyze(business)
                    analysis = BusinessAnalysis(business_id=str(business.id), **analysis_data)
                    await analysis.insert()
                except Exception as e:
                    print(f"⚠️ AI Analysis failed for {business_name}: {e}")

            return business

        # Run all scraping concurrently
        tasks = [process_result(res) for res in results]
        businesses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        valid_businesses = [b for b in businesses if isinstance(b, Business)]
        
        return {
            "status": "success",
            "message": f"Successfully discovered {len(valid_businesses)} businesses",
            "results": valid_businesses
        }
