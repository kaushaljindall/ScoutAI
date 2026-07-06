"""Discovery API routes — streaming SSE search + history + providers."""
import uuid
import json
import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.services.search.discovery_service import discovery_service
from app.providers.registry import get_all_providers, get_available_providers
from app.schemas.discovery import DiscoverRequest, ProviderHealthStatus
from app.core.config import settings

router = APIRouter(prefix="/search", tags=["search"])

# In-memory search history (per-process; use DB in production)
_search_history: list = []


@router.post("/discover")
async def discover_businesses(request: DiscoverRequest):
    """
    Streaming SSE endpoint — yields real-time progress and final results.
    Returns Server-Sent Events (text/event-stream).
    """
    session_id = uuid.uuid4()

    async def event_stream():
        try:
            async for event in discovery_service.discover(
                query=request.query,
                location=request.location,
                session_id=session_id,
                max_results_per_provider=request.max_results_per_provider,
            ):
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0)  # let event loop breathe

            # Append to in-memory history
            _search_history.insert(0, {
                "session_id": str(session_id),
                "query": request.query,
                "location": request.location,
            })
            if len(_search_history) > 50:
                _search_history.pop()

        except Exception as e:
            yield f"data: {json.dumps({'event': 'error', 'data': {'message': str(e)}})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/providers")
async def list_providers():
    """List all registered providers and their health status."""
    providers = get_all_providers()
    key_required = {"brave", "google_places"}
    result = []
    for p in providers:
        needs_key = p.name in key_required
        configured = (
            (p.name == "brave" and bool(settings.BRAVE_API_KEY)) or
            (p.name == "google_places" and bool(settings.GOOGLE_PLACES_API_KEY)) or
            p.name not in key_required
        )
        result.append(ProviderHealthStatus(
            name=p.name,
            display_name=p.display_name,
            priority=p.priority,
            is_healthy=configured,
            requires_key=needs_key,
            key_configured=configured,
        ))
    return result


@router.get("/providers/health")
async def check_provider_health():
    """Run health checks on all configured providers."""
    providers = get_available_providers()
    health = {}
    checks = await asyncio.gather(*[p.health_check() for p in providers], return_exceptions=True)
    for p, result in zip(providers, checks):
        health[p.name] = {
            "display_name": p.display_name,
            "healthy": result if isinstance(result, bool) else False,
            "error": str(result) if isinstance(result, Exception) else None,
        }
    return health


@router.get("/history")
async def get_search_history():
    """Return recent search history (in-memory, most recent first)."""
    return {"history": _search_history}


@router.post("/cancel")
async def cancel_search(session_id: str):
    """Placeholder for search cancellation — will integrate with task queue in future phases."""
    return {"status": "cancelled", "session_id": session_id}
