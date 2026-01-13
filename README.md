# ai-agent
agent小机器人
当前阶段目标：搭建一个具备简单调用工具和RAG能力的知识助手

后续计划演进框架：
agent/
├── app/                        # 应用入口
│   ├── main.py                 # 启动入口
│   ├── api.py                  # Web / CLI 接口
│   └── run_agent.py            # Agent 调用封装
│
├── agents/                     # Agent 定义层（核心）
│   ├── base_agent.py           # Agent 基类
│   ├── knowledge_agent.py      # 通用知识 Agent
│   └── tool_agent.py           # 其它工具型 Agent（预留）
│
├── llms/                       # 模型适配层（非常重要）
│   ├── base_llm.py             # LLM 抽象接口
│   ├── openai_llm.py           # 各种实际模型或者直接的大模型API接口
│   ├── qwen_llm.py
│   └── local_llm.py
│
├── MCP/                      # Tool 层（Agent 能力）
│   ├── base_tool.py
│   ├── search_tool.py
│   ├── calculator_tool.py
│   └── tools/                    # MCP 扩展
│       ├── base_tool.py
│       └── mcp_tools.py
│
├── rag/                        # RAG 子系统
│   ├── loaders/                # 文档加载
│   ├── index/                  # 索引构建
│   ├── retriever.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│
├── memory/                     # 记忆模块
│   ├── conversation_memory.py
│   └── vector_memory.py
│
├── config/                     # 配置中心
│   ├── base.yaml
│   ├── dev.yaml
│   └── prod.yaml
│
├── common_scripts/             # “通用”的工具，脚本
│   ├── logger.py
│   ├── utils.py
│   └── exceptions.py
│
├── tests/                      # 测试用例等等。。。
│
├── requirements.txt
└── README.md
