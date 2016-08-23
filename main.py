import http.client
import logging
import time
from pprint import pprint
from bs4 import BeautifulSoup

DOUBAN_ID =         "bluicezhen"
USER_AGENT =        "Spider-37"
COMMON_HEADERS =    {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    def spider_movie():
        # Connect to 豆瓣电影.
        movie_connection = http.client.HTTPSConnection("movie.douban.com")

        # Get user movie page.
        movie_url = "/people/%s/" % DOUBAN_ID
        movie_connection.request("GET", movie_url, headers=COMMON_HEADERS)
        movie_response = movie_connection.getresponse()
        movie_html = movie_response.read().decode("utf-8")

        # Analysis user movie information
        movie_soup = BeautifulSoup(movie_html, "html.parser").find("div", {"id": "db-movie-mine"})
        movie_number_watched = int(movie_soup.find("h2").find("a").text.split("部")[0])

        # Get user movies which is watched.
        for i in range(0, movie_number_watched, 15):
            url = "https://movie.douban.com/people/%s/collect?start=%d&sort=time&rating=all&filter=all&mode=grid"\
                  % (DOUBAN_ID, i)
            try:
                movie_connection.request("GET", url, headers=COMMON_HEADERS)
                movies_page_response = movie_connection.getresponse()
            except http.client.ResponseNotReady:
                movie_connection = http.client.HTTPSConnection("movie.douban.com")
                movie_connection.request("GET", url, headers=COMMON_HEADERS)
                movies_page_response = movie_connection.getresponse()
            logging.info("Get movie infomation page %d:" % (i / 15 + 1))
            movies_html = movies_page_response.read()

            time.sleep(3)

            if i == 45:     # Just for test
                break       # Just for test

if __name__ == "__main__":
    spider_movie()