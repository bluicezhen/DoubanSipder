import click
import json
import http.client
from bs4 import BeautifulSoup
from func import load_config, COMMON_HEADERS


@click.command(name="movie-get", help='获取并存储电影信息')
def movie_get():
    """获取基本信息，获取电影信息，存储信息"""

    # 获取配置
    config = load_config()
    douban_id = config["douban"]["id"]
    

    # 初始化连接豆瓣电影
    host = "movie.douban.com"
    conn = http.client.HTTPSConnection(host)

    # 获取电影业概要信息
    movie_number = get_movie_basic_information(conn, douban_id)
    click.secho("已获取电影基本信息\n\t豆瓣用户%s标记过电影%d部" % (douban_id, movie_number), fg='green')

    # 逐条获取电影信息
    movies = get_movies(movie_number, conn, douban_id)

    # 存储电影信息至文件
    movies_json = json.dumps(movies, ensure_ascii=False, indent=4)
    movies_file = open("movie/movies.json", "wt")
    movies_file.write(movies_json)
    movies_file.close()
    click.secho("文件信息已存储", fg='green')

    conn.close()


@click.command(name="movie-poster-download", help='下载电影海报')
def movie_poster_download():
    """下载电影海报"""

    movies_file = open("movie/movies.json")
    movies = json.load(movies_file)

    movie_poster_download_core(movies)


def movie_poster_download_core(movies: list):
    """下载电影海报的核心函数"""
    host = "img3.doubanio.com"
    conn = http.client.HTTPSConnection(host)

    for movie in movies:
        url = movie["img"].split(".com")[1]
        conn.request("GET", url, headers=COMMON_HEADERS)
        response = conn.getresponse()
        body = response.read()

        file_name = "%s.%s.jpg" % (movie["date"], movie["title"])

        img_file = open("movie/poster/%s" % file_name, "wb")
        img_file.write(body)
        img_file.close()

        click.secho("\t下载电影海报: %s" % file_name)

    conn.close()


def get_movie_basic_information(conn: http.client.HTTPSConnection, douban_id: str) -> int:
    """获取该用户电影概要信息，爬取的页面是https://movie.douban.com/{{ douban_id }}

    Args:
        conn        [http.client.HTTPSConnection]   与豆瓣电影的HTTP连接
        douban_id   [str]                           豆瓣ID

    Returns:
        movie_number [int] # 在豆瓣上标记看过电影的数量
    """
    url = "/people/%s/" % douban_id
    conn.request("GET", url, headers=COMMON_HEADERS)
    response = conn.getresponse()
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    div_movie = soup.find("div", {"id": "db-movie-mine"})
    movie_number = int(div_movie.find("h2").find("a").text.split("部")[0])       # 在豆瓣上标记看过电影的数量

    return movie_number


def get_movies(movie_number: int, conn: http.client.HTTPSConnection, douban_id: str) -> list:
    """获取全部电影信息，并将电影信息存储到列表

    Args:
        movie_number    [int]                           在豆瓣上标记看过电影的数量
        conn            [http.client.HTTPSConnection]   与豆瓣电影的HTTP连接
        douban_id       [str]                           豆瓣ID

    Return: 电影信息列表
    """

    movies = []  # 保存电影信息的列表

    # 获取第i页电影， 豆瓣电影页每页15条记录
    for i in range(0, movie_number, 15):

        url = "/people/%s/collect?start=%d&sort=time&rating=all&filter=all&mode=grid" % (douban_id, i) # 第i页电影的URL
        conn.request("GET", url, headers=COMMON_HEADERS)
        response = conn.getresponse()
        html = response.read().decode("utf-8")
        click.secho("正在爬取看过的电影，第%d页" % ((i + 15) / 15), fg='green')

        soup = BeautifulSoup(html, "html.parser").find("div", attrs={"class": "grid-view"}) \
            .find_all("div", attrs={"class": "item"})

        # 解析当前页电影信息
        for soup_movie in soup:
            movie_title = soup_movie.find("em").text.split(" /", 1)[0]          # 电影名
            movie_date = soup_movie.find("span", attrs={"class": "date"}).text  # 观看时间
            movie_score = 0                                                     # 电影评分，满分为5，0即初始状态
            for j in range(5, 0, -1):
                score_html = soup_movie.find("span", attrs={"class": "rating%d-t" % j})
                if score_html is not None:
                    movie_score = j
                    break
            try:                                                                # 获取电影评论，有空评论情况
                movie_comment = soup_movie.find("span", attrs={"class": "comment"}).text
            except AttributeError:
                movie_comment = ""
            movie_link = soup_movie.find("a").attrs["href"]                     # 该电影的豆瓣链接

            try:                                                                # 获取海报大图链接，方法简单粗暴
                movie_img = "https://img3.doubanio.com/view/photo/photo/public/%s" \
                      % soup_movie.find("img").attrs["src"].split("/public/")[1]
            except IndexError:
                # 豆瓣电影某些海报的链接（估计是老电影，像《香巴拉信使》的海报链接是(https://movie.douban.com/subject/2224967/)
                # 和其他的不太一样，要特殊处理"""
                movie_img = "https://img3.doubanio.com/lpic/%s" % soup_movie.find("img").attrs["src"].split("/spic/")[1]

            movies.append({
                "title": movie_title,
                "date": movie_date,
                "score": movie_score,
                "comment": movie_comment,
                "link": movie_link,
                "img": movie_img
            })
            click.secho("\t获取条电影《%s》" % movie_title, fg='green')

    return movies
