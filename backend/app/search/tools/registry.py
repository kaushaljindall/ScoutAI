from typing import List, Dict, Any, Callable
from pydantic import BaseModel

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        
    def register(self, name: str):
        def decorator(func: Callable):
            self.tools[name] = func
            return func
        return decorator
        
    def get_tool(self, name: str) -> Callable:
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found in registry.")
        return self.tools[name]
        
    def list_tools(self) -> List[str]:
        return list(self.tools.keys())

registry = ToolRegistry()

# ==========================================
# Tool Implementations (Independent of Agents)
# ==========================================

@registry.register("search_businesses")
async def search_businesses(queries: List[str], limit: int) -> List[str]:
    # Integrated GoogleSearch / SearXNG
    urls = []
    try:
        from googlesearch import search
        import asyncio
        def do_searches():
            found = []
            for q in queries:
                found.extend(list(search(q, num_results=limit, lang="en")))
            return found
        urls = await asyncio.to_thread(do_searches)
    except Exception as e:
        pass
    return urls

@registry.register("crawl_website")
async def crawl_website(url: str) -> Dict[str, Any]:
    # Using existing scraper for MVP, can be swapped with Crawl4AI
    from app.services.discovery.scraper import WebScraper
    scraper = WebScraper()
    return await scraper.scrape_website(url)

@registry.register("validate_business")
async def validate_business(urls: List[str]) -> List[str]:
    # Deduplication and blacklist removal
    seen = set()
    unique = []
    ignore_list = ["facebook.com", "instagram.com", "justdial.com", "indiamart.com", "yelp.com", "linkedin.com", "wikipedia.org", "w3.org"]
    
    for url in urls:
        domain = url.split("://")[-1].split("/")[0].replace("www.", "").lower()
        if domain not in seen and not any(ig in domain for ig in ignore_list):
            seen.add(domain)
            unique.append(url)
    return unique

@registry.register("analyze_business")
async def analyze_business(business_data: Dict[str, Any]) -> Dict[str, Any]:
    # Use existing AI Analyzer
    from app.services.ai.analyzer import AIService
    from app.services.ai.provider import GeminiProvider
    from app.core.config import settings
    
    if not settings.GEMINI_API_KEY:
        return {}
        
    class FakeBusiness:
        def __init__(self, data):
            self.business_name = data.get("domain", "Unknown")
            self.website = data.get("url", "")
            self.phone = data.get("phone", "")
            self.email = data.get("email", "")
            self.raw_data = {"scraped_text": data.get("raw_text", "")[:1000]}
            
    biz = FakeBusiness(business_data)
    ai_service = AIService(GeminiProvider(settings.GEMINI_API_KEY))
    
    return await ai_service.analyze(biz)

@registry.register("generate_outreach")
async def generate_outreach(analysis_data: Dict[str, Any]) -> str:
    # Placeholder for outreach generation tool
    return "Hello, we noticed your website could use some improvements..."

@registry.register("save_business")
async def save_business(data: Dict[str, Any], intent: Dict[str, Any]) -> str:
    from app.models.scout import Business, BusinessAnalysis
    business = Business(
        business_name=data.get("domain", "Unknown"),
        website=data.get("url", ""),
        category=intent.get("category", "General"),
        city=intent.get("city", ""),
        email=data.get("email"),
        phone=data.get("phone"),
        linkedin=data.get("linkedin"),
        instagram=data.get("instagram"),
        facebook_url=data.get("facebook_url"),
        source="LangGraph AI Agent",
        raw_data={"scraped_text": data.get("raw_text", "")[:500]}
    )
    await business.insert()
    
    if data.get("opportunity_score"):
        analysis = BusinessAnalysis(
            business_id=str(business.id),
            summary_short=data.get("summary_short"),
            summary_medium=data.get("summary_medium"),
            summary_long=data.get("summary_long"),
            strengths=data.get("strengths"),
            weaknesses=data.get("weaknesses"),
            opportunities=data.get("opportunities"),
            opportunity_score=data.get("opportunity_score"),
            confidence_score=data.get("confidence_score"),
            ai_tags=data.get("ai_tags"),
            estimated_budget=data.get("estimated_budget"),
            recommended_services=data.get("recommended_services")
        )
        await analysis.insert()
        
    return str(business.id)
