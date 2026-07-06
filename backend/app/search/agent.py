import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.search.state import ScoutState
from app.search.tools.registry import registry
from app.services.ai.provider import GeminiProvider
from app.core.config import settings
from pydantic import BaseModel

ai_provider = GeminiProvider(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

class PlannerOutput(BaseModel):
    category: str
    city: str = ""
    country: str = ""
    limit: int = 10
    special_requirements: list[str] = []
    search_queries: list[str]

# --- 1. Planner Agent ---
async def planner_agent(state: ScoutState) -> Dict:
    query = state["query"]
    if not ai_provider:
        return {
            "intent": {"category": query, "limit": 5, "special_requirements": []},
            "search_queries": [query],
            "progress": ["Understanding request", "Planning search"]
        }
    prompt = f"User request: '{query}'. Extract category, city, limit and output 2-3 optimal Google Search queries."
    
    try:
        def generate():
            return ai_provider.generate_structured(prompt, PlannerOutput)
        plan: PlannerOutput = await asyncio.to_thread(generate)
        return {
            "intent": plan.dict(),
            "search_queries": plan.search_queries,
            "progress": ["Understanding request", "Planning search"]
        }
    except Exception as e:
        return {
            "errors": [f"Planner Failed: {e}"],
            "intent": {"category": query, "limit": 5, "special_requirements": []},
            "search_queries": [query]
        }

# --- 2. Search Agent ---
async def search_agent(state: ScoutState) -> Dict:
    queries = state.get("search_queries", [])
    limit = state.get("intent", {}).get("limit", 10)
    
    tool = registry.get_tool("search_businesses")
    urls = await tool(queries, limit)
    
    if not urls:
        # Fallback to mock data
        urls = ["https://www.cult.fit/", "https://goldsgym.in/"] if "gym" in str(queries).lower() else ["https://example.com/biz"]
            
    return {"raw_urls": urls, "progress": ["Discovering businesses"]}

# --- 3. Validation Agent ---
async def validation_agent(state: ScoutState) -> Dict:
    tool = registry.get_tool("validate_business")
    unique = await tool(state.get("raw_urls", []))
    limit = state.get("intent", {}).get("limit", 10)
    return {"unique_urls": unique[:limit], "progress": ["Validating contacts"]}

# --- 4. Crawl Agent ---
async def crawl_agent(state: ScoutState) -> Dict:
    tool = registry.get_tool("crawl_website")
    crawled = []
    
    async def process(url: str):
        try:
            data = await tool(url)
            data["url"] = url
            data["domain"] = url.split("://")[-1].split("/")[0].replace("www.", "").capitalize()
            return data
        except Exception:
            return None
            
    tasks = [process(url) for url in state.get("unique_urls", [])]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    crawled = [r for r in results if r and isinstance(r, dict)]
            
    return {"crawled_data": crawled, "progress": ["Crawling websites"]}

# --- 5. AI Analysis Agent ---
async def analysis_agent(state: ScoutState) -> Dict:
    tool = registry.get_tool("analyze_business")
    analyzed = []
    
    for data in state.get("crawled_data", []):
        try:
            analysis = await tool(data)
            data.update(analysis)
            analyzed.append(data)
        except Exception:
            analyzed.append(data)
            
    return {"analyzed_businesses": analyzed, "progress": ["Analyzing businesses"]}

# --- 6. Ranking Agent ---
async def ranking_agent(state: ScoutState) -> Dict:
    analyzed = state.get("analyzed_businesses", [])
    analyzed.sort(key=lambda x: x.get("opportunity_score", 0), reverse=True)
    return {"analyzed_businesses": analyzed, "progress": ["Ranking opportunities"]}

# --- 7. Outreach Agent ---
async def outreach_agent(state: ScoutState) -> Dict:
    tool = registry.get_tool("generate_outreach")
    for b in state.get("analyzed_businesses", []):
        if b.get("opportunity_score"):
            b["outreach_script"] = await tool(b)
    return {"progress": ["Generating outreach strategies"]}

# --- 8. Storage Agent ---
async def storage_agent(state: ScoutState) -> Dict:
    tool = registry.get_tool("save_business")
    saved = []
    for data in state.get("analyzed_businesses", []):
        sid = await tool(data, state.get("intent", {}))
        if sid: saved.append(sid)
            
    return {"saved_business_ids": saved, "status": "completed", "progress": ["Saving results"]}

# --- Build LangGraph ---
def build_scout_graph() -> StateGraph:
    workflow = StateGraph(ScoutState)
    
    workflow.add_node("planner", planner_agent)
    workflow.add_node("search", search_agent)
    workflow.add_node("validator", validation_agent)
    workflow.add_node("crawl", crawl_agent)
    workflow.add_node("analysis", analysis_agent)
    workflow.add_node("rank", ranking_agent)
    workflow.add_node("outreach", outreach_agent)
    workflow.add_node("storage", storage_agent)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "search")
    workflow.add_edge("search", "validator")
    workflow.add_edge("validator", "crawl")
    workflow.add_edge("crawl", "analysis")
    workflow.add_edge("analysis", "rank")
    workflow.add_edge("rank", "outreach")
    workflow.add_edge("outreach", "storage")
    workflow.add_edge("storage", END)
    
    return workflow.compile()
