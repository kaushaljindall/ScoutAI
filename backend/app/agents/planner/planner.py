import os
import json
from loguru import logger
from pydantic_ai import Agent

from app.schemas.agent import PlanResponse, PlanRequest
from app.core.config import settings

# pydantic_ai expects GOOGLE_API_KEY in the environment for Google models
if settings.GEMINI_API_KEY:
    os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY

# Simple Pydantic-AI agent for planning
planner_agent = Agent(
    model='google:gemini-2.5-flash',
    output_type=PlanResponse,
    system_prompt=(
        "You are an expert AI execution planner. Your job is to understand natural language "
        "search requests and generate a structured execution plan. "
        "DO NOT execute the tools, just plan what needs to be done. "
        "Determine the user's intent, the target industry, location, and a list of tool names "
        "required to fulfill the request. Example requires: ['search_businesses', 'discover_websites', 'crawl_website']."
    ),
)


async def plan_execution(request: PlanRequest) -> PlanResponse:
    """Run the planner agent on a user query."""
    logger.info(f"Running planner for query: {request.query}")
    try:
        # pydantic_ai automatically uses litellm or native SDK depending on model.
        # However, to be safe, we use a generic string or properly configured litellm model.
        # You may need to inject Gemini API key properly via env vars (GEMINI_API_KEY).
        result = await planner_agent.run(request.query)
        logger.info(f"Planner generated plan: {result.data}")
        return result.data
    except Exception as e:
        logger.error(f"Planner failed: {e}")
        raise
