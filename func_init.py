import click
import json
import os


@click.command(help='Create a new blog, default name is "blog"')
@click.argument("name", default="blog")
def init(name):
    """初始化一个豆瓣爬虫，创建目录与配置文件

    Args:
        name:    [str]   要创建的目录名
    """

    default_config = {  # 默认配置，详见文档
        "douban": {
            "id": "xxx"
        },
        "qiniu": {
            "access_key": "xxx",
            "secret_key": "xxx"
        }
    }

    try:
        os.mkdir(name, mode=0o755)          # 主目录
        os.mkdir("%s/movie" % name, mode=0o755)    # 电影目录
    except FileExistsError:
        print("【致命错误】目录%s已存在，无法初始化！" % name)
        return

    # 创建默认配置文件
    config_file = open("%s/config.json" % name, "wt")
    config_file.write(json.dumps(default_config, ensure_ascii=False, indent=4))
    config_file.close()

    print("初始化成功，创建目录【%s】" % name)