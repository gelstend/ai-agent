"""
通用函数脚本
"""
import configparser


def read_config(path):
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    data = {}
    for section in config.sections():
        data[section] = dict(config.items(section))

    return data


if __name__ == "__main__":
    cfg = read_config("config.txt")

    print(cfg["jay_zhang_a800_1"]["ip"])

