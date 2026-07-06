import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import String, DateTime, JSON, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from enum import Enum

from app.database.postgres import Base

class ExecutionState(str, Enum):
    PENDING = "Pending"
    PLANNING = "Planning"
    EXECUTING = "Executing"
    WAITING = "Waiting"
    RETRYING = "Retrying"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class SearchSession(Base):
    __tablename__ = "search_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String, index=True)
    original_query: Mapped[str] = mapped_column(Text)
    planner_output: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    execution_time: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[ExecutionState] = mapped_column(SQLEnum(ExecutionState), default=ExecutionState.PENDING)
    errors: Mapped[Optional[List[str]]] = mapped_column(JSONB, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    executions: Mapped[List["AgentExecution"]] = relationship("AgentExecution", back_populates="session", cascade="all, delete-orphan")


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("search_sessions.id", ondelete="CASCADE"))
    agent_name: Mapped[str] = mapped_column(String)
    status: Mapped[ExecutionState] = mapped_column(SQLEnum(ExecutionState), default=ExecutionState.PENDING)
    input_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    session: Mapped["SearchSession"] = relationship("SearchSession", back_populates="executions")
    logs: Mapped[List["ExecutionLog"]] = relationship("ExecutionLog", back_populates="execution", cascade="all, delete-orphan")
    tool_invocations: Mapped[List["ToolInvocation"]] = relationship("ToolInvocation", back_populates="execution", cascade="all, delete-orphan")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_executions.id", ondelete="CASCADE"))
    level: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    execution: Mapped["AgentExecution"] = relationship("AgentExecution", back_populates="logs")


class ToolInvocation(Base):
    __tablename__ = "tool_invocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_executions.id", ondelete="CASCADE"))
    tool_name: Mapped[str] = mapped_column(String)
    input_params: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    output_result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_time: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[ExecutionState] = mapped_column(SQLEnum(ExecutionState), default=ExecutionState.PENDING)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    execution: Mapped["AgentExecution"] = relationship("AgentExecution", back_populates="tool_invocations")
