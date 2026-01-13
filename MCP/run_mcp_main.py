"""
结合MCP的模型调用主函数（vLLM OpenAI Compatible）
"""
# run_mcp.py
import json
import uuid
from typing import Optional

# 相对导入包内模块
from MCP.mcp_state import MCPState
from MCP.tool_registry import MCPToolRegistry
from MCP.prompt_builder import build_mcp_prompt, build_final_prompt
from MCP.tools.geo_tool import GeoTool
from MCP.tools.weather_tool import WeatherTool
from model_calling import get_model_response


class MCPRunner:
    def __init__(self, user_id: Optional[str] = None, session_id: Optional[str] = None):
        # 创建 state（注意 MCPContext 需要 user_id & session_id）
        user_id = user_id or f"user-{uuid.uuid4().hex[:8]}"
        session_id = session_id or f"session-{uuid.uuid4().hex[:8]}"
        self.state = MCPState(user_id=user_id, session_id=session_id)
        self.registry = MCPToolRegistry()

        # 注册你现有的工具实例
        self.registry.register(GeoTool())
        self.registry.register(WeatherTool())

    def run_once(self, user_input: str) -> str:
        # 1) 构造 Prompt，让 LLM 决定是否调用工具
        prompt = build_mcp_prompt(user_input=user_input, tools=self.registry._tools, context=self.state.context)
        llm_output = get_model_response(prompt)

        print("1)", prompt)

        # 2) 尝试解析为工具调用 JSON
        tool_call = self._try_parse_tool_call(llm_output)
        if not tool_call:
            # LLM 直接回答
            return llm_output

        print("2)", tool_call)

        # 3) 执行工具
        tool_name = tool_call.get("tool")
        tool_input = tool_call.get("input", {})
        tool = self.registry.get(tool_name)
        if not tool:
            return f"Error: tool '{tool_name}' not found"

        tool_result = tool.run(tool_input, self.state.context)

        print("3)", tool_result)

        # 4) 把 Tool 结果回灌到上下文（你需要在 MCPContext/MCPState 实现 add_tool_result）
        # 如果没有该方法，暂时把结果追加为 history
        try:
            self.state.context.add_message(f"[tool {tool_name} input={tool_input} output={tool_result}]")
        except Exception:
            # fallback: append to history attribute
            if hasattr(self.state.context, "history"):
                self.state.context.history.append(f"[tool {tool_name} input={tool_input} output={tool_result}]")

        # 5) 再次构造 prompt 生成最终回答
        final_prompt = build_final_prompt(user_input=user_input, context=self.state.context)
        final_answer = get_model_response(final_prompt)
        print("5)", final_prompt)
        return final_answer

    def _try_parse_tool_call(self, text: str):
        """
        期望 LLM 返回 JSON：
        { "tool": "geocode", "input": {"location": "北京"} }
        """
        try:
            data = json.loads(text.strip())
            if isinstance(data, dict) and "tool" in data and "input" in data:
                return data
        except Exception:
            return None


def main():
    runner = MCPRunner()
    # 测试句子
    examples = [
        "北京市今天天气怎么样？",
        "告诉我上海市今天的温度",
    ]
    for ex in examples:
        print("=== INPUT:", ex)
        print(runner.run_once(ex))
        print()


if __name__ == "__main__":
    main()
