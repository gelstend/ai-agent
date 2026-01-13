from typing import Dict
from tools.base import MCPTool


class MCPToolRegistry:

    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}

    def register(self, tool: MCPTool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> MCPTool:
        return self._tools[name]

    def all_tools(self):
        return list(self._tools.values())
