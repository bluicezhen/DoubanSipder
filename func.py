import json

# 同用HTTP头部
COMMON_HEADERS = {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}


def load_config() -> dict:
    """读取并返回配置

    Return [dict] 配置
    """
    config_file = open("config.json")
    config_json = config_file.read()
    config = json.loads(config_json)

    return config
