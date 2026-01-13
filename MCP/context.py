from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class MCPContext:
    """
    MCP 上下文：
    - 给模型看的结构化信息
    """
    user_id: str
    session_id: str

    variables: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)

    def add_message(self, message: str):
        self.history.append(message)

    def set_var(self, key: str, value: Any):
        self.variables[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "variables": self.variables,
            "history": self.history,
        }
