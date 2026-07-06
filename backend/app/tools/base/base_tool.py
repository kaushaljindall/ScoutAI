from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel

class BaseTool(ABC):
    """
    Base class for all tools in the Agentic system.
    Every tool must implement execute(), validate(), and health_check().
    """

    name: str
    description: str
    args_schema: Type[BaseModel]

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the core logic of the tool."""
        pass

    @abstractmethod
    def validate(self, **kwargs) -> bool:
        """Validate input parameters."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the tool's dependencies/APIs are available."""
        pass
