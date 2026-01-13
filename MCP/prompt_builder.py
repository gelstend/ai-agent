from context import MCPContext


def build_mcp_prompt(user_input: str, tools: dict, context: MCPContext) -> str:
    """
    MCP Agent 决策 Prompt：
    - 告诉模型有哪些工具
    - 让模型决定是否调用工具
    """
    history = "\n".join(context.history)

    tool_descriptions = "\n".join(
        f"- {name}: {tool.description}"
        for name, tool in tools.items()
    )

    prompt = f"""
You are an AI agent with access to external tools.

Available tools:
{tool_descriptions}

Context variables:
{context.variables}

Conversation history:
{history}

User input:
{user_input}

If you need to use a tool, respond ONLY with a valid JSON in this format:
{{
  "tool": "<tool_name>",
  "input": {{ ... }}
}}

If no tool is needed, respond with the final answer text directly.
"""
    return prompt



def build_final_prompt(user_input: str, context) -> str:
    history = "\n".join(context.history) if hasattr(context, "history") else ""
    return f"""
User question:
{user_input}

Tool call results & context:
{history}

Please answer the user's question based on above information in a concise, human-readable format.
"""
