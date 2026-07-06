from typing import Any, Dict
from pydantic import BaseModel
from loguru import logger

from app.tools.base.base_tool import BaseTool
from app.tools.registry.registry import registry

class PlaceholderArgs(BaseModel):
    pass

def create_placeholder_tool(name_: str, description_: str) -> BaseTool:
    class PlaceholderTool(BaseTool):
        name = name_
        description = description_
        args_schema = PlaceholderArgs

        async def execute(self, **kwargs) -> Dict[str, Any]:
            logger.info(f"Executing placeholder tool: {self.name} with args: {kwargs}")
            return {"status": "success", "message": f"{self.name} executed successfully (placeholder)", "data": kwargs}

        def validate(self, **kwargs) -> bool:
            return True

        async def health_check(self) -> bool:
            return True
            
    return PlaceholderTool()

# Register all required tools
REQUIRED_TOOLS = [
    ("search_businesses", "Search for businesses based on query"),
    ("discover_websites", "Discover websites for businesses"),
    ("crawl_website", "Crawl a specific website"),
    ("extract_contacts", "Extract contacts from a website or text"),
    ("validate_business", "Validate if a business meets criteria"),
    ("enrich_business", "Enrich business profile with additional data"),
    ("analyze_business", "Analyze business based on AI models"),
    ("rank_business", "Rank business against user criteria"),
    ("generate_outreach", "Generate outreach emails for the business"),
    ("save_business", "Save the final business result to the database")
]

def register_placeholders():
    for name, desc in REQUIRED_TOOLS:
        tool = create_placeholder_tool(name, desc)
        registry.register(tool)
