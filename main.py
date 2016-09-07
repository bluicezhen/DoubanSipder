import http.client
from bs4 import BeautifulSoup

# 请求通用头部
COMMON_HEADERS = {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}


def book():
    pass


def spider_movie(douban_id: str):
    URL_MOV = "movie.douban.com"    # 豆瓣电影域名
    URL_IMG = "img3.doubanio.com"   # 豆瓣电影海报域名

    conn_mov = http.client.HTTPSConnection(URL_MOV)
    conn_img = http.client.HTTPSConnection(URL_IMG)

    # 获取该用户电影概要信息
    url = "/people/%s/" % douban_id                                         # 豆瓣个人主页URL
    conn_mov.request("GET", url, headers=COMMON_HEADERS)
    response = conn_mov.getresponse()
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    div_movie = soup.find("div", {"id": "db-movie-mine"})
    movie_number = int(div_movie.find("h2").find("a").text.split("部")[0])   # 在豆瓣上标记看过电影的数量




if __name__ == "__main__":
    douban_id = "bluicezhen"
    spider_movie(douban_id)
