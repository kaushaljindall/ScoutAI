import asyncio
import time
from typing import Any, Dict
from uuid import UUID
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.tools.base.base_tool import BaseTool
from app.tools.registry.registry import registry
from app.events.bus import event_bus, AgentEvent, EventType
from app.models.agent import ExecutionState


class RetryableError(Exception):
    """Exception raised when a tool fails but can be retried."""
    pass


class NonRetryableError(Exception):
    """Exception raised when a tool fails and should NOT be retried (e.g. validation)."""
    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RetryableError),
    reraise=True,
)
async def _execute_tool_with_retry(tool: BaseTool, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return await tool.execute(**kwargs)
    except NonRetryableError:
        raise
    except Exception as e:
        logger.warning(f"Tool {tool.name} failed with error: {e}. Retrying if possible.")
        raise RetryableError(str(e)) from e


class ExecutionEngine:
    """Engine responsible for running tools with retry and timeout logic."""

    @staticmethod
    async def execute_tool(session_id: UUID, tool_name: str, kwargs: Dict[str, Any], timeout_seconds: int = 30) -> Dict[str, Any]:
        """Execute a single tool with retries, timeout, and events."""
        tool = registry.get_tool(tool_name)
        
        await event_bus.publish(AgentEvent(
            session_id=session_id,
            event_type=EventType.TOOL_STARTED,
            payload={"tool_name": tool_name, "input": kwargs}
        ))
        
        start_time = time.time()
        try:
            # Validate first
            if not tool.validate(**kwargs):
                raise NonRetryableError(f"Validation failed for tool {tool.name} with inputs {kwargs}")

            # Run with timeout and retry
            result = await asyncio.wait_for(
                _execute_tool_with_retry(tool, kwargs),
                timeout=timeout_seconds
            )
            
            execution_time = time.time() - start_time
            await event_bus.publish(AgentEvent(
                session_id=session_id,
                event_type=EventType.TOOL_COMPLETED,
                payload={"tool_name": tool_name, "result": result, "execution_time": execution_time}
            ))
            return {"tool": tool_name, "status": "success", "result": result}
            
        except asyncio.TimeoutError:
            error_msg = f"Tool {tool_name} timed out after {timeout_seconds} seconds"
            logger.error(error_msg)
            await event_bus.publish(AgentEvent(
                session_id=session_id,
                event_type=EventType.TOOL_FAILED,
                payload={"tool_name": tool_name, "error": error_msg}
            ))
            return {"tool": tool_name, "status": "failed", "error": error_msg}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Tool {tool_name} execution failed: {error_msg}")
            await event_bus.publish(AgentEvent(
                session_id=session_id,
                event_type=EventType.TOOL_FAILED,
                payload={"tool_name": tool_name, "error": error_msg}
            ))
            return {"tool": tool_name, "status": "failed", "error": error_msg}
