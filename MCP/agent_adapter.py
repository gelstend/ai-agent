from langchain_core.tools import Tool
from tool_registry import MCPToolRegistry


def build_langchain_tools(mcp_registry: MCPToolRegistry, context):
    """
    把 MCP Tool 包装成 LangChain Tool
    """
    tools = []

    for tool in mcp_registry.all_tools():
        tools.append(
            Tool(
                name=tool.name,
                description=tool.description,
                func=lambda x, t=tool: t.run(x, context)
            )
        )

    return tools
