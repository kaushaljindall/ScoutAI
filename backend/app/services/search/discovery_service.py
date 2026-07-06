"""Core discovery service — orchestrates parallel provider execution with events and cache."""
import asyncio
import time
import uuid
from typing import AsyncGenerator, List, Optional, Dict, Any
from loguru import logger

from app.providers.base.base_provider import BaseSearchProvider, DiscoveredBusiness
from app.providers.registry import get_available_providers
from app.services.merge.merge_engine import merge_results
from app.services.cache import search_cache
from app.events.bus import event_bus, AgentEvent, EventType
from app.core.config import settings


class ProviderResult:
    def __init__(self, provider_name: str, display_name: str):
        self.provider_name = provider_name
        self.display_name = display_name
        self.status: str = "pending"      # pending | running | completed | failed
        self.results: List[DiscoveredBusiness] = []
        self.error: Optional[str] = None
        self.duration: Optional[float] = None
        self.started_at: Optional[float] = None


class DiscoveryService:
    """Runs all available providers in parallel and streams progress events."""

    async def discover(
        self,
        query: str,
        location: Optional[str],
        session_id: uuid.UUID,
        max_results_per_provider: int = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Async generator that yields SSE-friendly progress events, then final results.
        Yields dicts with 'event' and 'data' keys.
        """
        max_results = max_results_per_provider or settings.SEARCH_MAX_RESULTS_PER_PROVIDER
        providers = get_available_providers()
        provider_names = [p.name for p in providers]

        # --- Cache check ---
        cached = search_cache.get_cached(query, location, provider_names)
        if cached is not None:
            yield {"event": "progress", "data": {"message": "Loaded from cache", "stage": "completed", "total": len(cached)}}
            yield {"event": "results", "data": [b.model_dump(mode='json') for b in cached]}
            yield {"event": "finished", "data": {"total": len(cached), "cached": True, "duration": 0}}
            return

        start_time = time.time()

        # --- Planning event ---
        await event_bus.publish(AgentEvent(
            session_id=session_id,
            event_type=EventType.SEARCH_STARTED,
            payload={"query": query, "location": location, "providers": provider_names}
        ))
        yield {"event": "progress", "data": {"message": f"Planning search with {len(providers)} providers...", "stage": "planning", "providers": [
            {"name": p.name, "display_name": p.display_name, "status": "pending"} for p in providers
        ]}}

        provider_results: Dict[str, ProviderResult] = {
            p.name: ProviderResult(p.name, p.display_name) for p in providers
        }

        # --- Run providers concurrently ---
        async def run_provider(provider: BaseSearchProvider) -> List[DiscoveredBusiness]:
            result_tracker = provider_results[provider.name]
            result_tracker.status = "running"
            result_tracker.started_at = time.time()

            await event_bus.publish(AgentEvent(
                session_id=session_id,
                event_type=EventType.PROVIDER_STARTED,
                payload={"provider": provider.name}
            ))

            try:
                results = await asyncio.wait_for(
                    provider.safe_search(query, location, max_results),
                    timeout=settings.SEARCH_PROVIDER_TIMEOUT,
                )
                result_tracker.results = results
                result_tracker.status = "completed"
                result_tracker.duration = time.time() - result_tracker.started_at

                await event_bus.publish(AgentEvent(
                    session_id=session_id,
                    event_type=EventType.PROVIDER_COMPLETED,
                    payload={"provider": provider.name, "count": len(results), "duration": result_tracker.duration}
                ))
                logger.success(f"[discovery] {provider.display_name}: {len(results)} results in {result_tracker.duration:.2f}s")
                return results

            except asyncio.TimeoutError:
                result_tracker.status = "failed"
                result_tracker.error = f"Timed out after {settings.SEARCH_PROVIDER_TIMEOUT}s"
                result_tracker.duration = time.time() - result_tracker.started_at
                await event_bus.publish(AgentEvent(
                    session_id=session_id,
                    event_type=EventType.PROVIDER_FAILED,
                    payload={"provider": provider.name, "error": result_tracker.error}
                ))
                logger.warning(f"[discovery] {provider.display_name} timed out.")
                return []

            except Exception as e:
                result_tracker.status = "failed"
                result_tracker.error = str(e)
                result_tracker.duration = time.time() - result_tracker.started_at
                await event_bus.publish(AgentEvent(
                    session_id=session_id,
                    event_type=EventType.PROVIDER_FAILED,
                    payload={"provider": provider.name, "error": str(e)}
                ))
                logger.error(f"[discovery] {provider.display_name} failed: {e}")
                return []

        yield {"event": "progress", "data": {"message": "Running providers in parallel...", "stage": "running"}}

        tasks = [run_provider(p) for p in providers]
        all_results_lists = await asyncio.gather(*tasks, return_exceptions=False)

        # --- Emit provider status update ---
        provider_statuses = [
            {
                "name": r.provider_name,
                "display_name": r.display_name,
                "status": r.status,
                "count": len(r.results),
                "duration": r.duration,
                "error": r.error,
            }
            for r in provider_results.values()
        ]
        yield {"event": "providers_done", "data": {"providers": provider_statuses}}

        # --- Merge ---
        yield {"event": "progress", "data": {"message": "Merging results...", "stage": "merging"}}
        merged = merge_results(all_results_lists)

        # --- Cache ---
        search_cache.set_cached(query, location, provider_names, merged)

        total_duration = time.time() - start_time
        errors = {name: r.error for name, r in provider_results.items() if r.error}

        await event_bus.publish(AgentEvent(
            session_id=session_id,
            event_type=EventType.SEARCH_FINISHED,
            payload={"total": len(merged), "duration": total_duration, "errors": errors}
        ))

        yield {"event": "results", "data": [b.model_dump(mode='json') for b in merged]}
        yield {"event": "finished", "data": {
            "total": len(merged),
            "duration": round(total_duration, 2),
            "cached": False,
            "providers": provider_statuses,
            "errors": errors,
        }}


discovery_service = DiscoveryService()
