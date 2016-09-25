# 三十七豆瓣爬爬

**[https://github.com/bluicezhen/Spider-For-Douban](https://github.com/bluicezhen/Spider-For-Douban)**

## 简介：

**三十七豆瓣爬爬**是一个简单的豆瓣爬虫程序程序，主要有一下功能：

- 根据用户ID爬取用户标记的电影，并保存为json。
- 下载豆瓣电影的海报。
- 将海报上传至七牛云存储

## 安装：

当前不支持自动安装，`main.py`是入口文件，有经验的用户可以试图自己写shell脚本，不会写shell脚本的可以尝试和我交个朋友。

我自己的shell脚本是这样写的：

```Shell
#!/bin/bash
source /Users/bluicezhen/Documents/Code/Blog-Server/.venv/bin/activate
python /Users/bluicezhen/Documents/Code/Blog-Server/main.py $1 $2
```

## 用法：

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init                   初始化一个豆瓣爬虫，创建目录与配置文件
  movie-get              获取并存储电影信息
  movie-poster-download  下载电影海报
  movie-upload           上传海报至七牛云存储
  movie_to-html          编译生成HTML

Process finished with exit code 0
```