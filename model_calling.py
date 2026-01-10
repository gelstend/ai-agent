"""
模型调用主函数（vLLM OpenAI Compatible）
"""
import re
import requests
import time
from typing import Dict, Tuple, Optional
from common_script import read_config

config_path = "./config.txt"
config = read_config(config_path)

# 配置
SERVER_IP = config["jay_zhang_a800_2"]["ip"]
PORT = 8000
BASE_URL = f"http://{SERVER_IP}:{PORT}/v1"

MODEL_NAME = "Qwen3-32B"

DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}

THINK_PATTERN = re.compile(
    r"<think>(.*?)</think>",
    re.DOTALL | re.IGNORECASE
)


# vllm服务启动查询
def wait_for_service_ready(
    base_url: str,
    max_retry: int = 30,
    interval: int = 2
) -> None:
    """等待 vLLM 服务 Ready"""
    for i in range(max_retry):
        try:
            rsp = requests.get(f"{base_url}/models", timeout=5)
            if rsp.status_code == 200:
                print("✅ vLLM 服务 Ready")
                print("📦 可用模型：", rsp.json())
                return
        except Exception as e:
            print(f"⏳ 等待服务就绪 ({i + 1}/{max_retry}):", e)

        time.sleep(interval)

    raise RuntimeError("❌ vLLM 服务未启动或未就绪")


# 构建请求体，prompt
def build_payload(
    system_input: str,
    user_input: str,
    model: str,
    # 最大窗口
    max_tokens: int = 2048*4,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> Dict:
    """构造 Chat Completion 请求体"""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_input},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }


def parse_response(response_json: Dict) -> Tuple[Optional[str], Optional[str]]:
    """
    解析模型返回，支持：
    1. reasoning_content（Qwen / DeepSeek）
    2. 显式 think 字段
    3. <think>...</think> 文本标签
    4. 普通文本兜底
    """

    message = response_json["choices"][0]["message"]

    think = None
    content = message.get("content", "")

    # ===== 结构化 reasoning_content（最优）=====
    if "reasoning_content" in message:
        return message.get("reasoning_content"), content

    # ===== 显式 think 字段 =====
    if "think" in message:
        return message.get("think"), content

    # ===== <think>...</think> 标签解析 =====
    if isinstance(content, str):
        match = THINK_PATTERN.search(content)
        if match:
            think = match.group(1).strip()

            # 把 think 从最终回答中移除
            content = THINK_PATTERN.sub("", content).strip()

            return think, content

    # ===== 普通模型兜底 =====
    return None, content


def chat_completion(payload: Dict) -> Dict:
    """发送 Chat Completion 请求"""
    rsp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=DEFAULT_HEADERS,
        json=payload,
        timeout=600
    )
    rsp.raise_for_status()
    return rsp.json()


def main():
    system_input = "你是一个乐于助人的小机器人，叫233，耐心，谨慎的回答用户的问题~"
    user_input = "你好，简单做个自我介绍"

    wait_for_service_ready(BASE_URL)

    payload = build_payload(
        system_input=system_input,
        user_input=user_input,
        model=MODEL_NAME
    )

    print("\n📨 发送请求")
    print("👤 User:", user_input)

    response_json = chat_completion(payload)

    think, context = parse_response(response_json)
    # 打印模型思考
    if think:
        print("\n🧠 Model Think:")
        print(think)

    # 打印模型输出
    print("\n🤖 Model Answer:")
    print(context)


if __name__ == "__main__":
    main()
