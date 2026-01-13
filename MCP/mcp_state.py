from context import MCPContext


class MCPState:
    """
    管理 MCP Context 生命周期
    """

    def __init__(self, user_id: str, session_id: str):
        self.context = MCPContext(
            user_id=user_id,
            session_id=session_id
        )

    def update_from_user(self, user_input: str):
        self.context.add_message(f"User: {user_input}")

    def update_from_agent(self, agent_output: str):
        self.context.add_message(f"Agent: {agent_output}")
