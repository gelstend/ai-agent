from abc import ABC, abstractmethod
from typing import Any


class MCPTool(ABC):
    """
    MCP Tool 抽象
    """

    name: str
    description: str

    @abstractmethod
    def run(self, input: Any, context) -> Any:
        pass
