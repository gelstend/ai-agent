"""
SSH协议远程连接服务器，执行vllm运行命令
"""
import paramiko
import time
from common_script import read_config

config_path = "./config.txt"
config = read_config(config_path)

# ===== 服务器信息 =====
HOST = config["jay_zhang_h20_1"]["ip"]
PORT = 23
USERNAME = "root"
PASSWORD = config["jay_zhang_h20_1"]["passwd"]

# ===== 顺序执行的命令 =====
commands = [
    "pkill -f vllm || true",
    "source /usr/local/miniconda3/etc/profile.d/conda.sh",
    "conda activate longcat",
    "cd /root/model_train",
    "chmod +x run.sh",
    "./run.sh"
]


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("🔗 连接服务器中...")
    client.connect(
        hostname=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        timeout=10
    )

    # 必须使用交互式 shell，conda 才能生效
    shell = client.invoke_shell()
    time.sleep(1)

    for cmd in commands:
        print(f"\n▶ 执行: {cmd}")
        shell.send(cmd + "\n")
        time.sleep(2)

        while shell.recv_ready():
            output = shell.recv(8192).decode("utf-8", errors="ignore")
            print(output, end="")

    print("\n✅ 所有命令执行完成")
    client.close()


if __name__ == "__main__":
    main()
