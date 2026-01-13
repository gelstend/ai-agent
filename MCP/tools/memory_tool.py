from base import MCPTool


class MemoryTool(MCPTool):
    name = "mcp_memory"
    description = "Store or retrieve MCP context memory"

    def run(self, input: str, context):
        context.add_message(f"[MemoryTool] {input}")
        return "Memory updated"
