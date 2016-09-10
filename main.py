import click
import http.client
import json
import qiniu
from bs4 import BeautifulSoup
from func_init import init
from func_spider_movie import movie_get, movie_poster_download

COMMON_HEADERS = {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}


def spider_movi(douban_id: str):
    URL_MOV = "movie.douban.com"    # 豆瓣电影域名
    URL_IMG = "img3.doubanio.com"   # 豆瓣电影海报域名

    conn_mov = http.client.HTTPSConnection(URL_MOV)
    conn_img = http.client.HTTPSConnection(URL_IMG)

    #初始化七牛云存储
    QINIU_AK = "bLkJDOtulf-H56xaSJw1id4KoU5-U2QJffFSlB_7"       # 七牛 Access Key
    QINIU_SK = "5LuqkX2Kp8NfSdXxt6dC5uw6_7fFcPeu-YPISnhP"       # 七牛 Secret Key
    QINIU_BUCKET_NAME = "github"                                # 七牛存储空间名称
    qi = qiniu.Auth(QINIU_AK, QINIU_SK)                         # 七牛鉴权对象

    # 获取该用户电影概要信息
    url = "/people/%s/" % douban_id                                             # 豆瓣个人主页URL
    conn_mov.request("GET", url, headers=COMMON_HEADERS)
    response = conn_mov.getresponse()
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    div_movie = soup.find("div", {"id": "db-movie-mine"})
    movie_number = int(div_movie.find("h2").find("a").text.split("部")[0])       # 在豆瓣上标记看过电影的数量
    print("爬取概要信息:\n\t%s共标记%d条豆瓣电影" % (douban_id, movie_number))

    # 获取电影
    movies = []                                                                 # 保存电影信息的列表
    for i in range(0, movie_number, 15):
        """获取第i页电影"""

        url = "/people/%s/collect?start=%d&sort=time&rating=all&filter=all&mode=grid" % (douban_id, i)
        # 第i页电影的URL
        conn_mov.request("GET", url, headers=COMMON_HEADERS)
        response = conn_mov.getresponse()
        html = response.read().decode("utf-8")
        print("正在爬取看过的电影，第%d页" % ((i + 15) / 15))

        # 解析电影页HTML信息，soup是当前页电影列表部分的HTML
        soup = BeautifulSoup(html, "html.parser").find("div", attrs={"class": "grid-view"}) \
            .find_all("div", attrs={"class": "item"})

        for soup_movie in soup:
            """解析当前页电影信息"""

            movie_title = soup_movie.find("em").text.split(" /", 1)[0]                      # 电影名
            movie_date = soup_movie.find("span", attrs={"class": "date"}).text              # 观看时间
            movie_score = 0                                                                 # 电影评分，满分为5，0即初始状态
            for j in range(5, 0, -1):
                score_html = soup_movie.find("span", attrs={"class": "rating%d-t" % j})
                if score_html is not None:
                    movie_score = j
                    break
            try:                                                                            # 获取电影评论，有空评论情况
                movie_comment = soup_movie.find("span", attrs={"class": "comment"}).text
            except AttributeError:
                movie_comment = ""
            movie_link = soup_movie.find("a").attrs["href"]                                 # 该电影的豆瓣链接

            # 下载电影海报并上传至七牛云存储
            # 获取豆瓣电影海报大图的链接
            try:
                url = "https://img3.doubanio.com/view/photo/photo/public/%s"\
                        % soup_movie.find("img").attrs["src"].split("/public/")[1]
            except IndexError:
                """ 豆瓣电影某些海报的链接（估计是老电影，像《香巴拉信使》的海报链接是(https://movie.douban.com/subject/2224967/)
                和其他的不太一样，要特殊处理"""
                url = "https://img3.doubanio.com/lpic/%s" % soup_movie.find("img").attrs["src"].split("/spic/")[1]
            conn_img.request("GET", url)
            response = conn_img.getresponse()
            body = response.read()
            # 存储到七牛云
            file_name = "douban/movie/%s.jpg" % movie_title
            qiniu_token = qi.upload_token(QINIU_BUCKET_NAME, file_name, 3600)
            qiniu.put_data(qiniu_token, file_name, body)

            print("\t获取条电影《%s》" %  movie_title)

            # 添加该电影信息到列表
            movies.append({
                "title":    movie_title,
                "date":     movie_date,
                "score":    movie_score,
                "comment":  movie_comment,
                "link":     movie_link
            })

    # 将电影列表存储为json并保存
    movies_json = json.dumps(movies, ensure_ascii=False, indent=4)
    file = open("my_movie.json", "wt", encoding="utf-8")
    file.write(movies_json)
    file.close()


@click.group()
def main():
    pass

if __name__ == "__main__":
    main.add_command(init)
    main.add_command(movie_get)
    main.add_command(movie_poster_download)
    main()
