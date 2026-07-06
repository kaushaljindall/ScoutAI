from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

def merge_lists(a: List, b: List) -> List:
    if not a:
        a = []
    if not b:
        b = []
    return a + b

class ScoutState(TypedDict):
    # Input
    user_id: str
    query: str
    
    # State tracking
    status: str # "running", "completed", "failed"
    progress: Annotated[List[str], merge_lists]
    errors: Annotated[List[str], merge_lists]
    
    # Intent Parser
    intent: Optional[Dict[str, Any]]
    
    # Provider/Search URLs
    search_queries: Annotated[List[str], merge_lists]
    raw_urls: Annotated[List[str], merge_lists]
    
    # Deduplication
    unique_urls: List[str]
    
    # Crawler
    crawled_data: Annotated[List[Dict[str, Any]], merge_lists]
    
    # AI Enrichment & Analysis
    analyzed_businesses: Annotated[List[Dict[str, Any]], merge_lists]
    
    # Storage
    saved_business_ids: Annotated[List[str], merge_lists]
