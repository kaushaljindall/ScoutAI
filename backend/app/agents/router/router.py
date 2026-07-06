import asyncio
from typing import Dict, Any, Literal
from loguru import logger
from langgraph.graph import StateGraph, END

from app.agents.graph.state import GraphState
from app.agents.planner.planner import plan_execution
from app.agents.executor.engine import ExecutionEngine
from app.schemas.agent import PlanRequest
from app.models.agent import ExecutionState
from app.events.bus import event_bus, AgentEvent, EventType

async def planner_node(state: GraphState) -> Dict[str, Any]:
    """Node that generates a plan based on user query."""
    await event_bus.publish(AgentEvent(
        session_id=state["session_id"],
        event_type=EventType.SEARCH_STARTED,
        payload={"query": state["query"]}
    ))
    
    plan = await plan_execution(PlanRequest(query=state["query"]))
    
    await event_bus.publish(AgentEvent(
        session_id=state["session_id"],
        event_type=EventType.PLANNING_COMPLETE,
        payload={"plan": plan.model_dump()}
    ))
    
    return {"plan": plan, "current_status": ExecutionState.PLANNING}

async def tool_selector_node(state: GraphState) -> Dict[str, Any]:
    """Node that selects tools based on the plan."""
    if not state.get("plan"):
        return {"errors": ["No plan available"], "current_status": ExecutionState.FAILED}
    
    # Select tools directly from the plan's requirements
    tools_selected = state["plan"].requires
    return {"tools_selected": tools_selected, "current_status": ExecutionState.EXECUTING}

async def tool_execution_node(state: GraphState) -> Dict[str, Any]:
    """Node that executes the selected tools in parallel."""
    tools = state.get("tools_selected", [])
    if not tools:
        return {"errors": ["No tools selected"], "current_status": ExecutionState.FAILED}
    
    session_id = state["session_id"]
    
    # Execute all tools concurrently for this phase. In reality, some might be sequential.
    # The execution engine handles timeout and retries.
    tasks = []
    for tool_name in tools:
        # Mock input params based on the query and plan
        kwargs = {"query": state["query"], "intent": state["plan"].intent}
        tasks.append(ExecutionEngine.execute_tool(session_id, tool_name, kwargs))
        
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    formatted_results = []
    errors = []
    for r in results:
        if isinstance(r, Exception):
            errors.append(str(r))
        elif r.get("status") == "failed":
            errors.append(r.get("error", "Unknown tool error"))
        else:
            formatted_results.append(r)
            
    return {
        "tool_results": formatted_results,
        "errors": state.get("errors", []) + errors,
        "current_status": ExecutionState.WAITING if not errors else ExecutionState.FAILED
    }

async def result_validator_node(state: GraphState) -> Dict[str, Any]:
    """Node that validates the execution results."""
    # Simple validation: if there are no errors and results exist, we're good
    if state.get("errors"):
        return {"current_status": ExecutionState.FAILED}
        
    if not state.get("tool_results"):
        return {"errors": ["No results produced"], "current_status": ExecutionState.FAILED}
        
    return {"current_status": ExecutionState.COMPLETED}

def should_continue(state: GraphState) -> Literal["result_validator_node", "__end__"]:
    """Conditional edge logic."""
    if state.get("current_status") == ExecutionState.FAILED:
        return "__end__"
    return "result_validator_node"

def build_graph() -> StateGraph:
    """Build and compile the LangGraph execution pipeline."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("planner_node", planner_node)
    workflow.add_node("tool_selector_node", tool_selector_node)
    workflow.add_node("tool_execution_node", tool_execution_node)
    workflow.add_node("result_validator_node", result_validator_node)
    
    workflow.set_entry_point("planner_node")
    workflow.add_edge("planner_node", "tool_selector_node")
    workflow.add_edge("tool_selector_node", "tool_execution_node")
    
    workflow.add_conditional_edges(
        "tool_execution_node",
        should_continue,
    )
    
    workflow.add_edge("result_validator_node", END)
    
    return workflow.compile()

agent_router = build_graph()
