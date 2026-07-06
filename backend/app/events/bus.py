import asyncio
from enum import Enum
from typing import Any, Callable, Dict, List
from loguru import logger
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class EventType(str, Enum):
    # Phase 5A — Agent events
    SEARCH_STARTED = "search_started"
    PLANNING_COMPLETE = "planning_complete"
    TOOL_STARTED = "tool_started"
    TOOL_COMPLETED = "tool_completed"
    TOOL_FAILED = "tool_failed"
    RETRY = "retry"
    EXECUTION_FINISHED = "execution_finished"
    # Phase 5B — Discovery events
    PROVIDER_STARTED = "provider_started"
    PROVIDER_COMPLETED = "provider_completed"
    PROVIDER_FAILED = "provider_failed"
    SEARCH_PROGRESS = "search_progress"
    SEARCH_FINISHED = "search_finished"

class AgentEvent(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    session_id: uuid.UUID
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)

class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[AgentEvent], Any]]] = {
            event_type: [] for event_type in EventType
        }
        self._queue: asyncio.Queue = asyncio.Queue()
        self._worker_task = None

    def subscribe(self, event_type: EventType, callback: Callable[[AgentEvent], Any]):
        self._subscribers[event_type].append(callback)

    async def publish(self, event: AgentEvent):
        """Publish event asynchronously without blocking."""
        await self._queue.put(event)

    async def _process_events(self):
        while True:
            event: AgentEvent = await self._queue.get()
            try:
                # Notify all subscribers
                callbacks = self._subscribers.get(event.event_type, [])
                for callback in callbacks:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
            except Exception as e:
                logger.error(f"Error processing event {event.event_id}: {e}")
            finally:
                self._queue.task_done()

    def start(self):
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._process_events())

    async def stop(self):
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

# Global event bus
event_bus = EventBus()
